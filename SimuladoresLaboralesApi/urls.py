# SimuladoresLaboralesApi/urls.py
from django import urls
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
import usuario.views as user 
from django.conf.urls import url
from SimuladoresLaboralesApi.restful.login import Login
import adminApi.views as view
from usuario.models import Usuario as usuario
from usuario.views import EvaluadorRetrieveAPIView, MiPefilAPIView, actualizarPassword


router = routers.DefaultRouter()
router.register(r'informacionEvaluadores', views.EvaluadorViewSet)

urlpatterns = [
    path('api/info/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/buscarCedula/', buscarCuentasCedulaViews.as_view())
    # path('api/verficicarCorreo/', login.verificarExistenciaCorreo),
    # url(r'^api/verficicarCorreo$', login.verificarExistenciaCorreo),
    # url(r'^api/login$', Login.as_view(), name='token_obtain_pair'),
    # url(r'^api/login$', login.login),
    url(r'^api/login$', Login.as_view(), name='token_obtain_pair'),  # terminado
    # url(r'^api/loginAcceso$', login.loginAcceso),
    url(r'^api/logout$', login.logout),  # terminado
    # url(r'^api/refreshToken$', login.refreshToken),
    url(r'^api/saveExperienciaLaboral$', registrar.registrarExperienciaLaboral),
    url(r'^api/registro$', registrar.registrarParticipante),  # Terminado
    # url(r'^api/registrarParticipante$', registrar.registrarParticipante), #registra un partisipante
    # url(r'^api/registrarEvaluadores$', registrar.registrarEvaluador), #registra un evaluador
    url(r'^api/registrarDiscapacidad$', discapacidadParticipante.registrarDiscapacidad),  #
    url(r'^api/registrarExperienciaLaboral$', experienciaLaboral.registrarExperienciaLaboral),  #
    url(r'^api/registrarAsignacion$', asignacion.crearNuevaAsignacion),  #
    url(r'^api/agregarAsignacioneParticipante$', asignacion.agregarAsignacioneParticipante),  #
    url(r'^api/registrarActividad$', actividad.crearNuevaActividadUnity),  # Verificar
    url(r'^api/agregarNuevoComentarioActividadParticipante$', comentario.agregarNuevoComentarioActividadParticipante),
    # verificar
    url(r'^api/obtenerAsignacionesEjercitariosDeParticipante$',
        ejercitario.obtenerAsignacionDeEjercitarioDeUnParticipante),  #
    url(r'^api/tiempoTotalResolucionCompletaPorEjercitario$', asignacion.tiempoTotalResolucionCompletaPorEjercitario),
    # verificar
    url(r'^api/obtenerListaDeEscenarios$', ejercitario.obtenerListaDeEscenarios),  #
    url(r'^api/crearGraficaInicioExpertoTipoDiscapacidadVsNota$',
        ejercitario.crearGraficaInicioExpertoTipoDiscapacidadVsNota),
    url(r'^api/obtenerTipoGeneroPorEvaluador$', ejercitario.obtenerTipoGeneroPorEvaluador),  # Terminaod
    url(r'^api/obtenerDiscapacidadesPorEvaluador$', ejercitario.obtenerDiscapacidadesPorEvaluador),  # Terminado
    url(r'^api/obtenerParticipantesEjercitarioPorEvaluador$', ejercitario.obtenerParticipantesEjercitarioPorEvaluador),
    # Terminado

    url(r'^api/totalParticipantesPorEvaluador$', ejercitario.contarParticipantesPorEvaluador),  # Terminado
    url(r'^api/graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral$',
        ejercitario.graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral),
    url(r'^api/changePassword$', login.changePassword),
    url(r'^api/eliminarCuenta$', participante.eliminarCuentaParticipante),
    url(r'^api/editarCuenta$', participante.editarCuentaParticipante),
    url(r'^api/changePasswordResponsable$', login.changePasswordResponsable),
    url(r'^api/eliminarCuentaResponsable$', evaluador.eliminarCuentaResponsable),
    url(r'^api/editarCuentaResponsable$', evaluador.editarCuentaResponsable),
    url(r'^api/obtenerDiscapacidad$', ejercitario.obtenerDiscapacidad),  # Terminado
    url(r'^api/graficaInfoExpertoTipoDiscapacidadVsNotas$', ejercitario.graficaInfoExpertoTipoDiscapacidadVsNotas),
    url(r'^api/graficaPastelGeneroPorEjercitario$', ejercitario.graficaPastelGeneroPorEjercitario),
    url(r'^api/graficainfoParticipanteIntentosVsNotasTiempo$',
        ejercitario.graficainfoParticipanteIntentosVsNotasTiempo),
    path('api/getEjercitario/<int:pk>', ejercitario.getEscenario),
    path('api/getParticipante/<int:pk>', participante.getParticipante),  # Terminado --
    path('api/getParticipanteDeUnResponsable/<str:correo>/<str:correoResponsable>',
         participante.getParticipanteDeUnResponsable),
    path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    # path('api/getEvaluador/<str:correo>', evaluador.getEvaluadorCorreo),
    path('api/getParticipantesEvaluadorAceptar/<str:correo>', evaluador.getParticipantesEvaluadorAceptar),
    path('api/getParticipantesEvaluadorAceptados/<str:correo>', evaluador.getParticipantesEvaluadorAceptados),
    path('api/informacionActividadesParticipante/<str:correo>', participante.informacionActividadesParticipante),
    




     #metodos de Jonnatan
    path('api/getCompetenciasTotal/', ejercitario.CompetenciaT.as_view()),  # Terminado
    path('api/evaluadorTotalPendientes/', view.listarEvaluadoresPendientes), # Terminado
    path('api/evaluadorTotalAprobados/', view.listarEvaluladoresAprobados), # Terminado
    path('api/evaluadorTotalRechazados/', view.listarEvaluladoresRechazado), # Terminado
    path('api/aprobarEvaluador/', view.aprobarEvaluador),  # terminado
    path('api/registroCompetencia/', ejercitario.registroCompetencia),  # terminado
    path('api/discapacidadListas/', discapacidadParticipante.getDiscapacidad),  # terminado 
    path('api/regisDiscapacidad/', discapacidadParticipante.regiDiscapacidad),  # terminado 
    path('api/bloqueoCuenta/<int:pk>', view.bloqueoEvaluador),
     





    # path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    path('api/agregarParticipanteEvaluador/<str:correo>', evaluador.agregarParticipanteEvaluador),
    path('api/eliminarParticipanteEvaluador/<str:correo>', evaluador.eliminarParticipanteEvaluador),
    path('api/getEjercitarioNumeroDeEjercitario/<int:numeroDeEjercitario>', ejercitario.getEscenarioPorNumero),  #
    path('api/getEstudiantesEjercitarioResponsable/<int:ejercitario>',
         ejercitario.getEstudiantesEjercitarioResponsable),  # verificar
    path(
        'api/getNotasEstudianteEjercitarioResponsable/<int:ejercitario>/<str:idParticipante>',  #
        ejercitario.getNotasEstudianteEjercitarioResponsable),
    path('api/getExperienciaLaboralParticipante/<str:correo>', experienciaLaboral.getExperienciaLaboral),
    path('api/getDiscapacidadesDelParticipante/<str:correo>',
         discapacidadParticipante.getDiscapacidadesDelParticipante),
    path('api/getParticipantesIntentosEjercitario/<str:correo>/<int:ejercitario>',
         participante.getParticipantesIntentosEjercitario),
    path('api/getComentariosActividadRealizada/<int:actividad>', comentario.getComentariosActividadRealizada),
    path('api/getEvaluadores/', evaluador.getEvaluadores),
    # path('api/getUsuarioCookiesJWT/', login.recuperarUsuarioCookiesJWT),
    path('api/obtenerInformacionAsignacionesParticipante/<str:correo>/<str:correoResponsable>',
         participante.obtenerInformacionAsignacionesParticipante),
    path('api/eliminarAsignacion/<int:idAsignacion>', asignacion.eliminarAsignacion),
    path('api/obtenerInformacionLandingPage/', ejercitario.obtenerInformacionLandingPage),
    ##
    path('api/getTotalEjercitarios/', ejercitario.getTotalEjercitarios),  # Terminado
    path('api/getCompetencias/', ejercitario.CompetenciasRetrieveAPIView.as_view()),  # Terminado
    
    path('api/getCompetencia/<int:pk>', ejercitario.CompetenciaRetrieveAPIView.as_view()),  # Terminado
  
    path('api/getActividadesParticipante/<int:idEjercitario>/<int:idParticipante>',
         actividad.getActividadesParticipante), #terminado
    path('api/getActividades/<int:idEjercitario>',
         actividad.getActividades), #terminado
   path('api/obtenerParticipantesCompetencia/<int:pk>', ejercitario.ParticipantesEjercitario.as_view()),  # terminado
    path('api/obtenerParticipantesPendientes/', ejercitario.ParticipantesPendientesListApiView.as_view()),  # terminado
    path('api/obtenerParticipantesRechazados/', ejercitario.ParticipantesRechazadosListApiView.as_view()),  # terminado
    path('api/obtenerParticipantes/', ejercitario.ParticipantesListApiView.as_view()),  # terminado
    path('api/aprobarParticipante/', evaluador.aprobarParticipante),  # terminado
    path('api/comentarios/<int:pk>', actividad.ComentarioListAPIView.as_view()),  # terminado
    path('api/comentar/', actividad.ComentarioCreateAPIView.as_view()),  # terminado
    path('api/getActividad/<int:pk>', actividad.getActividad),  # terminado
    path('api/getEvaluador/<int:pk>', EvaluadorRetrieveAPIView.as_view()),  # terminado
    path('api/perfil/', MiPefilAPIView.as_view()),  # Terminado
    path('api/actualizarPassword/', actualizarPassword),  # terminado

# FabianUrls
    path('api/listaEjercitario/', ejercitario.listaEjercitario),
    path('api/listarUsuarioRegistrado/',user.listarUsuarioRegistrado),

]
