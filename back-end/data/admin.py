from django.contrib import admin
from .models import *

admin.site.site_header = "OpenWalletTracker"

# Register your models here.
@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "material"]
    search_fields = ["id", "name", "material"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abbr", "ascii_symbl"]
    search_fields = ["id", "name", "abbr", "ascii_symbl"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "creator", "balans"]
    list_filter = ["creator"]
    search_fields = ["id", "title"]


@admin.register(SpendsGroup, IncomesGroup)
class SpendNIncomeGroupsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "wallet"]
    search_fields = ["id", "title"]

@admin.register(Spends, Incomes)
class SpendNIncomeAdmin(admin.ModelAdmin):
    list_display = ["id", "group", "user", "value"]
    search_fields = ["id", "value"]


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "is_staff", "is_superuser"]