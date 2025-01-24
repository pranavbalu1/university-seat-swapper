from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token, create_or_update_profile, get_profile, add_class, get_classes
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore


schema_view = get_schema_view(
    openapi.Info(
        title="Student API",
        default_version="v1",
        description="API documentation for the Student App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/login/', login, name='login'),
    path('api/register/', register, name='register'),
    path('api/test_token/', test_token, name='test_token'),
    path('api/profile/', create_or_update_profile, name='create_or_update_profile'),
    path('api/get_profile/', get_profile, name='get_profile'),
    path('api/add_class/', add_class, name='add_class'),
    path('api/get_classes/', get_classes, name='get_classes'),

]