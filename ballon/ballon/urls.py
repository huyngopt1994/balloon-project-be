"""ballon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django_countries.serializers import CountryFieldMixin
from rest_framework import routers, serializers, viewsets, filters

from web_source.models import Products, Companies, Transactions, TransactionProducts

from ballon import settings


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `highlight` action.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('created_at', 'updated_at', 'name')


class CompanySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__'


class ShortCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = (
            'id', 'name', 'address', 'contact_name'
        )
        read_only_fields = ('name', 'address', 'contact_name')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('created_at', 'updated_at', 'name')


class TransactionProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_id = serializers.IntegerField(source='product.id')

    class Meta:
        model = TransactionProducts
        fields = ('id', 'total', 'price', 'total_price', 'product_id', 'product_name', 'transaction_id')
        read_only_fields = ('product_name', 'id')


class TransactionSerializer(serializers.ModelSerializer):
    company = ShortCompanySerializer(read_only=True)
    company_id = serializers.CharField(source='company.id')
    transaction_products = TransactionProductsSerializer(source='transactionproducts_set', many=True)

    class Meta:
        model = Transactions
        fields = ('id', 'type', 'transport_fee', 'created_at', 'updated_at', 'company',
                  'transaction_products', 'signed_name', 'total_price_before_vat', 'total_price_after_vat',
                  'company_id')

        depth = 1

    def create(self, validated_data):
        transaction_products = validated_data.pop('transactionproducts_set')

        company_instance = Companies.objects.get(pk=int(validated_data['company']['id']))
        validated_data.update({'company': company_instance})
        transaction_instance = Transactions.objects.create(**validated_data)
        for transaction_product in transaction_products:
            product = transaction_product.pop('product')
            product_instance = Products.objects.get(pk=int(product['id']))
            data = {
                'total': transaction_product['total'],
                'price': transaction_product['price'],
                'total_price': transaction_product['total_price'],
                'product': product_instance,
                'transaction': transaction_instance

            }
            TransactionProducts.objects.create(**data)
        return transaction_instance


class TransactionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        company_filter = self.request.query_params.get('company')
        order_filter = self.request.query_params.get('ordering')
        queryset = super(TransactionViewSet, self).get_queryset()
        if company_filter:
            queryset = Transactions.objects.filter(company__name__icontains=company_filter)
        if order_filter:
            queryset = queryset.order_by(order_filter)
        return queryset

    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = ('created_at', 'updated_at')


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'admin/company', CompanyViewSet)
router.register(r'admin/transaction', TransactionViewSet)
urlpatterns = [
                  url(r'^', include(router.urls)),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
