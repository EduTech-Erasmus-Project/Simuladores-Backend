# Generated by Django 3.2.7 on 2022-05-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0015_delete_asignacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercitario',
            name='sector',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ejercitario',
            name='categoria',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
