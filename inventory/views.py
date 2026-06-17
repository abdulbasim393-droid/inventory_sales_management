from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer



# Product List View, Create Product
@api_view(["GET", "POST"])
def product_list(request):

    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# View Specific Product
@api_view(["GET"])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    serializer = ProductSerializer(product)

    return Response(serializer.data)