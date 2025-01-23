from django.contrib import admin # type: ignore
from django.urls import path, re_path # type: ignore
from .views import login, register, test_token

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login/', login),
    re_path('register/', register),
    re_path('test_token/', test_token),

]
