from rest_framework import serializers
from .models import Product, Category




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):


    def validate_sku(self, value):
        if not value:
            raise serializers.ValidationError("SKU cannot be empty")
        return value
    

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    



    def validate(self, data):
        cost_price = data.get('cost_price')
        selling_price = data.get('selling_price')

        if cost_price is not None and cost_price < 0:
            raise serializers.ValidationError("Cost price cannot be negative")

        if selling_price is not None and selling_price < 0:
            raise serializers.ValidationError("Selling price cannot be negative")

        if cost_price and selling_price and selling_price < cost_price:
            raise serializers.ValidationError(
                "Selling price cannot be lower than cost price"
            )

        return data



    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'barcode',
            'description',
            'cost_price',
            'selling_price',
            'quantity',
            'is_active',
            'created_at',
            'updated_at',
            'category',
            'category_detail',
        ]