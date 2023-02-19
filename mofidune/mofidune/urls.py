from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from mofidune.product import views

router = DefaultRouter()
router.register("category/", views.CategoryViewSet)
router.register("product/", views.ProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/user/", include("mofidune.users.urls", namespace="users")),
    # account/login/google
    path("accounts/", include("allauth.urls")),
    # path('api/products/', include('products.urls', namespace='products')),
    path("", include("mofidune.order.urls")),
    # path("api/user/payments/", include("payment.urls", namespace="payment")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
