
from .models import Product, Supplier, Category, Customer, Sale
from .serializers import (
    ProductSerializer, 
    SupplierSerializer, 
    CategorySerializer, 
    CustomerSerializer, 
    SaleSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Sum, F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class SaleViewSet(ModelViewSet):
    queryset = (
        Sale.objects
        .select_related("customer", "product")
    )

    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]






class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Product List View, Create Product
class ProductViewSet(ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = (
        Product.objects
        .select_related("category", "supplier")
        .all()
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



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):

    total_products = Product.objects.count()

    total_customers = Customer.objects.count()

    total_sales = Sale.objects.count()

    total_revenue = (
        Sale.objects.aggregate(
            revenue=Sum(
                F("quantity") * F("selling_price")
            )
        )["revenue"]
        or 0
    )

    low_stock = Product.objects.filter(
        quantity__lt=10,
        quantity__gt=0
    ).count()

    out_of_stock = Product.objects.filter(
        quantity=0
    ).count()

    return Response({
        "total_products": total_products,
        "total_customers": total_customers,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock,
        "out_of_stock_products": out_of_stock,
    })