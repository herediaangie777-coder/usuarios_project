from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_sesion_arbitro"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipo",
            name="horas_juego",
            field=models.CharField(blank=True, default="0", max_length=50),
        ),
    ]
