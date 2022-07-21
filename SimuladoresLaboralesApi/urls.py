from django.urls import path
from SimuladoresLaboralesApi.models import Pregunta
from SimuladoresLaboralesApi.restful import login as login
from SimuladoresLaboralesApi.restful import registrar as registrar
from SimuladoresLaboralesApi.restful import ejercitario as ejercitario
from SimuladoresLaboralesApi.restful import actividad as actividad
from SimuladoresLaboralesApi.restful import participante as participante
from SimuladoresLaboralesApi.restful import evaluador as evaluador
from SimuladoresLaboralesApi.restful import experienciaLaboral as experienciaLaboral
from SimuladoresLaboralesApi.restful import pregunta as pregunta
from SimuladoresLaboralesApi.restful import rubrica as rubrica
from SimuladoresLaboralesApi.restful import DiscapacidadParticipante as discapacidadParticipante
from SimuladoresLaboralesApi.restful import comentario as comentario
import usuario.views as user

import usuario.views as user
import adminApi.views as view
from django.conf.urls import url
from SimuladoresLaboralesApi.restful.login import Login
import adminApi.views as view
from usuario.models import Usuario as usuario
from usuario.views import EvaluadorRetrieveAPIView, MiPefilAPIView, actualizarPassword, listarUsuarioRegistrado

urlpatterns = [
    # path('api/info/', include(router.urls)),
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
    url(r'^api/saveExperienciaLaboral$',
        registrar.registrarExperienciaLaboral),  # verificar
    url(r'^api/registro$', registrar.registrarParticipante),  # Terminado
    # url(r'^api/registrarParticipante$', registrar.registrarParticipante), #registra un partisipante
    # url(r'^api/registrarEvaluadores$', registrar.registrarEvaluador), #registra un evaluador
    # url(r'^api/registrarDiscapacidad$', discapacidadParticipante.registrarDiscapacidad),  # eliminar
    url(r'^api/registrarExperienciaLaboral$',
        experienciaLaboral.registrarExperienciaLaboral),  # eliminar
    # url(r'^api/registrarAsignacion$', asignacion.crearNuevaAsignacion),  # eliminar
    # url(r'^api/agregarAsignacioneParticipante$', asignacion.agregarAsignacioneParticipante),  # eliminar
    url(r'^api/registrarActividad$',
        actividad.crearNuevaActividadUnity),  # Terminado
    # url(r'^api/agregarNuevoComentarioActividadParticipante$', comentario.agregarNuevoComentarioActividadParticipante),
    # verificar
    # url(r'^api/obtenerAsignacionesEjercitariosDeParticipante$',
    # ejercitario.obtenerAsignacionDeEjercitarioDeUnParticipante),  #
    # url(r'^api/tiempoTotalResolucionCompletaPorEjercitario$', asignacion.tiempoTotalResolucionCompletaPorEjercitario),
    # verificar
    url(r'^api/obtenerListaDeEscenarios$',
        ejercitario.obtenerListaDeEscenarios),  #
    # url(r'^api/crearGraficaInicioExpertoTipoDiscapacidadVsNota$',
    # ejercitario.crearGraficaInicioExpertoTipoDiscapacidadVsNota),
    url(r'^api/obtenerTipoGeneroPorEvaluador$',
        ejercitario.obtenerTipoGeneroPorEvaluador),  # Terminaod
    url(r'^api/obtenerDiscapacidadesPorEvaluador$',
        ejercitario.obtenerDiscapacidadesPorEvaluador),  # Terminado
    url(r'^api/obtenerParticipantesEjercitarioPorEvaluador$',
        ejercitario.obtenerParticipantesEjercitarioPorEvaluador),
    # Terminado

    url(r'^api/totalParticipantesPorEvaluador$',
        ejercitario.contarParticipantesPorEvaluador),  # Terminado
    # url(r'^api/graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral$',
    # ejercitario.graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral),
    # url(r'^api/changePassword$', login.changePassword),
    # url(r'^api/eliminarCuenta$', participante.eliminarCuentaParticipante),  # eliminar
    # url(r'^api/editarCuenta$', participante.editarCuentaParticipante),  # eliminar
    # url(r'^api/changePasswordResponsable$', login.changePasswordResponsable),  # eliminar
    # url(r'^api/eliminarCuentaResponsable$', evaluador.eliminarCuentaResponsable),  # eliminar
    # url(r'^api/editarCuentaResponsable$', evaluador.editarCuentaResponsable),  # eliminar
    url(r'^api/obtenerDiscapacidad$', ejercitario.obtenerDiscapacidad),  # Terminado
    # url(r'^api/graficaInfoExpertoTipoDiscapacidadVsNotas$', ejercitario.graficaInfoExpertoTipoDiscapacidadVsNotas),
    # aliminar
    # url(r'^api/graficaPastelGeneroPorEjercitario$', ejercitario.graficaPastelGeneroPorEjercitario),  # eliminar
    # url(r'^api/graficainfoParticipanteIntentosVsNotasTiempo$',
    # ejercitario.graficainfoParticipanteIntentosVsNotasTiempo),  # eliminar
    path('api/getEjercitario/<int:pk>', ejercitario.getEscenario),
    path('api/getParticipante/<int:pk>',
         participante.getParticipante),  # Terminado --

    # metodos de Jonnatan
    path('api/getCompetenciasTotal/',
         ejercitario.CompetenciaT.as_view()),  # Terminado
    path('api/evaluadorTotalPendientes/',
         view.listarEvaluadoresPendientes),  # Terminado
    path('api/evaluadorTotalAprobados/',
         view.listarEvaluladoresAprobados),  # Terminado
    path('api/evaluadorTotalRechazados/',
         view.listarEvaluladoresRechazado),  # Terminado
    path('api/aprobarEvaluador/', view.aprobarEvaluador),  # terminado
    path('api/registroCompetencia/', ejercitario.registroCompetencia),  # terminado

    path('api/discapacidadListas/',
         discapacidadParticipante.getDiscapacidad),  # terminado
    path('api/regisDiscapacidad/',
         discapacidadParticipante.regiDiscapacidad),  # terminado
    path('api/bloqueoCuenta/<int:pk>', view.bloqueoEvaluador),

    path('api/discapacidadListas/', discapacidadParticipante.getDiscapacidad),  # terminado 
    path('api/regisDiscapacidad/', discapacidadParticipante.regiDiscapacidad),  # terminado 
    path('api/editarDiscapacidad/<int:pk>', discapacidadParticipante.editarDiscapacidad),  # terminado 
    path('api/guardarEditarCompetencia/', ejercitario.guardarECompetencia),  # terminado 
    path('api/bloqueoCuenta/<int:pk>', view.bloqueoEvaluador), #terminado
    path('api/editarCompetencia/<int:pk>', ejercitario.editarCompetencia),  # terminado
    path('api/guardarEditarDiscapacidad/', discapacidadParticipante.guardarEditarDiscapacidad),  # terminado 


    # path('api/getParticipanteDeUnResponsable/<str:correo>/<str:correoResponsable>',
    # participante.getParticipanteDeUnResponsable),
    # path('api/getEvaluador/<int:pk>', evaluador.getEvaluador), #eliminar
    # path('api/getEvaluador/<str:correo>', evaluador.getEvaluadorCorreo), #eliminar
    # path('api/getParticipantesEvaluadorAceptar/<str:correo>', evaluador.getParticipantesEvaluadorAceptar),
    # path('api/getParticipantesEvaluadorAceptados/<str:correo>', evaluador.getParticipantesEvaluadorAceptados),
    # path('api/informacionActividadesParticipante/<str:correo>', participante.informacionActividadesParticipante),
    # path('api/getEvaluador/<int:pk>', evaluador.getEvaluador),
    # path('api/agregarParticipanteEvaluador/<str:correo>', evaluador.agregarParticipanteEvaluador),
    # path('api/eliminarParticipanteEvaluador/<str:correo>', evaluador.eliminarParticipanteEvaluador),

    path('api/getEjercitarioNumeroDeEjercitario/<int:numeroDeEjercitario>',
         ejercitario.getEscenarioPorNumero),  #
    # path('api/getEstudiantesEjercitarioResponsable/<int:ejercitario>',
    # ejercitario.getEstudiantesEjercitarioResponsable),  # verificar
    path(
        'api/getNotasEstudianteEjercitarioResponsable/<int:ejercitario>/<str:idParticipante>',  #
        ejercitario.getNotasEstudianteEjercitarioResponsable),
    path('api/getExperienciaLaboralParticipante/<str:correo>',
         experienciaLaboral.getExperienciaLaboral),
    # path('api/getDiscapacidadesDelParticipante/<str:correo>',
    # discapacidadParticipante.getDiscapacidadesDelParticipante),
    path('api/getParticipantesIntentosEjercitario/<str:correo>/<int:ejercitario>',
         participante.getParticipantesIntentosEjercitario),
    # path('api/getComentariosActividadRealizada/<int:actividad>', comentario.getComentariosActividadRealizada),
    path('api/getEvaluadores/', evaluador.getEvaluadores),
    # path('api/getUsuarioCookiesJWT/', login.recuperarUsuarioCookiesJWT),
    # path('api/obtenerInformacionAsignacionesParticipante/<str:correo>/<str:correoResponsable>',
    # participante.obtenerInformacionAsignacionesParticipante),
    # path('api/eliminarAsignacion/<int:idAsignacion>', asignacion.eliminarAsignacion),
    path('api/obtenerInformacionLandingPage/',
         ejercitario.obtenerInformacionLandingPage),
    ##
    path('api/getTotalEjercitarios/',
         ejercitario.getTotalEjercitarios),  # Terminado
    path('api/getCompetencias/',
         ejercitario.CompetenciasRetrieveAPIView.as_view()),  # Terminado

    path('api/getCompetencia/<int:pk>',
         ejercitario.CompetenciaRetrieveAPIView.as_view()),  # Terminado

    path('api/getActividadesParticipante/<int:idEjercitario>/<int:idParticipante>',
         actividad.getActividadesParticipante),  # terminado
    path('api/getActividades/<int:idEjercitario>',
         actividad.getActividades),  # terminado
    path('api/obtenerParticipantesCompetencia/<int:pk>',
         ejercitario.ParticipantesEjercitario.as_view()),  # terminado
    path('api/obtenerParticipantesPendientes/',
         ejercitario.ParticipantesPendientesListApiView.as_view()),  # terminado
    path('api/obtenerParticipantesRechazados/',
         ejercitario.ParticipantesRechazadosListApiView.as_view()),  # terminado
    path('api/obtenerParticipantes/',
         ejercitario.ParticipantesListApiView.as_view()),  # terminado
    path('api/aprobarParticipante/', evaluador.aprobarParticipante),  # terminado
    path('api/comentarios/<int:pk>',
         actividad.ComentarioListAPIView.as_view()),  # terminado

    path('api/correccionPreguntas/<int:pk>',
         actividad.PreguntasListAPIView.as_view()),  # terminado

    path('api/comentar/', actividad.ComentarioCreateAPIView.as_view()),  # terminado
    path('api/getActividad/<int:pk>',
         actividad.ActividadRetrieveAPIView.as_view()),  # terminado
    path('api/getEvaluador/<int:pk>',
         EvaluadorRetrieveAPIView.as_view()),  # terminado
    path('api/perfil/', MiPefilAPIView.as_view()),  # Terminado
    path('api/actualizarImagenPerfil/', user.actualizarImagenPerfil),  # Terminado
    path('api/actualizarPassword/', actualizarPassword),  # terminado
    path('api/informacionCount/', ejercitario.informacionCount),  # terminado
    path('api/reporte/<int:idCompetencia>/<int:idParticipante>',
         participante.getReporte),  # terminado

    # FabianUrls
    path('api/listaEjercitario/', ejercitario.listaEjercitario),  # terminado
    path('api/listarUsuarioRegistrado/', user.listarUsuarioRegistrado),  # terminado
    path('api/bloqueoCuenta/<int:pk>', user.bloqueoUsuario),  # Termindo
    path('api/editarEjercitario/', ejercitario.editarEjercitario),  # Terminado
    path('api/recuperarEjercitario/<int:pk>', ejercitario.recuperarEjercitario),  # Terminado
    path('api/registroEjercitario/', ejercitario.registroEjercitario),  # Terminado
    
    path('api/registroPregunta/', pregunta.registroPregunta),  # Terminado
    path('api/editarPregunta/', pregunta.editarPregunta),# Terminado
    path('api/listaPreguntaEjercitario/<int:pk>', pregunta.listaPreguntaEjercitario),# Terminado
    path('api/recuperaPreguntaEjercitario/<int:pk>', pregunta.recuperarPreguntaEjercitario),# Terminado
    path('api/eliminarPregunta/<int:pk>', pregunta.eliminarPregunta),
    
    path('api/registroRubrica/', rubrica.registroRubrica),# Terminado
    path('api/editarRubrica/', rubrica.editarRubrica),# Terminado
    path('api/recuperarRubrica/<int:pk>', rubrica.recuperarRubrica),# Terminado
    path('api/listaRubrica/<int:pk>', rubrica.listaRubrica),# Terminado
     path('api/eliminarRubrica/<int:pk>', rubrica.eliminarRubrica), #Terminado
    
    
    
         

    # certificados
    path('api/descargarCertificado/<int:idCompetencia>/<int:idParticipante>',
         participante.descargar_certificado),
    # path('api/enviarCertificado/<int:idCompetencia>/<int:idParticipante>', participante.descargar_certificado),


]
