from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, SeatExchangeViewSet

router = DefaultRouter()
router.register(r'classes', ClassViewSet)
router.register(r'seat-exchange', SeatExchangeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
