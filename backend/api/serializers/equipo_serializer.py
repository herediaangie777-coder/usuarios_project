from rest_framework import serializers

from api.models import Atleta, Equipo, Trofeo


class AtletaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = ["id", "nombre_completo", "username"]
        read_only_fields = fields


class TrofeoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trofeo
        fields = ["id", "nombre", "puntos"]
        read_only_fields = fields


class EquipoSerializer(serializers.ModelSerializer):
    usuarios = AtletaMiniSerializer(many=True, read_only=True)
    trofeos = TrofeoMiniSerializer(many=True, read_only=True)
    usuarios_ids = serializers.PrimaryKeyRelatedField(
        queryset=Atleta.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Equipo
        fields = [
            "id",
            "nombre",
            "juego",
            "horas_juego",
            "nivel",
            "puntos_experiencia",
            "usuarios",
            "trofeos",
            "usuarios_ids",
        ]
        read_only_fields = ["id", "nivel", "puntos_experiencia", "trofeos"]

    def create(self, validated_data):
        usuarios = validated_data.pop("usuarios_ids", [])
        equipo = Equipo.objects.create(**validated_data)
        if usuarios:
            equipo.usuarios.set(usuarios)
        return equipo

    def update(self, instance, validated_data):
        usuarios = validated_data.pop("usuarios_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if usuarios is not None:
            instance.usuarios.set(usuarios)
        return instance
