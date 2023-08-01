from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Competencia, Grupo, Equipo, Partido, Jugador
from .utils import sortear_equipos_en_grupos, generar_programacion_partidos


# Create your views here.

def generar_partidos(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    generar_programacion_partidos(competencia_id)

    # Redireccionar a la vista 'partidos'
    return redirect(reverse('partidos', kwargs={'competencia_id': competencia_id}))


def sortear_grupos(request):
    competencias = Competencia.objects.all()
    for competencia in competencias:
        sortear_equipos_en_grupos(competencia.id)

    return redirect('grupos', pk=   competencia.id)


def home(request):
    competencias = Competencia.objects.all()
    return render(request, 'home.html', {'competencias': competencias})


def competencias(request):
    competencias = Competencia.objects.all()
    return render(request, 'competencias.html', {'competencias': competencias})


def detalles_competencia(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    return render(request, 'detalles_competencia.html', {'competencia': competencia})


def grupos(request, competencia_id):
    competencia = Competencia.objects.get(pk=competencia_id)
    grupos = competencia.grupos.all()
    return render(request, 'grupos.html', {'grupos': grupos})


def partidos(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    grupos = competencia.grupos.all()

    # Obtenemos todos los partidos relacionados con los grupos de la competencia
    partidos = Partido.objects.filter(equipo_local__in=grupos.values('equipos__id'),
                                      equipo_visitante__in=grupos.values('equipos__id'))

    return render(request, 'partidos.html', {'competencia': competencia, 'partidos': partidos})


def jugadores(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    jugadores = Jugador.objects.filter(equipo__in=competencia.grupos.all())
    return render(request, 'jugadores.html', {'competencia': competencia, 'jugadores': jugadores})
