import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_restore_training_flow"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcudienteAtleta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_completo", models.CharField(max_length=150)),
                ("tipo_documento", models.CharField(choices=[("CC", "Cedula"), ("CE", "Cedula extranjeria"), ("TI", "Tarjeta identidad"), ("PAS", "Pasaporte")], max_length=5)),
                ("numero_documento", models.CharField(max_length=30)),
                ("telefono", models.CharField(max_length=30)),
                ("parentesco", models.CharField(max_length=50)),
                ("direccion", models.CharField(blank=True, default="", max_length=200)),
                ("atleta", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="datos_acudiente", to="api.atleta")),
            ],
        ),
    ]
