# Generated by Django 3.2.7 on 2022-07-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0049_auto_20220711_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='ref',
            field=models.CharField(default='DGmQXp6mLRxqjvcnJHgafRfxTf4XTf67GkTaPp3CwDwoXMwYqKRzfdtucjQPFzLx', max_length=64),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='codigo',
            field=models.CharField(default='3ECkKg', max_length=6),
        ),
    ]
