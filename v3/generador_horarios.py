# archivo: generador_horarios.py

import pandas as pd
from utilidades_horario import (
    cargar_datos_json,
    inicializar_horario_global,
    normalizar_grupo,
    normalizar_materia,
)

from comparador_maestros import find_discrepancies as clasificar_maestros

# REGLA DE NEGOCIO PRINCIPAL
HORAS_POR_ANO = {
    "1": {
        "español": 5,
        "ingles": 3,
        "matematicas": 5,
        "ciencias": 4,
        "historia": 2,
        "geografia": 4,
        "formacion civica y etica": 2,
        "educacion artistica": 3,
        "tutoria": 1,
        "educacion fisica": 2,
        "integracion": 1,
    },
    "2": {
        "español": 5,
        "ingles": 3,
        "matematicas": 5,
        "ciencias": 6,
        "historia": 4,
        "formacion civica y etica": 2,
        "educacion artistica": 3,
        "tutoria": 1,
        "educacion fisica": 2,
        "integracion": 1,
    },
    "3": {
        "español": 5,
        "ingles": 3,
        "matematicas": 5,
        "ciencias": 6,
        "historia": 4,
        "formacion civica y etica": 2,
        "tutoria": 1,
        "educacion artistica": 3,
        "educacion fisica": 2,
        "integracion": 1,
    },
}
for ano in HORAS_POR_ANO:
    HORAS_POR_ANO[ano]["tecnologia"] = 3

# --- FUNCIONES DE SOPORTE Y VALIDACIÓN ---


def poblar_horario_base(horario_global, maestros_continuidad):
    print(
        "Poblando horario con datos de maestros de continuidad (se asume horario válido)..."
    )
    for maestro in maestros_continuidad:
        grupos_actuales = (
            {normalizar_grupo(g) for g in maestro.get("grupos", [])}
            if "grupos" in maestro
            else set()
        )
        if maestro.get("tutoria"):
            grupos_actuales.add(normalizar_grupo(maestro["tutoria"]))
        nombre_corto = " ".join(maestro["nombre"].replace("-", "").strip().split()[:2])
        for clase in maestro.get("horario", []):
            dia, hora, actividad = (
                clase["dia"],
                clase["hora"],
                clase["grupo_o_actividad"],
            )
            # Mejor parsing: maneja formatos variados (Tut., *, comas, etc.)
            grupos_clase_antigua = {
                normalizar_grupo(g.strip())
                for g in actividad.replace("Tut.", "")
                .replace("*", "")
                .replace("Lab.", "")
                .split(",")
                if g.strip() and normalizar_grupo(g.strip()) in grupos_actuales
            }
            if not grupos_clase_antigua:
                continue
            materia_asignada = (
                "TUTORIA"
                if "Tut." in actividad
                else (
                    normalizar_materia(maestro["materias"][0])
                    if maestro.get("materias")
                    else "indefinida"
                )
            )
            if materia_asignada == "tecnologia":
                continue  # Saltar tecnología, se asigna por separado
            for grupo in grupos_clase_antigua:
                if grupo not in horario_global[dia][hora]:
                    continue
                if horario_global[dia][hora][grupo]:
                    print(
                        f"    -> CONFLICTO: Slot {dia} {hora} para {grupo} ya ocupado. Saltando."
                    )
                    continue
                if esta_maestro_ocupado(horario_global, nombre_corto, dia, hora):
                    print(
                        f"    -> CONFLICTO: Maestro {nombre_corto} ocupado en {dia} {hora}. Saltando."
                    )
                    continue
                horario_global[dia][hora][grupo] = {
                    "maestro": nombre_corto,
                    "materia": materia_asignada.upper(),
                }
    return horario_global


def calcular_horas_pendientes(horario_global, grupos_lista):
    pendientes = {}
    for grupo in grupos_lista:
        ano = grupo[0]
        if ano not in HORAS_POR_ANO:
            continue
        pendientes[grupo] = {
            normalizar_materia(k): v for k, v in HORAS_POR_ANO[ano].items()
        }
        for dia in horario_global:
            for hora in horario_global[dia]:
                clase = horario_global[dia][hora].get(grupo)
                if clase:
                    materia_norm = normalizar_materia(clase["materia"])
                    if materia_norm in pendientes[grupo]:
                        pendientes[grupo][materia_norm] -= 1
                        if pendientes[grupo][materia_norm] < 0:
                            pendientes[grupo][materia_norm] = 0
    return pendientes


def esta_maestro_ocupado(horario, maestro_nombre, dia, hora):
    for clase in horario[dia][hora].values():
        if clase and clase["maestro"] == maestro_nombre:
            return True
    return False


def crear_mapa_continuidad(maestros_continuidad):
    mapa = set()
    for data_maestro in maestros_continuidad:
        for clase in data_maestro.get("horario", []):
            grupos_clase_antigua = {
                normalizar_grupo(g)
                for g in clase["grupo_o_actividad"]
                .replace("Tut.", "")
                .replace("*", "")
                .replace("Lab.", "")
                .strip()
                .split(",")
                if g.strip()
            }
            for grupo in grupos_clase_antigua:
                mapa.add((clase["dia"], clase["hora"], grupo))
    return mapa


def _viola_limite_consecutivo(
    horario, dia, hora, grupo, materia, horas_ordenadas, limite=1
):
    if normalizar_materia(materia) == "tecnologia":
        return False  # Excepción para tecnología (permite 3 consecutivas)
    idx_hora_actual = horas_ordenadas.index(hora)
    count_before, count_after, materia_norm = 0, 0, normalizar_materia(materia)
    for i in range(idx_hora_actual - 1, -1, -1):
        clase_anterior = horario[dia][horas_ordenadas[i]].get(grupo)
        if (
            clase_anterior
            and normalizar_materia(clase_anterior["materia"]) == materia_norm
        ):
            count_before += 1
        else:
            break
    for i in range(idx_hora_actual + 1, len(horas_ordenadas)):
        clase_siguiente = horario[dia][horas_ordenadas[i]].get(grupo)
        if (
            clase_siguiente
            and normalizar_materia(clase_siguiente["materia"]) == materia_norm
        ):
            count_after += 1
        else:
            break
    return (count_before + 1 + count_after) > limite


def _crea_clase_dividida(horario, dia, hora_actual, grupo, materia, horas_ordenadas):
    materia_norm = normalizar_materia(materia)
    idx_actual = horas_ordenadas.index(hora_actual)
    # Verificar si ya hay clases de esta materia en el día
    clases_en_dia = [
        i
        for i, h in enumerate(horas_ordenadas)
        if horario[dia][h].get(grupo)
        and normalizar_materia(horario[dia][h][grupo]["materia"]) == materia_norm
    ]
    if not clases_en_dia:
        return False  # Primera clase, no divide
    # Verificar si la nueva clase está adyacente a un bloque existente
    adyacente = any(abs(idx_actual - i) == 1 for i in clases_en_dia)
    return not adyacente  # True si crea división (no adyacente)


def _viola_limite_bloques_dobles(
    horario, dia, hora_actual, grupo, materia, horas_ordenadas, limite_bloques=2
):
    materia_norm = normalizar_materia(materia)
    idx_actual = horas_ordenadas.index(hora_actual)

    # Verificar si esta asignación completa un bloque doble
    es_potencial_bloque_doble = False
    if idx_actual > 0:
        clase_anterior = horario[dia][horas_ordenadas[idx_actual - 1]].get(grupo)
        if (
            clase_anterior
            and normalizar_materia(clase_anterior["materia"]) == materia_norm
        ):
            es_potencial_bloque_doble = True

    if not es_potencial_bloque_doble:
        return False

    # Contar bloques dobles existentes (cualquier materia)
    bloques_existentes = 0
    i = 0
    while i < len(horas_ordenadas) - 1:
        clase_1 = horario[dia][horas_ordenadas[i]].get(grupo)
        clase_2 = horario[dia][horas_ordenadas[i + 1]].get(grupo)
        if clase_1 and clase_2 and clase_1["materia"] == clase_2["materia"]:
            bloques_existentes += 1
            i += 2  # Saltar el bloque
        else:
            i += 1
    return bloques_existentes >= limite_bloques


# Nueva función para llenar huecos con horas de servicio
def llenar_huecos_servicio(
    horario_global, maestros_a_asignar, dias, horas_ordenadas, grupos
):
    print("\n--- PASO 4: Llenando huecos de maestros con horas de servicio ---")
    servicio_por_maestro = {}
    for m in maestros_a_asignar:
        nombre_corto = " ".join(m["nombre"].split()[:2])
        horas_serv = m.get("horas_servicio")
        servicio_por_maestro[nombre_corto] = horas_serv if horas_serv is not None else 0

    # Diccionario para actividades de servicio por maestro (no por grupo)
    teacher_services = {
        maestro: {dia: set() for dia in dias} for maestro in servicio_por_maestro
    }

    # Nuevo: Identificar maestros de formación cívica y asignar "INTEGRACION CURRICULAR" (1 hora, en hueco libre)
    # for m in maestros_a_asignar:
    #    nombre_corto = " ".join(m["nombre"].split()[:2])
    #    if normalizar_materia(m.get("materia", "")) == "formacion civica y etica":
    #        asignada = False
    #        for dia in dias:
    #            for hora in horas_ordenadas:
    #                if not esta_maestro_ocupado(
    #                    horario_global, nombre_corto, dia, hora
    #                ):
    #                    teacher_services[nombre_corto][dia].add(
    #                        (hora, "INTEGRACION CURRICULAR")
    #                    )
    #                    asignada = True
    #                    break
    #            if asignada:
    #                break
    #        if not asignada:
    #            print(
    #                f"    -> ADVERTENCIA: No se pudo asignar INTEGRACION CURRICULAR para {nombre_corto}"
    #            )

    for dia in dias:
        for maestro, horas_servicio in list(servicio_por_maestro.items()):
            if horas_servicio <= 0:
                continue
            hueco_count = 0
            current_hueco_start = None
            for idx, hora in enumerate(horas_ordenadas):
                ocupado = any(
                    horario_global[dia][hora].get(g)
                    and horario_global[dia][hora][g]["maestro"] == maestro
                    for g in grupos
                )
                if not ocupado:
                    if hueco_count == 0:
                        current_hueco_start = idx
                    hueco_count += 1
                    if hueco_count > 2 and horas_servicio > 0:
                        # Llenar el hueco empezando desde el inicio, pero solo los necesarios para romper >2
                        # Por simplicidad, llenamos la última hora del hueco con servicio
                        service_hora = horas_ordenadas[idx]
                        teacher_services[maestro][dia].add(
                            (service_hora, "SERVICIO")
                        )  # Cambiado a tupla para tipo de actividad
                        horas_servicio -= 1
                        hueco_count = 0  # Resetear después de llenar uno
                else:
                    hueco_count = 0
                servicio_por_maestro[maestro] = horas_servicio
    return teacher_services


# --- FUNCIONES DE ASIGNACIÓN ---


def asignar_bloques_tecnologia(
    horario_global, maestros_a_asignar, maestros_continuidad, dias, horas_ordenadas
):
    print(
        "\n--- PASO 1: Buscando el mejor lugar para Tecnología (Mínimo Conflicto) ---"
    )
    mapa_continuidad, tech_by_year = (
        crear_mapa_continuidad(maestros_continuidad),
        {"1": {}, "2": {}, "3": {}},
    )
    for maestro in maestros_a_asignar:
        if normalizar_materia(maestro["materia"]) == "tecnologia":
            nombre_corto = " ".join(maestro["nombre"].split()[:2])
            for grupo in maestro.get("grupos", []):
                ano = grupo[0]
                if ano in tech_by_year:
                    tech_by_year[ano][grupo] = nombre_corto
    for ano in sorted(tech_by_year.keys()):
        grupos_del_ano_map = tech_by_year[ano]
        if not grupos_del_ano_map:
            continue
        posibles_franjas = []
        for dia in dias:
            for i in range(len(horas_ordenadas) - 2):
                horas_bloque = horas_ordenadas[i : i + 3]
                # Validar conflictos básicos
                hora_inicio = horas_bloque[0].split("/")[1].strip().split(":")[0]
                if int(hora_inicio) < 11:
                    continue
                if any(
                    horario_global[dia][h].get(g)
                    or esta_maestro_ocupado(
                        horario_global, grupos_del_ano_map[g], dia, h
                    )
                    for g in grupos_del_ano_map
                    for h in horas_bloque
                ):
                    continue
                conflicto_score = sum(
                    1
                    for h in horas_bloque
                    for g in grupos_del_ano_map
                    if (dia, h, g) in mapa_continuidad
                )
                posibles_franjas.append((conflicto_score, dia, horas_bloque))
        if not posibles_franjas:
            print(
                f"      -> ADVERTENCIA: No se encontró ninguna franja para TECNOLOGIA de {ano}° AÑO."
            )
            continue
        posibles_franjas.sort(key=lambda x: x[0])
        best_score, best_dia, best_horas = posibles_franjas[0]
        print(
            f"  -> Asignando TECNOLOGIA de {ano}° AÑO en {best_dia} {best_horas[0].split('/')[1].strip()}-{best_horas[-1].split('/')[1].strip()}. (Conflicto: {best_score})"
        )
        for grupo, maestro in grupos_del_ano_map.items():
            for h in best_horas:
                horario_global[best_dia][h][grupo] = {
                    "maestro": maestro,
                    "materia": "TECNOLOGIA",
                }
    return horario_global


def asignar_horarios_regulares(
    horario_parcial, maestros_a_asignar, pendientes, dias, horas_ordenadas
):
    print("\n--- PASO 3: Asignando materias de nuevos maestros y horas faltantes ---")
    for maestro in maestros_a_asignar:
        nombre_corto, materia_maestro = (
            " ".join(maestro["nombre"].split()[:2]),
            maestro["materia"],
        )
        materia_norm = normalizar_materia(materia_maestro)
        if materia_norm == "tecnologia":
            continue
        # Asignar tutoría primero
        if maestro.get("tutoria"):
            grupo_tutoria = normalizar_grupo(maestro.get("tutoria"))
            if pendientes.get(grupo_tutoria, {}).get("tutoria", 0) > 0:
                asignada = asignar_clase_con_prioridad(
                    horario_parcial,
                    nombre_corto,
                    "TUTORIA",
                    grupo_tutoria,
                    pendientes,
                    dias,
                    horas_ordenadas,
                )
                if not asignada:
                    print(
                        f"    -> ADVERTENCIA: No se pudo asignar TUTORIA para {grupo_tutoria} (Maestro: {nombre_corto})"
                    )
        # Asignar horas por grupo
        for grupo in maestro.get("grupos", []):
            horas_a_asignar = pendientes.get(grupo, {}).get(materia_norm, 0)
            for _ in range(horas_a_asignar):
                asignada = asignar_clase_con_prioridad(
                    horario_parcial,
                    nombre_corto,
                    materia_maestro.upper(),
                    grupo,
                    pendientes,
                    dias,
                    horas_ordenadas,
                )
                if not asignada:
                    print(
                        f"    -> ADVERTENCIA: No se pudo encontrar espacio para {materia_maestro.upper()} en {grupo} (Maestro: {nombre_corto})"
                    )
    return horario_parcial


# Nueva función auxiliar para asignar con prioridad (evita divisiones y huecos)
def asignar_clase_con_prioridad(
    horario, maestro, materia, grupo, pendientes, dias, horas_ordenadas
):
    posibles_slots = []
    for dia in dias:
        for hora in horas_ordenadas:
            if horario[dia][hora].get(grupo):
                continue
            if esta_maestro_ocupado(horario, maestro, dia, hora):
                continue
            if _viola_limite_consecutivo(
                horario, dia, hora, grupo, materia, horas_ordenadas
            ):
                continue
            if _crea_clase_dividida(
                horario, dia, hora, grupo, materia, horas_ordenadas
            ):
                continue
            if _viola_limite_bloques_dobles(
                horario, dia, hora, grupo, materia, horas_ordenadas
            ):
                continue
            # Puntaje: priorizar adyacencia a clases existentes de la materia
            score = 0
            idx = horas_ordenadas.index(hora)
            if idx > 0 and horario[dia][horas_ordenadas[idx - 1]].get(grupo):
                score += 1
            if idx < len(horas_ordenadas) - 1 and horario[dia][
                horas_ordenadas[idx + 1]
            ].get(grupo):
                score += 1
            posibles_slots.append((-score, dia, hora))  # Mayor score primero
    if not posibles_slots:
        return False
    posibles_slots.sort()
    _, best_dia, best_hora = posibles_slots[0]
    horario[best_dia][best_hora][grupo] = {"maestro": maestro, "materia": materia}
    pendientes[grupo][normalizar_materia(materia)] -= 1
    return True


# -------- FUNCIÓN `main` Y `generar_excel_completo` --------


def main():
    print("--- INICIANDO GENERADOR DE HORARIOS ESCOLARES ---")
    data_maestros, data_referencia = (
        cargar_datos_json("maestros.json"),
        cargar_datos_json("1.json"),
    )
    if not data_maestros or not data_referencia:
        return
    maestros_continuidad, maestros_nuevos = clasificar_maestros(
        data_maestros, data_referencia
    )
    todos_los_maestros_actuales, maestros_a_asignar, maestros_invalidos = (
        data_referencia,
        [],
        [],
    )
    for m in todos_los_maestros_actuales:
        motivo = ""
        if not m.get("materia"):
            motivo = "Materia no especificada"
        elif not (m.get("grupos") or m.get("tutoria")):
            motivo = "No tiene grupos ni tutoría asignados"
        if motivo:
            maestros_invalidos.append({"Maestro": m["nombre"], "Motivo": motivo})
        else:
            maestros_a_asignar.append(m)
    print(
        f"\nAnálisis de maestros completado:\n  - {len(maestros_continuidad)} de continuidad.\n  - {len(maestros_nuevos)} nuevos.\n  - {len(maestros_a_asignar)} a procesar.\n  - {len(maestros_invalidos)} con datos inválidos."
    )
    horario_global, dias, horas_ordenadas, grupos = inicializar_horario_global(
        data_maestros, data_referencia
    )
    horario_con_tecnologia = asignar_bloques_tecnologia(
        horario_global, maestros_a_asignar, maestros_continuidad, dias, horas_ordenadas
    )
    horario_con_base = poblar_horario_base(horario_con_tecnologia, maestros_continuidad)
    horas_pendientes = calcular_horas_pendientes(horario_con_base, grupos)
    horario_con_regulares = asignar_horarios_regulares(
        horario_con_base, maestros_a_asignar, horas_pendientes, dias, horas_ordenadas
    )
    teacher_services = llenar_huecos_servicio(
        horario_con_regulares,
        maestros_a_asignar,
        dias,
        horas_ordenadas,
        grupos,
    )
    maestros_activos_final = {
        " ".join(m["nombre"].split()[:2])
        for m in todos_los_maestros_actuales
        if m.get("nombre")
    }
    generar_excel_completo(
        horario_con_regulares,
        dias,
        horas_ordenadas,
        grupos,
        maestros_activos_final,
        maestros_invalidos,
        horas_pendientes,
        teacher_services,
        maestros_a_asignar,  # Nuevo parámetro
    )
    print("\n--- PROCESO COMPLETADO ---")


def generar_excel_completo(
    horario_final,
    dias,
    horas,
    grupos,
    maestros_activos,
    maestros_invalidos,
    pendientes_final,
    teacher_services,
    maestros_a_asignar,  # Nuevo parámetro
    archivo_salida="horario_completo_generado.xlsx",
):
    print(f"\nGenerando archivo Excel con múltiples hojas: {archivo_salida}...")
    with pd.ExcelWriter(archivo_salida, engine="openpyxl") as writer:
        if maestros_invalidos:
            pd.DataFrame(maestros_invalidos).to_excel(
                writer, sheet_name="Maestros con Datos Inválidos", index=False
            )
            print("  -> Hoja 'Maestros con Datos Inválidos' creada.")
        df_data, filas_index_general = (
            [],
            [f"{dia} | {hora}" for dia in dias for hora in horas],
        )
        for dia in dias:
            for hora in horas:
                fila = {
                    g: f"{c['materia']}\n{c['maestro']}" if c else ""
                    for g, c in ((g, horario_final[dia][hora].get(g)) for g in grupos)
                }
                df_data.append(fila)
        pd.DataFrame(df_data, index=filas_index_general, columns=grupos).to_excel(
            writer, sheet_name="Horario General por Grupo"
        )
        print("  -> Hoja 'Horario General por Grupo' creada.")
        dias_map = {
            "LU": "LUNES",
            "MA": "MARTES",
            "MI": "MIÉRCOLES",
            "JU": "JUEVES",
            "VI": "VIERNES",
        }
        for grupo in grupos:
            df_horario_data = {
                "Hora": [h.split("/")[1].strip() for h in horas],
                **{dias_map[d]: [] for d in dias_map},
            }
            for dia_cod in dias_map:
                for hora in horas:
                    clase = horario_final[dia_cod][hora].get(grupo)
                    df_horario_data[dias_map[dia_cod]].append(
                        clase["materia"] if clase else ""
                    )
            df_horario = pd.DataFrame(df_horario_data).set_index("Hora")
            df_horario.to_excel(writer, sheet_name=f"Grupo {grupo}")
            resumen_data = []
            ano = grupo[0]
            if ano in HORAS_POR_ANO:
                for materia, req in HORAS_POR_ANO[ano].items():
                    materia_norm = normalizar_materia(materia)
                    faltantes = pendientes_final.get(grupo, {}).get(materia_norm, 0)
                    if faltantes > 0:
                        resumen_data.append(
                            {
                                "Materia": materia.upper(),
                                "Horas Faltantes": faltantes,
                            }
                        )
            if resumen_data:
                pd.DataFrame(resumen_data).to_excel(
                    writer,
                    sheet_name=f"Grupo {grupo}",
                    startrow=len(df_horario) + 3,
                    index=False,
                )
        print(f"  -> {len(grupos)} hojas de horarios por grupo (con resumen) creadas.")
        for maestro_nombre in sorted(list(maestros_activos)):
            df_maestro_data = {
                "Hora": [h.split("/")[1].strip() for h in horas],
                **{dias_map[d]: [] for d in dias_map},
            }
            # Nuevo: Calcular horas asignadas
            horas_asignadas_clase = 0
            horas_asignadas_tutoria = 0
            horas_asignadas_servicio = 0
            for dia_cod in dias_map:
                for hora in horas:
                    actividad = ""
                    for grupo in grupos:
                        clase = horario_final[dia_cod][hora].get(grupo)
                        if clase and clase["maestro"] == maestro_nombre:
                            if clase["materia"] == "TUTORIA":
                                horas_asignadas_tutoria += 1
                            else:
                                horas_asignadas_clase += 1
                            actividad = f"{clase['materia']}\n({grupo})"
                            break
                    if not actividad:
                        # Verificar si hay servicio o integración asignado en este slot
                        services = teacher_services.get(maestro_nombre, {}).get(
                            dia_cod, set()
                        )
                        for s_hora, s_tipo in services:
                            if s_hora == hora:
                                actividad = s_tipo
                                if s_tipo == "SERVICIO":
                                    horas_asignadas_servicio += 1
                                break
                    df_maestro_data[dias_map[dia_cod]].append(actividad)
            df_maestro = pd.DataFrame(df_maestro_data).set_index("Hora")
            # Nuevo: Agregar resumen de horas
            matching_maestros = [
                m
                for m in maestros_a_asignar
                if " ".join(m["nombre"].split()[:2]) == maestro_nombre
            ]
            horas_req_grupo = sum(m.get("horas_grupo", 0) for m in matching_maestros)
            horas_req_tutoria = sum(
                m.get("horas_tutoria", 0) or 0 for m in matching_maestros
            )
            horas_req_servicio = sum(
                m.get("horas_servicio", 0) or 0 for m in matching_maestros
            )
            horas_req_total = sum(m.get("total", 0) or 0 for m in matching_maestros)
            resumen_data = {
                "Tipo": ["Horas Grupo", "Horas Tutoria", "Horas Servicio", "Total"],
                "Requeridas": [
                    horas_req_grupo,
                    horas_req_tutoria,
                    horas_req_servicio,
                    horas_req_total,
                ],
                "Asignadas": [
                    horas_asignadas_clase,
                    horas_asignadas_tutoria,
                    horas_asignadas_servicio,
                    horas_asignadas_clase
                    + horas_asignadas_tutoria
                    + horas_asignadas_servicio,
                ],
            }
            df_resumen = pd.DataFrame(resumen_data)
            # Escribir horario y resumen en la hoja
            df_maestro.to_excel(writer, sheet_name=f"Maestro {maestro_nombre}")
            df_resumen.to_excel(
                writer,
                sheet_name=f"Maestro {maestro_nombre}",
                startrow=len(df_maestro) + 3,
                index=False,
            )
        print(
            f"  -> {len(maestros_activos)} hojas de horarios por maestro creadas (con resumen de horas)."
        )
    print("¡Archivo Excel completo generado con éxito!")


if __name__ == "__main__":
    main()
