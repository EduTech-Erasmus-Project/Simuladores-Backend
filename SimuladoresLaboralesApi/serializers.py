from rest_framework import serializers
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
        fields ='__all__'
    
class SesionSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta: 
        model = Asignacion
        fields = '__all__'

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


#Clases para serealizar desde dentro de la apliacion ModelSerializer
class ParticipanteSerializerObjects(serializers.ModelSerializer): 
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
        fields ='__all__'
        
class EvaluadorSerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Evaluador
        fields = '__all__'
        
class asignacionSerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Asignacion
        fields = '__all__'

class nuevaActividadUnitySerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Actividad
        fields = '__all__'
        
class nuevaPreguntaUnitySerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Respuesta
        fields = '__all__'
        
class EjercitarioSerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Ejercitario
        fields = '__all__'   

class AtributoGeneroSerializerObjects(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ('genero')