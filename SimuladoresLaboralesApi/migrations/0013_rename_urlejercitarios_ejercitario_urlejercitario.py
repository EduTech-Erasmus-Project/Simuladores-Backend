# Generated by Django 3.2.7 on 2022-05-12 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0012_rename_ejercitario_asignacion_competencia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ejercitario',
            old_name='urlEjercitarios',
            new_name='urlEjercitario',
        ),
    ]
