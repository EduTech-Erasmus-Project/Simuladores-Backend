# Generated by Django 3.2.7 on 2022-05-24 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0023_remove_actividad_calificacionporcentaje'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubrica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.IntegerField(default=0)),
                ('indicador', models.TextField(blank=True, null=True)),
                ('ejercitario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rubrica_ejercitario', to='SimuladoresLaboralesApi.ejercitario')),
            ],
        ),
    ]
