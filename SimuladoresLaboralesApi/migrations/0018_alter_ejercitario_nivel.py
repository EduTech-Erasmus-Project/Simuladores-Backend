# Generated by Django 3.2.7 on 2022-05-15 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0017_alter_ejercitario_competencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejercitario',
            name='nivel',
            field=models.CharField(blank=True, choices=[('Nivel1', 'Nivel 1'), ('Nivel2', 'NIvel 2'), ('Nivel3', 'NIvel 3')], max_length=7, null=True),
        ),
    ]