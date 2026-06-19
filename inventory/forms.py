from django import forms
from django.contrib.auth.models import Group, User

from .models import Product, Category, Supplier, Customer, Sale


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'supplier',
            'sku',
            'barcode',
            'description',
            'cost_price',
            'selling_price',
            'quantity',
            'is_active',
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'contact_person',
            'email',
            'phone',
            'address',
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'customer', 'quantity', 'selling_price']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'password', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user
