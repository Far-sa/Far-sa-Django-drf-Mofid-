from django.db import connection
from drf_spectacular.utils import extend_schema
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sqlparse import format

from .models import Category, Product, ProductImage, ProductLine
from .serializers import (
    CategorySerializer,
    ProductCategorySerializer,
    ProductSerializer,
)

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset
    """

    queryset = Category.objects.all().is_active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset
    """

    #! Custom model manager
    # queryset = Product.isactive.all()
    # queryset = Product.objects.isactive()

    queryset = Product.objects.all()
    lookup_field = "slug"

    def retrieve(self, request, pk=None, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .select_related("category")
            .prefetch_related("product_line")
            .prefetch_related("product_line__product_image")
            .prefetch_related("product_line__attribute_value__attribute"),
            many=True,
        )
        data = Response(serializer.data)

        #! parse query
        # x = self.queryset.filter(slug=slug)
        # sqlformatted = format(str(x.query), reindent=True)
        # print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))
        # return x

        #! count simple query
        q = list(connection.queries)
        print(len(q))
        for qs in q:
            sqlformatted = format(str(qs["sql"]), reindent=True)
            print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return data

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An Endpoint to return Products by Category
        """
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                "product_line", queryset=ProductLine.objects.order_by("order")
            )
            .prefetch_related(
                "product_line__product_image",
                queryset=ProductImage.objects.filter("order=1"),
            ),
            many=True,
        )
        return Response(serializer.data)

    # def list_product_by_category(self, request, category=None):
    #     """
    #     An Endpoint to return Products by Category
    #     """
    #     serializer = ProductSerializer(
    #         self.queryset.filter(category__name=category), many=True
    #     )
    #     return Response(serializer.data)
