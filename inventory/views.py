from .models import Product
from .serializers import ProductSerializer

from rest_framework.viewsets import ModelViewSet



# Product List View, Create Product
class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer