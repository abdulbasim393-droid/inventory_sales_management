from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard



from .views import ( 
    ProductViewSet,
   CategoryViewSet, 
   SupplierViewSet, 
   CustomerViewSet, 
   SaleViewSet,
   dashboard,
)

router = DefaultRouter()

router.register("products",ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("suppliers", SupplierViewSet)
router.register("customers",CustomerViewSet)
router.register("sales",SaleViewSet)


urlpatterns = [
   path("", include(router.urls)),
   path("dashboard/", dashboard),
   
]