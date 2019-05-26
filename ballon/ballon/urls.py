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
from rest_framework import routers, serializers, viewsets, filters

from web_source.models import Products, Companies, Transactions, TransactionProducts

from ballon import settings


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'description', 'image', 'created_at', 'updated_at')


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


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Companies
        fields = (
            'id', 'name', 'telephone', 'tax_number', 'contact_name', 'address', 'logo', 'created_at', 'updated_at')


class ShortCompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Companies
        fields = (
            'id', 'name'
        )


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('created_at', 'updated_at', 'name')


class TransactionProductsSerializer(serializers.HyperlinkedModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = TransactionProducts
        fields = ('id', 'total', 'price', 'total_price', 'product_id', 'product_name', 'transaction_id')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    company = ShortCompanySerializer()
    transaction_products = TransactionProductsSerializer(source='transactionproducts_set', many=True)

    class Meta:
        model = Transactions
        fields = ('id', 'type', 'transport_fee', 'created_at', 'updated_at', 'company',
                  'transaction_products', 'signed_name', 'total_price_before_vat', 'total_price_after_vat')

        depth = 1


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'admin/company', CompanyViewSet)
router.register(r'admin/transaction', TransactionViewSet)
urlpatterns = [
                  url(r'^', include(router.urls)),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
