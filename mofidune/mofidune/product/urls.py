from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet

app_name = "products"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
