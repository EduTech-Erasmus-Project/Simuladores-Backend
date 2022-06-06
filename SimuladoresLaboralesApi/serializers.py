from dataclasses import field
from msilib.schema import Class
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from usuario.models import Usuario, Participante, Evaluador
from .models import *


class ParticipanteSerializer(serializers.HyperlinkedModelSerializer):
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


class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class ComentarioSerializerObjects(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class RespuestaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'


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


class EjercitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercitario
        fields = '__all__'

    def to_representation(self, instance):
        if self.context.tipoUser is not None and self.context.tipoUser == 'participante':
            try:
                #print("user in serializer", instance["id"])
                actividad = Actividad.objects.filter(ejercitario_id=instance["id"],
                                                     participante__usuario_id=self.context.id).order_by(
                    "-fecha").first()
                total = round((actividad.calificacion * 100) / actividad.totalPreguntas, 2)
                instance["progreso"] = total
            except Exception as e:
                instance["progreso"] = 0
        return instance


class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ('id', 'titulo', 'descripcion')

    def to_representation(self, instance):
        ejercitariosN1 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel1").values()
        ejercitariosN2 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel2").values()
        ejercitariosN3 = Ejercitario.objects.filter(competencia_id=instance.id, nivel="Nivel3").values()

        serializer1 = EjercitarioSerializer(ejercitariosN1, many=True, context=self.context['request'].user)
        serializer2 = EjercitarioSerializer(ejercitariosN2, many=True, context=self.context['request'].user)
        serializer3 = EjercitarioSerializer(ejercitariosN3, many=True, context=self.context['request'].user)

        return {
            "id": instance.id,
            "titulo": instance.titulo,
            "descripcion": instance.descripcion,
            "niveles": [
                {
                    "name": "Nivel 1",
                    "value": "Nivel1",
                    "ejercitarios": serializer1.data
                },
                {
                    "name": "Nivel 2",
                    "value": "Nivel2",
                    "ejercitarios": serializer2.data
                },
                {
                    "name": "Nivel 3",
                    "value": "Nivel3",
                    "ejercitarios": serializer3.data
                },
            ]

        }

class CompetenciaTotal(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ('id', 'titulo', 'descripcion')

class EjercitarioCompetenciaSerializer(serializers.ModelSerializer):
    competencia = CompetenciaTotal()
    class Meta:
        model =Ejercitario
        fields = '__all__'

class UsuarioListaSerializer(serializers.ModelSerializer):
    usuario = CompetenciaTotal()
    class Meta:
        model =Ejercitario
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
        fields = ("email", "nombre", "apellido", "password", "fechaNacimiento", "genero", "role")

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
            'nivelDeFormacion', 'codigo', 'estado','last_login','tipoUser'
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
        fields = ('__all__')



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


class UsuarioCalificacionGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellido', 'genero'
        )

    def to_representation(self, instance):
        participante = Participante.objects.get(usuario_id=instance.id)
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
            "calificacion": 0,
            "tiempo": 0,
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
            'nivelDeFormacion', 'codigo', 'tipoUser',
        )


class ActualizarPerfilSerializers(serializers.ModelSerializer):
    # discapacidades = DiscapacidadParticipante
    class Meta:
        model = Usuario
        fields = (
            'nombre', 'apellido', 'telefono', 'pais', 'ciudad', 'direccion', 'fechaNacimiento'
            , 'carreraUniversitaria', 'genero', 'numeroDeHijos', 'estadoCivil', 'etnia', 'estudiosPrevios',
            'nivelDeFormacion',
        )
