# Generated by Django 3.2.7 on 2022-05-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0011_auto_20220512_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluador',
            name='codigoEvaluador',
            field=models.CharField(default='3eQY4A', max_length=6),
        ),
        migrations.AlterField(
            model_name='participante',
            name='codigoEstudiante',
            field=models.CharField(default='36CqQY', max_length=6),
        ),
    ]
