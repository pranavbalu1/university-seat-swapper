from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token, create_or_update_profile, add_class, get_classes

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login/', login, name='login'),
    re_path('register/', register, name='register'),
    re_path('test_token/', test_token, name='test_token'),
    re_path('profile/', create_or_update_profile, name='create_or_update_profile'),
    re_path('add_class/', add_class, name='add_class'),
    re_path('get_classes/', get_classes, name='get_classes'),
]
