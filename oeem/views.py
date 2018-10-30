from django.shortcuts import render
from rest_framework import viewsets
from oeem.serializer import OtSerializer
from oeem.models import Ot
import datetime

class OtViewSet(viewsets.ModelViewSet):
    queryset = Ot.objects.filter(fecha=datetime.datetime.now())
    serializer_class = OtSerializer


# Create your views here.
