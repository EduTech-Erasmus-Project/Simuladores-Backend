from rest_framework import serializers
from SimuladoresLaboralesApi.serializers import UsuarioSerializer


from usuario.models import Usuario, Participante, Evaluador



class EvaluadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Evaluador
        fields = '__all__'


