# Generated by Django 3.2.7 on 2022-05-15 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0023_auto_20220514_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluador',
            name='codigoEvaluador',
            field=models.CharField(default='3BQ59Y', max_length=6),
        ),
        migrations.AlterField(
            model_name='participante',
            name='codigoEstudiante',
            field=models.CharField(default='3wenmw', max_length=6),
        ),
    ]
