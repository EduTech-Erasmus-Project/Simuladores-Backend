# Generated by Django 3.2.7 on 2022-01-14 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0018_gradodiscapacidadparticipante'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscapacidadParticipante',
            fields=[
                ('idGradoDeDiscapacidad', models.AutoField(primary_key=True, serialize=False)),
                ('gradoDeDiscapacidad', models.PositiveIntegerField(default=0, null=True)),
                ('discapacidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TipoDiscapacidad', to='SimuladoresLaboralesApi.discapacidad')),
                ('participante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DiscapacidadParticipante', to='SimuladoresLaboralesApi.participante')),
            ],
        ),
        migrations.DeleteModel(
            name='GradoDiscapacidadParticipante',
        ),
    ]
