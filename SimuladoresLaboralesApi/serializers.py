from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usuario.models import Usuario
from .models import *


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'


class EvaluadorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Evaluador
        fields = '__all__'


class ExperienciaLaboralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'


''' 
class SesionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'
'''


class EjercitarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ejercitario
        fields = '__all__'


class ActividadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'


''' 
class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'
'''


class ComentarioSerializerObjects(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


''' 
class RespuestaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'
'''


class DiscapacidadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discapacidad
        fields = '__all__'


class GradoDiscapacidadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiscapacidadParticipante
        fields = '__all__'

    # Clases para serealizar desde dentro de la apliacion ModelSerializer


class ParticipanteSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'


# Clases para serealizar desde dentro de la apliacion ModelSerializer
class RegistroParticipanteSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = (
            'id', 'email', 'password', 'nombre', 'apellido', 'fechaNacimiento', 'genero'
        )


class ParticipanteSerializerObjectsSinCorreo(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = (
            'id', 'password', 'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios'
            , 'codigoEstudiante', 'nivelDeFormacion', 'responsable'
        )


class ParticipanteSerializerObjectsNOPassword(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = (
            'id', 'email', 'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios'
            , 'codigoEstudiante', 'nivelDeFormacion', 'responsable'
        )


class EvaluadorSerializerObjectsNOPassword(serializers.ModelSerializer):
    class Meta:
        model = Evaluador
        fields = (
            'id', 'email', 'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'nivelDeFormacion'
        )


class ExperienciaLaboralSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'


class RegistroEvaluadorSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Evaluador
        fields = (
            'email', 'password', 'nombre', 'apellido', 'fechaNacimiento', 'genero'
        )


class EvaluadorSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Evaluador
        fields = '__all__'


''' 
class asignacionSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'
'''


class nuevaActividadUnitySerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'


class nuevaPreguntaUnitySerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'


class PreguntaTotal(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ('id', 'contenido', 'respuestaCorrecta', 'numeroPregunta', 'preguntaDelEjercitario')


class PreguntaEjercitarioSerializer(serializers.ModelSerializer):
    pregunta = PreguntaTotal()

    class Meta:
        model = Pregunta
        fields = '__all__'

class EjercitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercitario
        fields = '__all__'

    def to_representation(self, instance):
        if self.context.tipoUser is not None and self.context.tipoUser == 'participante':
            try:
                # print("user in serializer", instance["id"])
                actividad = Actividad.objects.filter(ejercitario_id=instance["id"],
                                                     participante__usuario_id=self.context.id).order_by(
                    "-fecha").first()
                total = actividad.calificacion  # round((actividad.calificacion * 100) / actividad.totalPreguntas, 2)
                instance["progreso"] = total
            except Exception as e:
                instance["progreso"] = 0
        return instance


class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ('id', 'titulo', 'descripcion')

    def to_representation(self, instance):
        try:
            ejercitariosN1 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel1").values()
            ejercitariosN2 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel2").values()
            ejercitariosN3 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel3").values()
            serializer1 = EjercitarioSerializer(ejercitariosN1, many=True, context=self.context['request'].user)
            serializer2 = EjercitarioSerializer(ejercitariosN2, many=True, context=self.context['request'].user)
            serializer3 = EjercitarioSerializer(ejercitariosN3, many=True, context=self.context['request'].user)
        except Exception as e:
            print(e)
            return {}

        return {
            "id": instance.id,
            "titulo": instance.titulo,
            "descripcion": instance.descripcion,
            "niveles": [
                {
                    "name": "Nivel 1",
                    "value": "Nivel1",
                    "ejercitarios": serializer1.data,
                    "status": True

                },
                {
                    "name": "Nivel 2",
                    "value": "Nivel2",
                    "ejercitarios": serializer2.data,
                    "status": True if self.context['request'].user.tipoUser == 'evaluador' else self.calculate(
                        serializer1)
                    # sum(item['progreso'] for item in serializer1.data) / len(serializer1.data) == 100
                },
                {
                    "name": "Nivel 3",
                    "value": "Nivel3",
                    "ejercitarios": serializer3.data,
                    "status": True if self.context['request'].user.tipoUser == 'evaluador' else self.calculate(
                        serializer2)
                    # sum(item['progreso'] for item in serializer2.data) / len(serializer2.data) == 100
                },
            ]
        }

    def calculate(self, serializer):
        if len(serializer.data) == 0:
            return False
        else:
            sum(item['progreso'] for item in serializer.data) / len(serializer.data) == 100


class CompetenciaTotal(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = '__all__'

class RubricaTotal(serializers.ModelSerializer):
    class Meta:
        model = Rubrica
        fields = ('id','calificacion', 'indicador', 'ejercitario_id')

class EjercitarioCompetenciaSerializer(serializers.ModelSerializer):
    competencia = CompetenciaTotal()

    class Meta:
        model = Ejercitario
        fields = '__all__'


class UsuarioListaSerializer(serializers.ModelSerializer):
    usuario = CompetenciaTotal()

    class Meta:
        model = Ejercitario
        fields = '__all__'


class EjercitarioSerializerObjects(serializers.ModelSerializer):
    competencia = CompetenciaSerializer()

    class Meta:
        model = Ejercitario
        fields = '__all__'


class AtributoGeneroSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ('genero')


class ComentarioSerializerObjectsModel(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


# Clases para serealizar desde dentro de la apliacion ModelSerializer
class DiscapacidadParticipanteSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = DiscapacidadParticipante
        fields = '__all__'


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField(max_length=7, write_only=True)

    class Meta:
        model = Usuario
        fields = ("email", "nombre", "apellido", "password", "fechaNacimiento", "genero", "role", "institucion")

    def create(self, validated_data):
        if validated_data["role"] == 'user':
            del validated_data["role"]
            user = Usuario.objects.create_user(**validated_data)
            return user
        elif validated_data["role"] == 'expert':
            del validated_data["role"]
            user = Usuario.objects.create_expert(**validated_data)
            return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id", "email", "nombre", "apellido", "img", "tipoUser", 'codigo')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios',
            'nivelDeFormacion', 'codigo', 'estado', 'last_login', 'tipoUser', 'img'
        )


class ParticipanteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Participante
        fields = '__all__'


class EvaluadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Evaluador
        fields = '__all__'


'''
class AsignacionUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'
'''
''' 
class ActividadSerialize(serializers.ModelSerializer):
    participante = ParticipanteSerializer()

    class Meta:
        model = Actividad
        fields = '__all__'
'''


class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = '__all__'

class DiscapacidadParticipanteSerializer(serializers.ModelSerializer):
    discapacidad = DiscapacidadSerializer()

    class Meta:
        model = DiscapacidadParticipante
        fields = ('id', 'gradoDeDiscapacidad', 'discapacidad')


class ParticipanteSerializerDiscapacidad(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    DiscapacidadParticipante = DiscapacidadParticipanteSerializer(many=True)

    class Meta:
        model = Participante
        fields = ('id', 'usuario', 'DiscapacidadParticipante')


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

    def to_representation(self, instance):
        rubrica = Rubrica.objects.filter(ejercitario_id=instance.ejercitario.id).values()

        if instance.calificacion >= 0 and instance.calificacion < 25:
            rubrica = list(filter(lambda d: d['calificacion'] == 25, rubrica))[0]

        if instance.calificacion >= 25 and instance.calificacion < 50:
            rubrica = list(filter(lambda d: d['calificacion'] == 50, rubrica))[0]

        if instance.calificacion >= 50 and instance.calificacion < 75:
            rubrica = list(filter(lambda d: d['calificacion'] == 75, rubrica))[0]

        if instance.calificacion >= 75 and instance.calificacion <= 100:
            rubrica = list(filter(lambda d: d['calificacion'] == 100, rubrica))[0]

        print("id", rubrica)
        print("instance", instance)
        print("data", model_to_dict(instance))

        data = {
            "actividad": model_to_dict(instance),
            "rubrica": rubrica,
        }
        print(data)

        return data


class UsuarioCalificacionGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellido', 'genero'
        )

    def to_representation(self, instance):
        nivel = 0
        tiempo = 0
        progreso = 0
        participante = Participante.objects.get(usuario_id=instance.id)
        nivel1 = Actividad.objects.filter(participante_id=participante.id, ejercitario__nivel="Nivel1").order_by(
            "-id").values()
        nivel2 = Actividad.objects.filter(participante_id=participante.id, ejercitario__nivel="Nivel2").order_by(
            "-id").values()
        nivel3 = Actividad.objects.filter(participante_id=participante.id, ejercitario__nivel="Nivel3").order_by(
            "-id").values()

        if len(nivel1) > 0:
            nivel = 1
            tiempo = round(sum(item['tiempoTotal'] for item in nivel1) / len(nivel1), 2)
            progreso += nivel1[0]["calificacion"]
        if len(nivel2) > 0:
            nivel = 2
            tiempo = round(sum(item['tiempoTotal'] for item in nivel2) / len(nivel2), 2)
            progreso += nivel2[0]["calificacion"]
        if len(nivel3) > 0:
            nivel = 3
            tiempo = round(sum(item['tiempoTotal'] for item in nivel3) / len(nivel3), 2)
            progreso += nivel3[0]["calificacion"]

        # nivel*100/3
        return {
            "id": participante.id,
            "usuario": {
                'id': instance.id,
                'email': instance.email,
                'nombre': instance.nombre,
                'apellido': instance.apellido,
                'genero': instance.genero,
                'codigo': instance.codigo
            },
            "progreso": round(progreso / 3, 2),
            "nivel": 1 if nivel == 0 else nivel,
            "tiempo": tiempo,
        }


class ParticipanteSerializerList(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Participante
        fields = ('id', 'usuario', 'razon')


class ComentarioSerializer(serializers.ModelSerializer):
    participante = ParticipanteSerializer()
    evaluador = EvaluadorSerializer()

    class Meta:
        model = Comentario
        fields = '__all__'


class ParticipanteLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ('id', 'ref', 'evaluador',)


class PerfilSerializers(serializers.ModelSerializer):
    # discapacidades = DiscapacidadParticipante
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios',
            'nivelDeFormacion', 'codigo', 'tipoUser', 'institucion',
        )


class ActualizarPerfilSerializers(serializers.ModelSerializer):
    # discapacidades = DiscapacidadParticipante
    class Meta:
        model = Usuario
        fields = (
            'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios',
            'nivelDeFormacion','institucion',
        )


class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def to_representation(self, instance):
        user = self.context['request'].user
        preguntaCorrecta = Pregunta.objects.get(preguntaDelEjercitario_id=instance.preguntaDeLaActividad.ejercitario.id,
                                                numeroPregunta=instance.numeroPregunta)

        data = {
            "respuesta": {
                "id": instance.id,
                "numeroPregunta": instance.numeroPregunta,
                "respuestaIngresada": instance.respuestaIngresada,
                "tiempoRespuesta": instance.tiempoRespuesta,
                "correcto": instance.respuestaIngresada == preguntaCorrecta.respuestaCorrecta,
            },
            "respuesta_correcta": {
                "contenido": preguntaCorrecta.contenido,
                "numeroPregunta": preguntaCorrecta.numeroPregunta
            }
        }

        if user.tipoUser == "evaluador":
            data["respuesta_correcta"]["respuestaCorrecta"] = preguntaCorrecta.respuestaCorrecta

        return data


class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = '__all__'
