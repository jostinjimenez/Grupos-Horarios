
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('competencias/', views.competencias, name='competencias'),
    path('competencias/<int:competencia_id>/', views.detalles_competencia, name='detalles_competencia'),
    path('competencias/<int:competencia_id>/grupos/', views.grupos, name='grupos'),
    path('competencias/<int:competencia_id>/jugadores/', views.jugadores, name='jugadores'),
    path('sortear_grupos/', views.sortear_grupos, name='sortear_grupos'),
    path('competencias/<int:competencia_id>/partidos/', views.partidos, name='partidos'),
    path('competencias/<int:competencia_id>/generar_partidos/', views.generar_partidos, name='generar_partidos'),

]
