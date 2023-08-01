from datetime import datetime, timedelta
import random
from datetime import timedelta

from django.db import transaction

from myapp.models import Competencia, Equipo, Grupo, Partido


def sortear_equipos_en_grupos(competencia_id):
    competencia = Competencia.objects.get(pk=competencia_id)
    numero_grupos = competencia.numero_grupos

    # Obtener una lista de los equipos participantes
    equipos_participantes = list(Equipo.objects.all())

    with transaction.atomic():
        # Eliminar los grupos existentes si no hay grupos o el número de grupos cambió
        if competencia.grupos.count() != numero_grupos:
            competencia.grupos.all().delete()

            # Asignar los equipos a cada grupo
            equipos_por_grupo = len(equipos_participantes) // numero_grupos
            random.shuffle(equipos_participantes)

            for i in range(numero_grupos):
                grupo = Grupo.objects.create(nombre=f"Grupo {i + 1}", descripcion=f"Grupo {i + 1} de la competencia")
                equipos_asignados = equipos_participantes[i * equipos_por_grupo: (i + 1) * equipos_por_grupo]
                for equipo in equipos_asignados:
                    grupo.equipos.add(equipo)
                competencia.grupos.add(grupo)

        else:
            equipos_en_grupos = [equipo for grupo in competencia.grupos.all() for equipo in grupo.equipos.all()]
            random.shuffle(equipos_en_grupos)

            for grupo in competencia.grupos.all():
                equipo_por_grupo = len(grupo.equipos.all())
                equipos_asignados = equipos_en_grupos[:equipo_por_grupo]
                equipos_en_grupos = equipos_en_grupos[equipo_por_grupo:]
                grupo.equipos.clear()
                for equipo in equipos_asignados:
                    grupo.equipos.add(equipo)

    competencia.save()


def generar_programacion_partidos(competencia_id):
    competencia = Competencia.objects.get(pk=competencia_id)
    grupos = competencia.grupos.all()
    numero_equipos_por_grupo = len(Equipo.objects.all()) // len(grupos)

    # Calcular el número total de partidos por grupo
    numero_partidos_por_grupo = numero_equipos_por_grupo * (numero_equipos_por_grupo - 1) // 2

    with transaction.atomic():
        # Fecha de inicio para la programación de partidos
        fecha_inicio = datetime.now()

        for grupo in grupos:
            equipos_grupo = grupo.equipos.all()
            equipos_combinaciones = [(equipo1, equipo2) for i, equipo1 in enumerate(equipos_grupo) for equipo2 in
                                     equipos_grupo[i + 1:]]

            # Barajear las combinaciones para asegurar que los partidos se generen al azar
            random.shuffle(equipos_combinaciones)

            # Crear los partidos para cada combinación de equipos
            for equipo1, equipo2 in equipos_combinaciones:
                # Asignar una fecha para el partido (puedes ajustar la lógica según tus necesidades)
                fecha_partido = fecha_inicio + timedelta(days=1)  # Agrega un día a la fecha de inicio para cada partido

                Partido.objects.create(equipo_local=equipo1, equipo_visitante=equipo2, fecha=fecha_partido)
