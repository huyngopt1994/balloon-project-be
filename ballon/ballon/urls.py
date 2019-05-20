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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from web_source.models import Products, Companies, Transactions


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'price', 'name', 'description', 'image')


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `highlight` action.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Companies
        fields = ('id', 'name', 'telephone', 'tax_number', 'contact_name', 'logo', 'created_at', 'updated_at')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer


class TransactionSerizalier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transactions
        fields = ('id', 'total', 'type', 'transport_fee', 'created_at', 'updated_at', 'price')


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerizalier


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'admin/company', CompanyViewSet)
router.register(r'admin/transaction', TransactionViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
]
