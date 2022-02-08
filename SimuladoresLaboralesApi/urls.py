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
from SimuladoresLaboralesApi.restful import experienciaLaboral as experienciaLaboral
from SimuladoresLaboralesApi.restful import DiscapacidadParticipante as discapacidadParticipante
from SimuladoresLaboralesApi.restful import comentario as comentario
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
    url(r'^api/agregarNuevoComentarioActividadParticipante$', comentario.agregarNuevoComentarioActividadParticipante),
    url(r'^api/obtenerAsignacionesEjercitariosDeParticipante$', ejercitario.obtenerAsignacionDeEjercitarioDeUnParticipante),
    url(r'^api/tiempoTotalResolucionCompletaPorEjercitario$', asignacion.tiempoTotalResolucionCompletaPorEjercitario),
    url(r'^api/obtenerListaDeEscenarios$', ejercitario.obtenerListaDeEscenarios),
    url(r'^api/crearGraficaInicioExpertoTipoDiscapacidadVsNota$', ejercitario.crearGraficaInicioExpertoTipoDiscapacidadVsNota),
    url(r'^api/obtenerTipoGeneroPorEvaluador$', ejercitario.obtenerTipoGeneroPorEvaluador),
    url(r'^api/graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral$', ejercitario.graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral),
    url(r'^api/changePassword$', login.changePassword),
    url(r'^api/eliminarCuenta$', participante.eliminarCuentaParticipante),
    url(r'^api/editarCuenta$', participante.editarCuentaParticipante),
    url(r'^api/changePasswordResponsable$', login.changePasswordResponsable),
    url(r'^api/eliminarCuentaResponsable$', evaluador.eliminarCuentaResponsable),
    url(r'^api/editarCuentaResponsable$', evaluador.editarCuentaResponsable),
    url(r'^api/obtenerDiscapacidad$', ejercitario.obtenerDiscapacidad),
    url(r'^api/graficaInfoExpertoTipoDiscapacidadVsNotas$', ejercitario.graficaInfoExpertoTipoDiscapacidadVsNotas),
    url(r'^api/graficaPastelGeneroPorEjercitario$', ejercitario.graficaPastelGeneroPorEjercitario),
    url(r'^api/graficainfoParticipanteIntentosVsNotasTiempo$', ejercitario.graficainfoParticipanteIntentosVsNotasTiempo),
    path('api/getEjercitario/<int:pk>', ejercitario.getEscenario),
    path('api/getParticipante/<str:correo>', participante.getParticipante),
    path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    path('api/getEvaluador/<str:correo>', evaluador.getEvaluadorCorreo),
    path('api/getParticipantesEvaluadorAceptar/<str:correo>', evaluador.getParticipantesEvaluadorAceptar),
    path('api/getParticipantesEvaluadorAceptados/<str:correo>', evaluador.getParticipantesEvaluadorAceptados),
    path('api/informacionActividadesParticipante/<str:correo>', participante.informacionActividadesParticipante),
    path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    path('api/agregarParticipanteEvaluador/<str:correo>', evaluador.agregarParticipanteEvaluador),
    path('api/eliminarParticipanteEvaluador/<str:correo>', evaluador.eliminarParticipanteEvaluador),
    path('api/getEjercitarioNumeroDeEjercitario/<int:numeroDeEjercitario>', ejercitario.getEscenarioPorNumero),
    path('api/getEstudiantesEjercitarioResponsable/<str:correo>/<int:ejercitario>', ejercitario.getEstudiantesEjercitarioResponsable),
    path('api/getNotasEstudianteEjercitarioResponsable/<str:correoEvaluador>/<int:ejercitario>/<str:correoParticipante>', ejercitario.getNotasEstudianteEjercitarioResponsable),
    path('api/getExperienciaLaboralParticipante/<str:correo>', experienciaLaboral.getExperienciaLaboral),
    path('api/getDiscapacidadesDelParticipante/<str:correo>', discapacidadParticipante.getDiscapacidadesDelParticipante),
    path('api/getParticipantesIntentosEjercitario/<str:correo>/<int:ejercitario>', participante.getParticipantesIntentosEjercitario),
    path('api/getComentariosActividadRealizada/<int:actividad>', comentario.getComentariosActividadRealizada),
    path('api/getEvaluadores/', evaluador.getEvaluadores),
   
    
]