from .models import *
from rest_framework import serializers

class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = '__all__'


