# Generated by Django 3.2.7 on 2022-05-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0020_alter_comentario_fechacomentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='calificacionPorcentaje',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
