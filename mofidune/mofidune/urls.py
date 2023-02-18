from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from mofidune.product import views

router = DefaultRouter()
router.register("category/", views.CategoryViewSet)
router.register("product/", views.ProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/user/", include("mofidune.users.urls", namespace="users")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # account/login/google
    path("accounts/", include("allauth.urls")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
