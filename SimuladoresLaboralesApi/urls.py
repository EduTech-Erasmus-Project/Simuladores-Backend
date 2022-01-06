# SimuladoresLaboralesApi/urls.py
from django.urls import include, path
from rest_framework import routers
from SimuladoresLaboralesApi import views as views
from SimuladoresLaboralesApi.restful import login as login
from SimuladoresLaboralesApi.restful import registrar as registrar
from django.conf.urls import url 

router = routers.DefaultRouter()
router.register(r'informacionEvaluadores', views.EvaluadorViewSet)


urlpatterns = [
    path('api/info/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api/buscarCedula/', buscarCuentasCedulaViews.as_view())
    #path('api/verficicarCorreo/', login.verificarExistenciaCorreo),
    url(r'^api/verficicarCorreo$', login.verificarExistenciaCorreo),
    url(r'^api/loginAcceso$', login.loginAcceso),
    url(r'^api/saveExperienciaLaboral$', registrar.registrarExperienciaLaboral),
    url(r'^api/registrarParticipante$', registrar.registrarParticipante),
]