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


#Clases para serealizar desde dentro de la apliacion ModelSerializer
class ParticipanteSerializerObjects(serializers.ModelSerializer): 
    class Meta: 
        model = Participante
        fields = '__all__'
 
class ExperienciaLaboralSerializerObjects(serializers.ModelSerializer):
    class Meta: 
        model = ExperienciaLaboral
        fields ='__all__'
    