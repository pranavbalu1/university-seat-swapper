from rest_framework import serializers
from .models import Class, SeatExchange

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SeatExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatExchange
        fields = '__all__'
