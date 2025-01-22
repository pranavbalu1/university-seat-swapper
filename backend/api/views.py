from rest_framework import viewsets
from .models import Class, SeatExchange
from .serializers import ClassSerializer, SeatExchangeSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class SeatExchangeViewSet(viewsets.ModelViewSet):
    queryset = SeatExchange.objects.all()
    serializer_class = SeatExchangeSerializer
