from oeem.models import Ot
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class OtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ot
        fields = ('idn', 'solicita', 'maquina', 'fecha', 'status', 'asignado')