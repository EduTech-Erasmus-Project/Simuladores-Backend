# Generated by Django 3.2.7 on 2022-05-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20220510_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluador',
            name='codigoEvaluador',
            field=models.CharField(default='3ePXWR', max_length=6),
        ),
        migrations.AlterField(
            model_name='participante',
            name='codigoEstudiante',
            field=models.CharField(default='GXikQi', max_length=6),
        ),
    ]
