from rest_framework import serializers

from ..models import (
    Usuario,
    Atleta,
    Arbitro,
    EquipoJuego,
    Juego,
    Plataforma,
    Trofeo,
    Consola,
    Control,
    SesionEntrenamiento,
    Telefono,
    RedSocial,
)


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ["id", "numero", "tipo"]
        read_only_fields = ["id"]


class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = ["id", "plataforma", "usuario_red"]
        read_only_fields = ["id"]


class UsuarioMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nombre_completo", "username"]
        read_only_fields = ["id", "nombre_completo", "username"]


class AtletaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = ["id", "nombre_completo", "username"]
        read_only_fields = ["id", "nombre_completo", "username"]


class EquipoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoJuego
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = ["id", "nombre", "marca"]
        read_only_fields = ["id"]


class JuegoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class TrofeoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trofeo
        fields = ["id", "nombre", "puntos"]
        read_only_fields = ["id", "nombre", "puntos"]


class UsuarioBaseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "codigo",
            "tipo_documento",
            "numero_documento",
            "nombre_completo",
            "edad",
            "sexo",
            "direccion",
            "username",
            "password",
            "tipo_usuario",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "codigo", "created_at", "updated_at"]


class UsuarioSerializer(UsuarioBaseSerializer):
    telefonos = TelefonoSerializer(many=True, required=False)
    redes = RedSocialSerializer(many=True, required=False)

    class Meta(UsuarioBaseSerializer.Meta):
        model = Usuario
        fields = UsuarioBaseSerializer.Meta.fields + ["telefonos", "redes"]

    def validate(self, attrs):
        instance = self.instance
        numero_documento = attrs.get("numero_documento")
        username = attrs.get("username")

        if numero_documento:
            qs = Usuario.objects.filter(numero_documento=numero_documento)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"numero_documento": "El numero de documento ya existe."}
                )

        if username:
            qs = Usuario.objects.filter(username=username)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"username": "El username ya existe."})

        return attrs


class AtletaSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        model = Atleta
        fields = UsuarioBaseSerializer.Meta.fields + ["puntos_experiencia"]
        read_only_fields = UsuarioBaseSerializer.Meta.read_only_fields + [
            "puntos_experiencia"
        ]


class ArbitroSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        model = Arbitro
        fields = UsuarioBaseSerializer.Meta.fields


class EquipoJuegoSerializer(serializers.ModelSerializer):
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


class TrofeoSerializer(serializers.ModelSerializer):
    juego_detalle = JuegoMiniSerializer(source="juego", read_only=True)
    usuarios = UsuarioMiniSerializer(many=True, read_only=True)
    equipos = EquipoMiniSerializer(many=True, read_only=True)

    usuarios_ids = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), many=True, write_only=True, required=False
    )
    equipos_ids = serializers.PrimaryKeyRelatedField(
        queryset=EquipoJuego.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Trofeo
        fields = [
            "id",
            "nombre",
            "puntos",
            "juego",
            "juego_detalle",
            "usuarios",
            "equipos",
            "usuarios_ids",
            "equipos_ids",
        ]
        read_only_fields = ["id"]


class ConsolaSerializer(serializers.ModelSerializer):
    plataforma_detalle = PlataformaSerializer(source="plataforma", read_only=True)

    class Meta:
        model = Consola
        fields = [
            "id",
            "numero_serie",
            "nombre",
            "total_existentes",
            "ip",
            "mac_lan",
            "mac_wifi",
            "total_controles",
            "plataforma",
            "plataforma_detalle",
        ]
        read_only_fields = ["id"]


class ControlSerializer(serializers.ModelSerializer):
    plataforma_detalle = PlataformaSerializer(source="plataforma", read_only=True)

    class Meta:
        model = Control
        fields = ["id", "numero_serie", "tipo", "plataforma", "plataforma_detalle"]
        read_only_fields = ["id"]


class SesionEntrenamientoSerializer(serializers.ModelSerializer):
    juego_detalle = JuegoMiniSerializer(source="juego", read_only=True)
    arbitro_detalle = UsuarioMiniSerializer(source="arbitro", read_only=True)
    atleta_detalle = AtletaMiniSerializer(source="atleta", read_only=True)
    equipo_detalle = EquipoMiniSerializer(source="equipo", read_only=True)

    class Meta:
        model = SesionEntrenamiento
        fields = [
            "id",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "estado",
            "puntos_experiencia",
            "juego",
            "juego_detalle",
            "arbitro",
            "arbitro_detalle",
            "atleta",
            "atleta_detalle",
            "equipo",
            "equipo_detalle",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        atleta = attrs.get("atleta")
        equipo = attrs.get("equipo")

        if atleta and equipo:
            raise serializers.ValidationError(
                "Solo puede haber atleta o equipo, no ambos."
            )
        if not atleta and not equipo:
            raise serializers.ValidationError("Debe asignar un atleta o un equipo.")

        return attrs


class PlataformaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class ControlMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ["id", "numero_serie", "tipo"]
        read_only_fields = ["id", "numero_serie", "tipo"]
