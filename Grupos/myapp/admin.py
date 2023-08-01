from django.contrib import admin
from .models import Grupo, Equipo, Partido, Jugador, Competencia
from .utils import sortear_equipos_en_grupos


def sortear_grupos(modeladmin, request, queryset):
    for competencia in queryset:
        sortear_equipos_en_grupos(competencia.id)
    modeladmin.message_user(request, "Se han sorteado los grupos exitosamente.")


sortear_grupos.short_description = "Sortear Grupos"


class CompetenciaAdmin(admin.ModelAdmin):
    actions = [sortear_grupos]


# Register your models here.
admin.site.register(Grupo)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Jugador)
admin.site.register(Competencia, CompetenciaAdmin)
