from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver

########################################################################
# Модель иконок 
class Icon(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название')
    material = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название MaterialIcon')

    def __str__(self):
        return f"Иконка #{self.id} '{self.name}'"

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"


# Модель валют
class Currency(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Название валюты")
    abbr = models.CharField(max_length=3, null=False, blank=False, verbose_name="Код валюты")
    ascii_symbl = models.CharField(max_length=3, null=True, blank=True, verbose_name="ASCII символ")

    def __str__(self):
        return f"Валюта #{self.id} {self.abbr}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

# Модель кошельков
class Wallet(models.Model):
    title = models.CharField(max_length=255, null=False, blank=True, default="Бюджет", verbose_name="Название")
    icon = models.ForeignKey('Icon', models.SET_NULL, null=True, blank=True, verbose_name="Иконка")
    currency = models.ForeignKey('Currency', models.SET_DEFAULT, null=False, blank=False, default=1, verbose_name="Валюта кошелька")
    balans = models.FloatField(null=False, blank=False, default=0.0, verbose_name="Баланс")
    creator = models.ForeignKey('CustomUser', models.CASCADE, verbose_name="Создатель")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Кошелёк #{self.id}"

    class Meta:
        verbose_name = "Кошелёк"
        verbose_name_plural = "Кошельки"


# Модель группы затрат
class SpendsGroup(models.Model):
    title = models.CharField(max_length=255, null=False, blank=True, default="Общие траты", verbose_name="Название")
    icon = models.ForeignKey('Icon', models.SET_NULL, null=True, blank=True, verbose_name="Иконка")
    wallet = models.ForeignKey('Wallet', models.CASCADE, verbose_name="Кошелек")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Группа затрат #{self.id} '{self.title}'"

    class Meta:
        verbose_name = "Группа трат"
        verbose_name_plural = "Группы трат"


# Модель затрат
class Spends(models.Model):
    group = models.ForeignKey('SpendsGroup', models.CASCADE, null=False, blank=False, verbose_name="Группа затрат")
    user = models.ForeignKey('CustomUser', models.CASCADE, verbose_name="Пользователь")
    value = models.FloatField(null=False, blank=False, verbose_name="Значение")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Трата #{self.id}"

    class Meta:
        verbose_name = "Трата"
        verbose_name_plural = "Траты"


# Модель группы прибыли
class IncomesGroup(models.Model):
    title = models.CharField(max_length=255, null=False, blank=True, default="Общая прибыль", verbose_name="Название")
    icon = models.ForeignKey('Icon', models.SET_NULL, null=True, blank=True, verbose_name="Иконка")
    wallet = models.ForeignKey('Wallet', models.CASCADE, verbose_name="Кошелек")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Группа прибыли #{self.id} '{self.title}'"

    class Meta:
        verbose_name = "Группа прибыли"
        verbose_name_plural = "Группы прибыли"


# Модель прибыли
class Incomes(models.Model):
    group = models.ForeignKey('IncomesGroup', models.CASCADE, null=False, blank=False, verbose_name="Группа прибыли")
    user = models.ForeignKey('CustomUser', models.CASCADE, verbose_name="Пользователь")
    value = models.FloatField(null=False, blank=False, verbose_name="Значение")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Прибыль #{self.id}"

    class Meta:
        verbose_name = "Прибыль"
        verbose_name_plural = "Прибыль"


# Модель пользователя
class CustomUser(AbstractUser):

    wallets = models.ManyToManyField(Wallet, blank=True, verbose_name="Кошельки")

    def __str__(self):
        return f"Пользователь #{self.id} {self.username}"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


################################################################ 
# Триггер сохранения новых затрат или изменения сушествующих
# -----------------------------------------------------------
@receiver(pre_save, sender=Spends)
def trigger_spend_save(sender, instance, **kwargs):
    if instance.id != None:
        old_value = sender.objects.get(id=instance.id).value
        instance.group.wallet.balans += old_value 
    new_value = instance.value
    instance.group.wallet.balans -= new_value 
    instance.group.wallet.save()

# Триггер удаления затрат
# -----------------------------------------------------------
@receiver(pre_delete, sender=Spends)
def trigger_spend_delete(sender, instance, **kwargs):
    value = instance.value
    instance.group.wallet.balans += value 
    instance.group.wallet.save()

# Триггер сохранения новой прибыли или изменения сушествующей
# -----------------------------------------------------------
@receiver(pre_save, sender=Incomes)
def trigger_incomes_save(sender, instance, **kwargs):
    if instance.id != None:
        old_value = sender.objects.get(id=instance.id).value
        instance.group.wallet.balans -= old_value 
    new_value = instance.value
    instance.group.wallet.balans += new_value 
    instance.group.wallet.save()

# Триггер удаления прибыли
# -----------------------------------------------------------
@receiver(pre_delete, sender=Incomes)
def trigger_incomes_delete(sender, instance, **kwargs):
    value = instance.value
    instance.group.wallet.balans -= value 
    instance.group.wallet.save()

# Триггер автоматического создания кошелька
# -----------------------------------------------------------
@receiver(post_save, sender=Wallet)
def trigger_wallet_create(sender, instance, created, **kwargs):
    if created:
        new_spends_group = SpendsGroup.objects.create(wallet=instance)
        new_incomes_group = IncomesGroup.objects.create(wallet=instance)
        new_spends_group.save()
        new_incomes_group.save()