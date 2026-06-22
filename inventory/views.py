
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from .pagination import ProductPagination

from .forms import (
    ProductForm,
    CategoryForm,
    SupplierForm,
    CustomerForm,
    SaleForm,
    UserForm,
)
from .models import Product, Supplier, Category, Customer, Sale
from .serializers import (
    ProductSerializer, 
    SupplierSerializer, 
    CategorySerializer, 
    CustomerSerializer, 
    SaleSerializer,
)

from .permissions import (
    ProductPermission,
    CategoryPermission,
    SupplierPermission,
    CustomerPermission,
    SalePermission,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet

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
    permission_classes = [SalePermission]






class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]




class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]



class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [SupplierPermission]

# Product List View, Create Product
class ProductViewSet(ModelViewSet):

    permission_classes = [ProductPermission]

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

    pagination_class = ProductPagination



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


def group_required(*group_names):
    def check_group(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=group_names).exists()
    return user_passes_test(check_group, login_url='login')


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_page')
        error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def paginate(request, queryset, page_size=10):
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(page_number)


@group_required('Admin', 'Manager', 'Sales Staff')
def dashboard_page(request):
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
    low_stock = Product.objects.filter(quantity__lt=10, quantity__gt=0).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    return render(request, 'dashboard.html', {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock,
        'out_of_stock_products': out_of_stock,
    })


@group_required('Admin', 'Manager', 'Sales Staff')
def products_page(request):
    query = request.GET.get('q', '')
    products = Product.objects.select_related('category', 'supplier').all()
    if query:
        products = products.filter(name__icontains=query)
    page_obj = paginate(request, products)
    return render(request, 'products.html', {
        'page_obj': page_obj,
        'query': query,
    })


@group_required('Admin', 'Manager')
def product_add(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('products_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Product',
        'cancel_url': '/products/',
    })


@group_required('Admin', 'Manager')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit Product: {product.name}',
        'cancel_url': '/products/',
    })


@group_required('Admin')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products_page')
    return render(request, 'confirm_delete.html', {
        'object_name': product.name,
        'cancel_url': '/products/',
    })


@group_required('Admin', 'Manager')
def categories_page(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    page_obj = paginate(request, categories)
    return render(request, 'categories.html', {
        'page_obj': page_obj,
        'query': query,
    })


@group_required('Admin')
def category_add(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('categories_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Category',
        'cancel_url': '/categories/',
    })


@group_required('Admin')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('categories_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit Category: {category.name}',
        'cancel_url': '/categories/',
    })


@group_required('Admin')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories_page')
    return render(request, 'confirm_delete.html', {
        'object_name': category.name,
        'cancel_url': '/categories/',
    })


@group_required('Admin', 'Manager')
def suppliers_page(request):
    query = request.GET.get('q', '')
    suppliers = Supplier.objects.all()
    if query:
        suppliers = suppliers.filter(name__icontains=query)
    page_obj = paginate(request, suppliers)
    return render(request, 'suppliers.html', {
        'page_obj': page_obj,
        'query': query,
    })


@group_required('Admin', 'Manager')
def supplier_add(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('suppliers_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Supplier',
        'cancel_url': '/suppliers/',
    })


@group_required('Admin', 'Manager')
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('suppliers_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit Supplier: {supplier.name}',
        'cancel_url': '/suppliers/',
    })


@group_required('Admin', 'Manager')
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers_page')
    return render(request, 'confirm_delete.html', {
        'object_name': supplier.name,
        'cancel_url': '/suppliers/',
    })


@group_required('Admin', 'Manager', 'Sales Staff')
def customers_page(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(name__icontains=query)
    page_obj = paginate(request, customers)
    return render(request, 'customers.html', {
        'page_obj': page_obj,
        'query': query,
    })


@group_required('Admin', 'Manager', 'Sales Staff')
def customer_add(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('customers_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Customer',
        'cancel_url': '/customers/',
    })


@group_required('Admin', 'Manager')
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customers_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit Customer: {customer.name}',
        'cancel_url': '/customers/',
    })


@group_required('Admin')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers_page')
    return render(request, 'confirm_delete.html', {
        'object_name': customer.name,
        'cancel_url': '/customers/',
    })


@group_required('Admin', 'Manager', 'Sales Staff')
def sales_page(request):
    query = request.GET.get('q', '')
    sales = Sale.objects.select_related('product', 'customer').all()
    if query:
        sales = sales.filter(product__name__icontains=query)
    page_obj = paginate(request, sales)
    return render(request, 'sales.html', {
        'page_obj': page_obj,
        'query': query,
    })


@group_required('Admin', 'Manager', 'Sales Staff')
def sale_add(request):
    form = SaleForm(request.POST or None)
    if form.is_valid():
        sale = form.save(commit=False)
        product = sale.product
        if sale.quantity > product.quantity:
            form.add_error('quantity', 'Not enough stock available.')
        else:
            with transaction.atomic():
                product.quantity -= sale.quantity
                product.save()
                sale.selling_price = sale.selling_price or product.selling_price
                sale.save()
            return redirect('sales_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Record Sale',
        'cancel_url': '/sales/',
    })


@group_required('Admin', 'Manager')
def sale_edit(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    previous_quantity = sale.quantity
    previous_product = sale.product
    form = SaleForm(request.POST or None, instance=sale)
    if form.is_valid():
        with transaction.atomic():
            updated_sale = form.save(commit=False)
            product = updated_sale.product
            new_quantity = updated_sale.quantity

            if previous_product == product:
                quantity_diff = new_quantity - previous_quantity
                if quantity_diff > 0 and quantity_diff > product.quantity:
                    form.add_error('quantity', 'Not enough stock available.')
                else:
                    product.quantity -= quantity_diff
                    product.save()
                    updated_sale.save()
                    return redirect('sales_page')
            else:
                if new_quantity > product.quantity:
                    form.add_error('quantity', 'Not enough stock available.')
                else:
                    previous_product.quantity += previous_quantity
                    previous_product.save()
                    product.quantity -= new_quantity
                    product.save()
                    updated_sale.save()
                    return redirect('sales_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit Sale: {sale}',
        'cancel_url': '/sales/',
    })


@group_required('Admin')
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        with transaction.atomic():
            sale.product.quantity += sale.quantity
            sale.product.save()
            sale.delete()
        return redirect('sales_page')
    return render(request, 'confirm_delete.html', {
        'object_name': str(sale),
        'cancel_url': '/sales/',
    })


@group_required('Admin')
def users_page(request):
    users = User.objects.order_by('username')
    page_obj = paginate(request, users)
    return render(request, 'users.html', {'page_obj': page_obj})


@group_required('Admin')
def user_add(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users_page')
    return render(request, 'form.html', {
        'form': form,
        'title': 'Add User',
        'cancel_url': '/users/',
    })


@group_required('Admin')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('users_page')
    return render(request, 'form.html', {
        'form': form,
        'title': f'Edit User: {user.username}',
        'cancel_url': '/users/',
    })


@group_required('Admin')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users_page')
    return render(request, 'confirm_delete.html', {
        'object_name': user.username,
        'cancel_url': '/users/',
    })


@group_required('Admin', 'Manager')
def reports_page(request):
    revenue_by_category = (
        Product.objects
        .values('category__name')
        .annotate(total_sales=Sum(F('sales__quantity') * F('sales__selling_price')))
        .order_by('-total_sales')
    )
    return render(request, 'reports.html', {
        'revenue_by_category': revenue_by_category,
    })
