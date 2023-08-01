import random
from django.db import transaction

from myapp.models import Competencia, Equipo, Grupo

def sortear_equipos_en_grupos(competencia_id):
    competencia = Competencia.objects.get(pk=competencia_id)
    equipos_participantes = list(Equipo.objects.all())
    grupos_existen = competencia.grupos.exists()

    # Obtener el nuevo número de grupos desde la competencia
    numero_grupos = competencia.numero_grupos

    with transaction.atomic():
        if not grupos_existen or competencia.grupos.count() != numero_grupos:
            # Eliminar los grupos existentes si no hay grupos o el número de grupos cambió
            competencia.grupos.all().delete()

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
