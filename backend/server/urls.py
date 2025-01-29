from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token
from .views import create_or_update_profile, get_profile, get_profile_by_user_id, add_class, remove_class, get_classes
from .views import create_class_trade_request, vote_request, toggle_favorite, delete_class_trade_request, list_class_trade_requests, get_all_class_trade_requests, get_favorite_class_trade_requests
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore


schema_view = get_schema_view(
    openapi.Info(
        title="Student API",
        default_version="v1",
        description="API documentation for the Student App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pranavbalu1@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Auth
    path('api/auth/login/', login, name='login'),
    path('api/auth/register/', register, name='register'),
    path('api/auth/test_token/', test_token, name='test_token'),

    # Profile
    path('api/profile/create_or_update_profile/', create_or_update_profile, name='create_or_update_profile'),
    path('api/profile/get_profile/', get_profile, name='get_profile'),
    path('api/profile/get_profile/<int:user_id>/', get_profile_by_user_id, name='get_profile'),

    # Classes
    path('api/profile/add_class/', add_class, name='add_class'),
    path('api/profile/remove_class/', remove_class, name='remove_class'),
    path('api/profile/get_classes/', get_classes, name='get_classes'),

    # Trade Requests
    path('api/class_trade_requests/create_class_trade_request', create_class_trade_request, name='create_class_trade_request'),
    
    path('api/class_trade_requests/<int:request_id>/vote/', vote_request, name='vote_request'),
    path('api/class_trade_requests/<int:request_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('api/class_trade_requests/<int:request_id>/delete/', delete_class_trade_request, name='delete_class_trade_request'),
    
    path('api/class_trade_requests/filtered', list_class_trade_requests, name='list_class_trade_requests'),
    path('api/class_trade_requests/all/', get_all_class_trade_requests, name='get_all_class_trade_requests'),
    path('api/class_trade_requests/favorites/', get_favorite_class_trade_requests, name='get_favorite_class_trade_requests'),

   
]

