# Generated by Django 3.2.7 on 2022-01-13 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0011_auto_20220107_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejercitario',
            name='instruccionesParticipantes',
            field=models.CharField(max_length=1000),
        ),
    ]