# Generated by Django 3.2.7 on 2022-06-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0037_auto_20220526_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='institucion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='participante',
            name='ref',
            field=models.CharField(default='6dNVYbK38V9PnUJe65mqK2PVPFzDUynG5WaXxqgtSLH843Fchib4NywvWJHtkw8t', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='codigo',
            field=models.CharField(default='3SN6BK', max_length=6),
        ),
    ]
