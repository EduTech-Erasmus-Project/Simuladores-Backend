# Generated by Django 3.2.7 on 2022-05-10 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_auto_20220510_1043'),
        ('SimuladoresLaboralesApi', '0004_auto_20220510_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='ActividadDeParticipante',
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='ActividadPorEjercitario',
        ),
        migrations.AddField(
            model_name='actividad',
            name='actividadDeParticipante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividadParticipante', to='usuario.participante'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='actividadPorEjercitario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividadEjercitario', to='SimuladoresLaboralesApi.ejercitario'),
        ),
    ]
