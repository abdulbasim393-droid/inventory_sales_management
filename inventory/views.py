from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView




# Product List View, Create Product
class ProductList(ListCreateAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer



# View Specific Product, Update Product
class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    lookup_field = "id"