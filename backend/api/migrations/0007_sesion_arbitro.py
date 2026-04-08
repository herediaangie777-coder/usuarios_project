import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_acudienteatleta"),
    ]

    operations = [
        migrations.AddField(
            model_name="sesionentrenamiento",
            name="arbitro",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sesiones_supervisadas", to="api.arbitro"),
        ),
    ]
