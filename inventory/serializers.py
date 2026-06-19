from rest_framework import serializers
from .models import Product, Category, Supplier, Customer, Sale
from django.db import transaction


class ProductSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]



class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = ["selling_price", "sale_date"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        if product.quantity < quantity:
            raise serializers.ValidationError(
                "Not enough stock available."
            )

        product.quantity -= quantity
        product.save()

        return Sale.objects.create(**validated_data)



    @transaction.atomic
    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        if product.quantity < quantity:
            raise serializers.ValidationError(
                "Not enough stock available."
            )

        product.quantity -= quantity
        product.save()
        validated_data["selling_price"] = product.selling_price

        sale = Sale.objects.create(**validated_data)

        return sale


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"



class CategorySerializer(serializers.ModelSerializer):

    products = ProductSummarySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Category
        fields = '__all__'



class SupplierSerializer(serializers.ModelSerializer):

    products = ProductSummarySerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = Supplier
        fields = "__all__"


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

        if (
            cost_price is not None
            and selling_price is not None
            and selling_price < cost_price
        ):
            raise serializers.ValidationError(
                "Selling price cannot be lower than cost price"
            )

        return data


    supplier_detail = SupplierSerializer(source="supplier",read_only=True)
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
            'supplier',
            'supplier_detail',
            
        ]