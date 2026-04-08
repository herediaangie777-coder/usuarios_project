from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import AcudienteAtleta, Arbitro, Atleta, Equipo, Telefono, Usuario


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ["id", "numero", "tipo"]
        read_only_fields = ["id"]


class AcudienteAtletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcudienteAtleta
        fields = [
            "nombre_completo",
            "tipo_documento",
            "numero_documento",
            "telefono",
            "parentesco",
            "direccion",
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    telefonos = TelefonoSerializer(many=True, required=False)
    acudiente = AcudienteAtletaSerializer(required=False, allow_null=True, write_only=True)
    equipo_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    equipo_nombre_input = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )
    equipo_nombre = serializers.SerializerMethodField(read_only=True)
    es_menor_edad = serializers.SerializerMethodField(read_only=True)
    puntos_experiencia = serializers.SerializerMethodField(read_only=True)
    acudiente_detalle = serializers.SerializerMethodField(read_only=True)

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
            "nivel",
            "puntos_experiencia",
            "telefonos",
            "equipo_id",
            "equipo_nombre_input",
            "equipo_nombre",
            "es_menor_edad",
            "acudiente",
            "acudiente_detalle",
        ]
        read_only_fields = ["id", "codigo", "nivel", "puntos_experiencia"]
        extra_kwargs = {"password": {"write_only": True}}

    def _get_atleta(self, obj):
        try:
            return obj.atleta
        except Atleta.DoesNotExist:
            return None

    def get_equipo_nombre(self, obj):
        atleta = self._get_atleta(obj)
        if not atleta:
            return None
        equipo = atleta.equipos.order_by("nombre").first()
        return equipo.nombre if equipo else None

    def get_es_menor_edad(self, obj):
        return obj.edad < 18

    def get_puntos_experiencia(self, obj):
        atleta = self._get_atleta(obj)
        return atleta.puntos_experiencia if atleta else 0

    def get_acudiente_detalle(self, obj):
        atleta = self._get_atleta(obj)
        if not atleta:
            return None
        try:
            acudiente = atleta.datos_acudiente
        except AcudienteAtleta.DoesNotExist:
            acudiente = None
        if not acudiente:
            return None
        return AcudienteAtletaSerializer(acudiente).data

    def validate(self, attrs):
        edad = attrs.get("edad", getattr(self.instance, "edad", None))
        acudiente = attrs.get("acudiente")
        tipo_usuario = attrs.get("tipo_usuario") or getattr(self.instance, "tipo_usuario", "atleta")

        if tipo_usuario == "atleta" and edad is not None and edad < 18 and not acudiente:
            raise serializers.ValidationError(
                {"acudiente": "Los atletas menores de edad deben registrar un acudiente."}
            )

        return attrs

    def create(self, validated_data):
        telefonos_data = validated_data.pop("telefonos", [])
        acudiente_data = validated_data.pop("acudiente", None)
        equipo = validated_data.pop("equipo_id", None)
        equipo_nombre_input = validated_data.pop("equipo_nombre_input", "").strip()
        tipo_usuario = validated_data.get("tipo_usuario") or "atleta"
        validated_data["tipo_usuario"] = tipo_usuario
        validated_data["password"] = make_password(validated_data["password"])
        model_class = Arbitro if tipo_usuario == "arbitro" else Atleta
        usuario = model_class.objects.create(**validated_data)
        for telefono in telefonos_data:
            Telefono.objects.create(usuario=usuario, **telefono)
        if tipo_usuario == "atleta" and acudiente_data:
            AcudienteAtleta.objects.create(atleta=usuario, **acudiente_data)
        if tipo_usuario == "atleta" and not equipo and equipo_nombre_input:
            equipo, _ = Equipo.objects.get_or_create(nombre=equipo_nombre_input)
        if tipo_usuario == "atleta" and equipo:
            equipo.usuarios.add(usuario)
        return usuario

    def update(self, instance, validated_data):
        telefonos_data = validated_data.pop("telefonos", None)
        acudiente_data = validated_data.pop("acudiente", None)
        equipo = validated_data.pop("equipo_id", None)
        equipo_nombre_input = validated_data.pop("equipo_nombre_input", "").strip()
        password = validated_data.pop("password", None)
        tipo_usuario = validated_data.get("tipo_usuario", getattr(instance, "tipo_usuario", "atleta"))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = make_password(password)

        instance.save()

        if telefonos_data is not None:
            instance.telefonos.all().delete()
            for telefono in telefonos_data:
                Telefono.objects.create(usuario=instance, **telefono)

        atleta = self._get_atleta(instance)

        if tipo_usuario == "atleta" and atleta and acudiente_data is not None:
            AcudienteAtleta.objects.update_or_create(
                atleta=atleta,
                defaults=acudiente_data,
            )

        if tipo_usuario == "atleta" and atleta and not equipo and equipo_nombre_input:
            equipo, _ = Equipo.objects.get_or_create(nombre=equipo_nombre_input)

        if tipo_usuario == "atleta" and atleta and (equipo is not None or equipo_nombre_input):
            atleta.equipos.clear()
            if equipo:
                equipo.usuarios.add(atleta)

        return instance
