from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Brand, Category, Product
from .serializers import BrandSerilazer, CategorySerilazer, ProductSerilazer

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerilazer)
    def list(self, request):
        serializer = CategorySerilazer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset
    """

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerilazer)
    def list(self, request):
        serializer = BrandSerilazer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset
    """

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerilazer)
    def list(self, request):
        serializer = ProductSerilazer(self.queryset, many=True)
        return Response(serializer.data)
