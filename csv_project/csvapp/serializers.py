# core/serializers.py
from rest_framework import serializers
from .models import CSVFile

class CSVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = '__all__'


class ProductSearchSerializer(serializers.Serializer):
    product_name = serializers.CharField() 
    sales = serializers.FloatField()
    quantity = serializers.IntegerField()
    discount = serializers.FloatField()
    profit = serializers.FloatField()