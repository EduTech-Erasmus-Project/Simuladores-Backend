# SimuladoresLaboralesApi/urls.py
from django.urls import include, path
from rest_framework import routers
from SimuladoresLaboralesApi import views as views
from SimuladoresLaboralesApi.restful import login as login
from SimuladoresLaboralesApi.restful import registrar as registrar
from SimuladoresLaboralesApi.restful import asignacion as asignacion
from SimuladoresLaboralesApi.restful import ejercitario as ejercitario
from SimuladoresLaboralesApi.restful import actividad as actividad
from SimuladoresLaboralesApi.restful import participante as participante
from SimuladoresLaboralesApi.restful import evaluador as evaluador
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
    url(r'^api/registrarEvaluadores$', registrar.registrarEvaluador),
    url(r'^api/registrarAsignacion$', asignacion.crearNuevaAsignacion),
    url(r'^api/registrarActividad$', actividad.crearNuevaActividadUnity),
    url(r'^api/obtenerAsignacionesEjercitariosDeParticipante$', ejercitario.obtenerAsignacionDeEjercitarioDeUnParticipante),
    url(r'^api/tiempoTotalResolucionCompletaPorEjercitario$', asignacion.tiempoTotalResolucionCompletaPorEjercitario),
    url(r'^api/obtenerListaDeEscenarios$', ejercitario.obtenerListaDeEscenarios),
    url(r'^api/obtenerTipoDiscapacidadPorEvaluador$', ejercitario.obtenerTipoDiscapacidadPorEvaluador),
    url(r'^api/changePassword$', login.changePassword),
    url(r'^api/eliminarCuenta$', participante.eliminarCuentaParticipante),
    url(r'^api/editarCuenta$', participante.editarCuentaParticipante),
    path('api/getEjercitario/<int:pk>', ejercitario.getEscenario),
    path('api/getParticipante/<str:correo>', participante.getParticipante),
    path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    path('api/informacionActividadesParticipante/<str:correo>', participante.informacionActividadesParticipante),
]