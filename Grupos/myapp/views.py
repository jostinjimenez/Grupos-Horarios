from django.shortcuts import render, get_object_or_404, redirect
from .models import Competencia, Grupo, Equipo, Partido, Jugador
from .utils import sortear_equipos_en_grupos


# Create your views here.

def sortear_grupos(request):
    competencias = Competencia.objects.all()
    for competencia in competencias:
        sortear_equipos_en_grupos(competencia.id)

    return redirect('grupos', id=competencia.id)


def home(request, ):
    competencias = Competencia.objects.all()
    return render(request, 'home.html', {'competencias': competencias})


def competencias(request):
    competencias = Competencia.objects.all()
    return render(request, 'competencias.html', {'competencias': competencias})


def detalles_competencia(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    return render(request, 'detalles_competencia.html', {'competencia': competencia})


def grupos(request, id):
    competencia = Competencia.objects.get(pk=id)
    grupos = competencia.grupos.all()
    return render(request, 'grupos.html', {'grupos': grupos})


def partidos(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    partidos = Partido.objects.filter(equipo_local__in=competencia.grupos.all())
    return render(request, 'partidos.html', {'competencia': competencia, 'partidos': partidos})


def jugadores(request, competencia_id):
    competencia = get_object_or_404(Competencia, pk=competencia_id)
    jugadores = Jugador.objects.filter(equipo__in=competencia.grupos.all())
    return render(request, 'jugadores.html', {'competencia': competencia, 'jugadores': jugadores})
