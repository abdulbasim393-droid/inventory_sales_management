from django.urls import path, include
from rest_framework.routers import DefaultRouter



from .views import ProductViewSet, CategoryViewSet, SupplierViewSet, CustomerViewSet

router = DefaultRouter()

router.register("products",ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("suppliers", SupplierViewSet)
router.register("customers",CustomerViewSet)

urlpatterns = [
   path("", include(router.urls)),
   
]