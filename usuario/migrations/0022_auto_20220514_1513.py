# Generated by Django 3.2.7 on 2022-05-14 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0021_auto_20220514_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluador',
            name='codigoEvaluador',
            field=models.CharField(default='6GwZhb', max_length=6),
        ),
        migrations.AlterField(
            model_name='participante',
            name='codigoEstudiante',
            field=models.CharField(default='4FtAFo', max_length=6),
        ),
    ]