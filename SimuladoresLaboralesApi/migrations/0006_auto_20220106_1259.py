# Generated by Django 3.2.7 on 2022-01-06 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0005_auto_20220105_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejercitario',
            name='asignacion',
        ),
        migrations.AddField(
            model_name='asignacion',
            name='ejercitario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AsignacionEjercitario', to='SimuladoresLaboralesApi.ejercitario'),
        ),
    ]