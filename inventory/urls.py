from django.urls import path, include
from rest_framework.routers import DefaultRouter



from .views import ProductViewSet, CategoryViewSet, SupplierViewSet

router = DefaultRouter()

router.register("products",ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("suppliers", SupplierViewSet)

urlpatterns = [
   path("", include(router.urls)),
   
]