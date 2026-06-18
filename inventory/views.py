from .models import Product
from .serializers import ProductSerializer

from .models import Product, Supplier, Category, Customer
from .serializers import ProductSerializer, SupplierSerializer, CategorySerializer, CustomerSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly





class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# Product List View, Create Product
class ProductViewSet(ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]

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



