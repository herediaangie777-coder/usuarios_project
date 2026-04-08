import uuid

from rest_framework import serializers

from api.models import Arbitro, Atleta, Equipo, SesionEntrenamiento


class SesionEntrenamientoSerializer(serializers.ModelSerializer):
    arbitro_nombre = serializers.CharField(source="arbitro.nombre_completo", read_only=True)
    arbitro_nombre_input = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )
    atleta_nombre = serializers.CharField(source="atleta.nombre_completo", read_only=True)
    equipo_nombre = serializers.CharField(source="equipo.nombre", read_only=True)

    class Meta:
        model = SesionEntrenamiento
        fields = [
            "id",
            "juego",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "arbitro",
            "arbitro_nombre",
            "arbitro_nombre_input",
            "atleta",
            "atleta_nombre",
            "equipo",
            "equipo_nombre",
            "estado",
            "puntos_experiencia",
            "hora_inicio_real",
            "motivo_cancelacion",
        ]
        read_only_fields = [
            "id",
            "estado",
            "puntos_experiencia",
            "hora_inicio_real",
            "motivo_cancelacion",
        ]

    def validate(self, attrs):
        atleta = attrs.get("atleta")
        equipo = attrs.get("equipo")
        arbitro = attrs.get("arbitro")
        arbitro_nombre_input = (attrs.get("arbitro_nombre_input") or "").strip()
        if atleta and equipo:
            raise serializers.ValidationError("Solo puedes asignar atleta o equipo, no ambos.")
        if not atleta and not equipo:
            raise serializers.ValidationError("Debes seleccionar un atleta o un equipo.")
        if not arbitro and not arbitro_nombre_input:
            raise serializers.ValidationError(
                {"arbitro": "Debes seleccionar un arbitro para monitorear la sesion."}
            )

        hora_inicio = attrs.get("hora_inicio")
        hora_fin = attrs.get("hora_fin")
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise serializers.ValidationError(
                {"hora_fin": "La hora final debe ser mayor que la hora inicial."}
            )

        return attrs

    def create(self, validated_data):
        arbitro = validated_data.pop("arbitro", None)
        arbitro_nombre_input = validated_data.pop("arbitro_nombre_input", "").strip()

        if not arbitro and arbitro_nombre_input:
            arbitro = Arbitro.objects.filter(nombre_completo__iexact=arbitro_nombre_input).first()
            if not arbitro:
                suffix = uuid.uuid4().hex[:8]
                arbitro = Arbitro.objects.create(
                    tipo_documento="CC",
                    numero_documento=f"ARB{suffix}".upper(),
                    nombre_completo=arbitro_nombre_input,
                    edad=18,
                    sexo="O",
                    direccion="Pendiente por definir",
                    username=f"arb_{suffix}",
                    password=uuid.uuid4().hex,
                    tipo_usuario="arbitro",
                )

        validated_data["arbitro"] = arbitro
        return SesionEntrenamiento.objects.create(**validated_data)
