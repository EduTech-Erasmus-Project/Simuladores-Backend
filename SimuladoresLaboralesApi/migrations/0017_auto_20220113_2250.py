# Generated by Django 3.2.7 on 2022-01-14 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0016_auto_20220113_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discapacidad',
            name='gradoDeDiscapacidad',
        ),
        migrations.RemoveField(
            model_name='participante',
            name='discapacidad',
        ),
    ]