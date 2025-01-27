from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token
from .views import create_or_update_profile, get_profile, add_class, remove_class, get_classes, create_trade_request, upvote_request, downvote_request, favorite_request, accept_trade_request, get_trade_requests, remove_trade_request, mark_request_accepted
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

    # Classes
    path('api/profile/add_class/', add_class, name='add_class'),
    path('api/profile/remove_class/', remove_class, name='remove_class'),
    path('api/profile/get_classes/', get_classes, name='get_classes'),

    # Trade Requests
    path('api/class_trade/create/', create_trade_request, name='create_trade_request'),
    path('api/class_trade/upvote/<int:trade_request_id>/', upvote_request, name='upvote_request'),
    path('api/class_trade/downvote/<int:trade_request_id>/', downvote_request, name='downvote_request'),
    path('api/class_trade/favorite/<int:trade_request_id>/', favorite_request, name='favorite_request'),
    path('api/class_trade/accept/<int:trade_request_id>/', accept_trade_request, name='accept_trade_request'),
    path('api/class_trade/', get_trade_requests, name='get_trade_requests'),
    path('api/class_trade/remove/<int:trade_request_id>/', remove_trade_request, name='remove_trade_request'),
    path('api/class_trade/mark_accepted/<int:trade_request_id>/', mark_request_accepted, name='mark_request_accepted'),
]

