from rest_framework import serializers

from api.models import Juego, Plataforma
from .plataforma_serializer import PlataformaSerializer


class JuegoSerializer(serializers.ModelSerializer):
    plataformas = PlataformaSerializer(many=True, read_only=True)
    plataformas_ids = serializers.PrimaryKeyRelatedField(
        queryset=Plataforma.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Juego
        fields = [
            "id",
            "nombre",
            "clasificacion_esrb",
            "desarrollador",
            "numero_jugadores",
            "tipo",
            "existencias",
            "plataformas",
            "plataformas_ids",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        plataformas = validated_data.pop("plataformas_ids", [])
        juego = Juego.objects.create(**validated_data)
        if plataformas:
            juego.plataformas.add(*plataformas)
        return juego

    def update(self, instance, validated_data):
        plataformas = validated_data.pop("plataformas_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if plataformas is not None:
            instance.plataformas.set(plataformas)
        return instance
