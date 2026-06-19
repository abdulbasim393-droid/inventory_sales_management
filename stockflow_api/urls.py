"""
URL configuration for stockflow_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inventory_views.home, name='home'),
    path('login/', inventory_views.login_view, name='login'),
    path('logout/', inventory_views.logout_view, name='logout'),
    path('dashboard/', inventory_views.dashboard_page, name='dashboard_page'),
    path('products/', inventory_views.products_page, name='products_page'),
    path('products/add/', inventory_views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', inventory_views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', inventory_views.product_delete, name='product_delete'),
    path('categories/', inventory_views.categories_page, name='categories_page'),
    path('categories/add/', inventory_views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', inventory_views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', inventory_views.category_delete, name='category_delete'),
    path('suppliers/', inventory_views.suppliers_page, name='suppliers_page'),
    path('suppliers/add/', inventory_views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', inventory_views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', inventory_views.supplier_delete, name='supplier_delete'),
    path('customers/', inventory_views.customers_page, name='customers_page'),
    path('customers/add/', inventory_views.customer_add, name='customer_add'),
    path('customers/edit/<int:pk>/', inventory_views.customer_edit, name='customer_edit'),
    path('customers/delete/<int:pk>/', inventory_views.customer_delete, name='customer_delete'),
    path('sales/', inventory_views.sales_page, name='sales_page'),
    path('sales/add/', inventory_views.sale_add, name='sale_add'),
    path('sales/edit/<int:pk>/', inventory_views.sale_edit, name='sale_edit'),
    path('sales/delete/<int:pk>/', inventory_views.sale_delete, name='sale_delete'),
    path('users/', inventory_views.users_page, name='users_page'),
    path('users/add/', inventory_views.user_add, name='user_add'),
    path('users/edit/<int:pk>/', inventory_views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', inventory_views.user_delete, name='user_delete'),
    path('reports/', inventory_views.reports_page, name='reports_page'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("inventory.urls")),
]
