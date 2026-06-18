from .models import Product
from .serializers import ProductSerializer

from .models import Product, Supplier, Category
from .serializers import ProductSerializer, SupplierSerializer, CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# Product List View, Create Product
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related(
        "category",
        "supplier"
    )

    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "supplier",
        "is_active",
    ]

    search_fields = [
        "name",
        "sku",
        "barcode",
    ]

    ordering_fields = [
        "selling_price",
        "cost_price",
        "quantity",
        "created_at",
    ]

    ordering = ["-created_at"]


