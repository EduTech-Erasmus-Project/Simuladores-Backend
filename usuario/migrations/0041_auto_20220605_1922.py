# Generated by Django 3.2.7 on 2022-06-06 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0040_auto_20220603_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='ref',
            field=models.CharField(default='A3kcYpAPUFRpUhGe7RFz27W5WkXBGry9MdWuy4yXx2GGkkJf4s9yHUwVvCRA3doN', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='codigo',
            field=models.CharField(default='38H2Zt', max_length=6),
        ),
    ]
