# Generated by Django 3.2.7 on 2022-05-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0036_auto_20220524_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='ref',
            field=models.CharField(default='KWY4Mi4MG8ANDbaGW8V8BVKoizGE6cXiy92w3b2rYYo4pmKtQ3djTMbHaacrCjZX', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='codigo',
            field=models.CharField(default='YdHL5r', max_length=6),
        ),
    ]