# Generated by Django 3.2.7 on 2022-05-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0033_auto_20220522_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='ref',
            field=models.CharField(default='A4fqT8oTHU8S3hBgwpE3VWJbgfSaRFMjDbtvzjkdiGu7MU2kHwAzQ49a4cLP4Hzg', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='codigo',
            field=models.CharField(default='gEmhFF', max_length=6),
        ),
    ]
