# Generated by Django 3.2.7 on 2021-12-17 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimuladoresLaboralesApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('idAsignacion', models.AutoField(primary_key=True, serialize=False)),
                ('fechaAsignacion', models.DateTimeField(auto_now=True, null=True)),
                ('evaluador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AsignacionEvaluador', to='SimuladoresLaboralesApi.evaluador')),
                ('participante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AsignacionParticipante', to='SimuladoresLaboralesApi.participante')),
            ],
        ),
        migrations.RenameField(
            model_name='ejercitario',
            old_name='idActividad',
            new_name='idEjercitario',
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='sesionPorActividad',
        ),
        migrations.AddField(
            model_name='actividad',
            name='ActividadDeParticipante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ActividadDelParticipante', to='SimuladoresLaboralesApi.participante'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='fechaDeActividad',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='ActividadPorEjercitario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ActividadEjercitarioID', to='SimuladoresLaboralesApi.ejercitario'),
        ),
        migrations.AlterField(
            model_name='experiencialaboral',
            name='participante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ExperienciaParticipante', to='SimuladoresLaboralesApi.participante'),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='preguntaDeLaActividad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PreguntaDeActividad', to='SimuladoresLaboralesApi.actividad'),
        ),
        migrations.DeleteModel(
            name='Sesion',
        ),
        migrations.AddField(
            model_name='ejercitario',
            name='asignacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EjercitarioAsignacion', to='SimuladoresLaboralesApi.asignacion'),
        ),
    ]
