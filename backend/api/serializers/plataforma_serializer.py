from rest_framework import serializers
from api.models.plataforma import Plataforma

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'