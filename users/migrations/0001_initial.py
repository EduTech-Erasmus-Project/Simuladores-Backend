# Generated by Django 3.2.6 on 2021-09-27 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nick', models.CharField(max_length=15)),
                ('clave', models.CharField(max_length=12)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=10)),
            ],
        ),
    ]
