from rest_framework import serializers

from api.models import Atleta, EquipoJuego, Juego, Trofeo


class JuegoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class AtletaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = ["id", "nombre_completo", "username"]
        read_only_fields = ["id", "nombre_completo", "username"]


class TrofeoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trofeo
        fields = ["id", "nombre", "puntos"]
        read_only_fields = ["id", "nombre", "puntos"]


class EquipoSerializer(serializers.ModelSerializer):
    juego_detalle = JuegoMiniSerializer(source="juego", read_only=True)
    usuarios = AtletaMiniSerializer(many=True, read_only=True)
    trofeos = TrofeoMiniSerializer(many=True, read_only=True)

    usuarios_ids = serializers.PrimaryKeyRelatedField(
        queryset=Atleta.objects.all(), many=True, write_only=True, required=False
    )
    trofeos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Trofeo.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = EquipoJuego
        fields = [
            "id",
            "nombre",
            "horas_juego",
            "juego",
            "juego_detalle",
            "usuarios",
            "trofeos",
            "usuarios_ids",
            "trofeos_ids",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        usuarios = validated_data.pop("usuarios_ids", [])
        trofeos = validated_data.pop("trofeos_ids", [])
        equipo = EquipoJuego.objects.create(**validated_data)
        if usuarios:
            equipo.usuarios.add(*usuarios)
        if trofeos:
            equipo.trofeos.add(*trofeos)
        return equipo

    def update(self, instance, validated_data):
        usuarios = validated_data.pop("usuarios_ids", None)
        trofeos = validated_data.pop("trofeos_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if usuarios is not None:
            instance.usuarios.set(usuarios)
        if trofeos is not None:
            instance.trofeos.set(trofeos)
        return instance
