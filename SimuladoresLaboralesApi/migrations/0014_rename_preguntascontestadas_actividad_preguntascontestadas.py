# Generated by Django 3.2.7 on 2022-05-12 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0013_rename_urlejercitarios_ejercitario_urlejercitario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actividad',
            old_name='PreguntasContestadas',
            new_name='preguntasContestadas',
        ),
    ]