# Generated by Django 3.2.7 on 2022-01-14 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0017_auto_20220113_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradoDiscapacidadParticipante',
            fields=[
                ('idGradoDeDiscapacidad', models.AutoField(primary_key=True, serialize=False)),
                ('gradoDeDiscapacidad', models.PositiveIntegerField(default=0, null=True)),
                ('gradoDiscapacidadDiscapacidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GradoDiscapacidadDiscapacidad', to='SimuladoresLaboralesApi.discapacidad')),
                ('gradoDiscapacidadParticipante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GradoDiscapacidadParticipante', to='SimuladoresLaboralesApi.participante')),
            ],
        ),
    ]
