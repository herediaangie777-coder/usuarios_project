import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_remove_equipo_horas_juego_remove_equipo_juego_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="nivel",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="equipo",
            name="juego",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="equipo",
            name="puntos_experiencia",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="equipo",
            name="trofeos",
            field=models.ManyToManyField(blank=True, related_name="equipos", to="api.trofeo"),
        ),
        migrations.AddField(
            model_name="equipo",
            name="usuarios",
            field=models.ManyToManyField(blank=True, related_name="equipos", to="api.atleta"),
        ),
        migrations.AlterField(
            model_name="trofeo",
            name="juego",
            field=models.CharField(blank=True, default="General", max_length=100),
        ),
        migrations.AddField(
            model_name="trofeo",
            name="descripcion",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="atleta",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sesiones_entrenamiento", to="api.atleta"),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="equipo",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sesiones_entrenamiento", to="api.equipo"),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="fecha",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="hora_fin",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="hora_inicio",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="juego",
            field=models.CharField(default="Valorant", max_length=100),
        ),
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="puntos_experiencia",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
