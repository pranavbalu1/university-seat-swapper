from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token, create_or_update_profile, get_profile, add_class, get_classes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login, name='login'),
    path('api/register/', register, name='register'),
    path('api/test_token/', test_token, name='test_token'),
    path('api/profile/', create_or_update_profile, name='create_or_update_profile'),
    path('api/get_profile/', get_profile, name='get_profile'),
    path('api/add_class/', add_class, name='add_class'),
    path('api/get_classes/', get_classes, name='get_classes'),
]