# SimuladoresLaboralesApi/urls.py
from django.urls import include, path
from rest_framework import routers
from SimuladoresLaboralesApi import views as views

router = routers.DefaultRouter()
router.register(r'informacionEvaluadores', views.EvaluadorViewSet)


urlpatterns = [
    path('api/info/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]