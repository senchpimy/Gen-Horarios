from profesor import profesores as Profs
from profesor import grupos_maestro
from tabulate import tabulate

print("\n")


def dia_to_num(dia):
    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miercoles": 2,
        "Jueves": 3,
        "Viernes": 4,
    }

    return dias.get(dia.capitalize(), None)


def num_to_dia(num):
    dias = {
        0: "Lunes",
        1: "Martes",
        2: "Miercoles",
        3: "Jueves",
        4: "Viernes",
    }

    return dias.get(num, None)


def print_horario(d):
    headers = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    table_data = []

    max_rows = max(len(d[key]) for key in d)

    for key in d:
        while len(d[key]) < max_rows:
            d[key].append("")

    n = 0
    for i in range(max_rows):
        row = [d[key][i] for key in headers]
        table_data.append([i + 1] + row)
        n += 1

    print(tabulate(table_data, headers=["Hora"] + headers))
    print()


horas_1ero = {
    "español": 5,
    "artes": 3,
    "ingles": 3,
    "matematicas": 5,
    "ciencias": 4,  # biologia
    "historia": 2,
    "geografia": 4,
    "civica": 2,
    "tutoria": 1,
    "ef": 2,
}

horas_2do = {
    "español": 5,
    "artes": 3,
    "ingles": 3,
    "matematicas": 5,
    "ciencias": 6,  # fisica
    "historia": 4,
    "civica": 2,
    "tutoria": 1,
    "ef": 2,
}

horas_3ero = {
    "español": 5,
    "artes": 3,
    "ingles": 3,
    "matematicas": 5,
    "ciencias": 6,  # Quimica
    "historia": 4,
    "civica": 2,
    "ef": 2,
    "tutoria": 1,
}

horas_grupos = {}
grupos_horarios = {}
maestros_horarios = {}
# for grupo in ["1A","1B","1C","1D","1E","1F","1G","2A","2B","2C","2D","2E","2F","3A","3B","3C","3D","3E","3F"]:
for grupo in grupos_maestro:
    grupos_horarios[grupo] = {
        "Lunes": ["" for _ in range(7)],
        "Martes": ["" for _ in range(7)],
        "Miercoles": ["" for _ in range(7)],
        "Jueves": ["" for _ in range(7)],
        "Viernes": ["" for _ in range(7)],
    }


def horas_de_materia_grupo():
    for g in grupos_horarios:
        horas_grupos[g] = {}
        horas = {}
        match g[0]:
            case "1":
                horas = horas_1ero.copy()
            case "2":
                horas = horas_2do.copy()
            case "3":
                horas = horas_3ero.copy()
        for dia in grupos_horarios[g]:
            for clase in grupos_horarios[g][dia]:
                if clase == "tecnologia":
                    continue
                if clase != "":
                    horas[clase] -= 1
        horas_grupos[g] = horas


# Agregamos todos los maestros a la lista
for prof in Profs:
    maestros_horarios[prof.nombre] = {
        "Lunes": ["" for _ in range(7)],
        "Martes": ["" for _ in range(7)],
        "Miercoles": ["" for _ in range(7)],
        "Jueves": ["" for _ in range(7)],
        "Viernes": ["" for _ in range(7)],
    }

# Agregamos los talleres
keys = {
    "1A": "1sec1",
    "1B": "1sec1",
    "1C": "1sec1",
    "1D": "1sec2",
    "1E": "1sec2",
    "1F": "1sec2",
    "1G": "1sec2",
    "2A": "2sec1",
    "2B": "2sec1",
    "2C": "2sec1",
    "2D": "2sec2",
    "2E": "2sec2",
    "2F": "2sec2",
    "3A": "3sec1",
    "3B": "3sec1",
    "3C": "3sec1",
    "3D": "3sec2",
    "3E": "3sec2",
    "3F": "3sec2",
}
for g in grupos_horarios:
    match keys[g]:
        case "1sec1":
            grupos_horarios[g]["Lunes"][4] = "tecnologia"
            grupos_horarios[g]["Lunes"][5] = "tecnologia"
            grupos_horarios[g]["Lunes"][6] = "tecnologia"
        case "1sec2":
            grupos_horarios[g]["Martes"][4] = "tecnologia"
            grupos_horarios[g]["Martes"][5] = "tecnologia"
            grupos_horarios[g]["Martes"][6] = "tecnologia"
        case "2sec1":
            grupos_horarios[g]["Miercoles"][4] = "tecnologia"
            grupos_horarios[g]["Miercoles"][5] = "tecnologia"
            grupos_horarios[g]["Miercoles"][6] = "tecnologia"
        case "2sec2":
            grupos_horarios[g]["Jueves"][4] = "tecnologia"
            grupos_horarios[g]["Jueves"][5] = "tecnologia"
            grupos_horarios[g]["Jueves"][6] = "tecnologia"
        case "3sec1":
            grupos_horarios[g]["Viernes"][1] = "tecnologia"
            grupos_horarios[g]["Viernes"][2] = "tecnologia"
            grupos_horarios[g]["Viernes"][3] = "tecnologia"
        case "3sec2":
            grupos_horarios[g]["Viernes"][4] = "tecnologia"
            grupos_horarios[g]["Viernes"][5] = "tecnologia"
            grupos_horarios[g]["Viernes"][6] = "tecnologia"

# Ordenamos a los maestros con preferencia
for maestro in Profs:
    if not maestro.p:
        continue
    if maestro.materia == "tecnologia":
        continue
    for g in maestro.grupos:
        horas = {}
        match g[0]:
            case "1":
                horas = horas_1ero.copy()
            case "2":
                horas = horas_2do.copy()
            case "3":
                horas = horas_3ero.copy()
        if horas[maestro.materia] > 5:
            assig = False
            for dia2 in grupos_horarios[g]:
                if assig:
                    break
                for index, clase in enumerate(grupos_horarios[g][dia2]):
                    try:
                        if (
                            grupos_horarios[g][dia2][index]
                            == grupos_horarios[g][dia2][index + 1]
                            == ""
                        ):
                            if (
                                maestros_horarios[maestro.nombre][dia2][index]
                                == maestros_horarios[maestro.nombre][dia2][index + 1]
                                == ""
                            ):
                                if (
                                    index + 1 in maestro.horarios[dia_to_num(dia2)]
                                    and index + 2 in maestro.horarios[dia_to_num(dia2)]
                                ):
                                    maestros_horarios[maestro.nombre][dia2][
                                        index + 1
                                    ] += g
                                    maestros_horarios[maestro.nombre][dia2][index] += g
                                    grupos_horarios[g][dia2][index] += maestro.materia
                                    grupos_horarios[g][dia2][index + 1] += (
                                        maestro.materia
                                    )
                                    assig = True
                                    break
                    except:
                        pass
            for i in range(horas[maestro.materia] - 2):
                assig2 = False
                dia_ind = 0
                for dia in maestro.horarios:
                    if assig2:
                        break
                    for clase in dia:
                        if dia_ind == 5:
                            dia_ind = 0
                        if maestro.materia in grupos_horarios[g][num_to_dia(dia_ind)]:
                            dia_ind += 1
                            continue
                        if (
                            grupos_horarios[g][num_to_dia(dia_ind)][clase - 1]
                            == ""
                            == maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                clase - 1
                            ]
                        ):
                            grupos_horarios[g][num_to_dia(dia_ind)][clase - 1] += (
                                maestro.materia
                            )
                            maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                clase - 1
                            ] += g
                            dia_ind += 1
                            assig2 = True
                            break
        else:
            for i in range(horas[maestro.materia]):
                assig = False
                dia_ind = 0
                for dia in maestro.horarios:
                    if assig:
                        break
                    for clase in dia:
                        if dia_ind == 5:
                            dia_ind = 0
                        if maestro.materia in grupos_horarios[g][num_to_dia(dia_ind)]:
                            dia_ind += 1
                            continue
                        if (
                            grupos_horarios[g][num_to_dia(dia_ind)][clase - 1]
                            == ""
                            == maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                clase - 1
                            ]
                        ):
                            grupos_horarios[g][num_to_dia(dia_ind)][clase - 1] += (
                                maestro.materia
                            )
                            maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                clase - 1
                            ] += g
                            dia_ind += 1
                            assig = True
                            break


def agregar_maestros():
    for maestro in Profs:
        if maestro.p or maestro.materia == "tecnologia" or maestro.materia == None:
            continue
        for g in maestro.grupos:
            horas = {}
            match g[0]:
                case "1":
                    horas = horas_1ero.copy()
                case "2":
                    horas = horas_2do.copy()
                case "3":
                    horas = horas_3ero.copy()
            if horas[maestro.materia] > 5:
                assig = False
                for dia2 in grupos_horarios[g]:
                    if assig:
                        break
                    for index, clase in enumerate(grupos_horarios[g][dia2]):
                        try:
                            if (
                                grupos_horarios[g][dia2][index]
                                == grupos_horarios[g][dia2][index + 1]
                                == ""
                            ):
                                if (
                                    maestros_horarios[maestro.nombre][dia2][index]
                                    == maestros_horarios[maestro.nombre][dia2][
                                        index + 1
                                    ]
                                    == ""
                                ):
                                    if (
                                        index + 1 in maestro.horarios[dia_to_num(dia2)]
                                        and index + 2
                                        in maestro.horarios[dia_to_num(dia2)]
                                    ):
                                        maestros_horarios[maestro.nombre][dia2][
                                            index + 1
                                        ] += g
                                        maestros_horarios[maestro.nombre][dia2][
                                            index
                                        ] += g
                                        grupos_horarios[g][dia2][index] += (
                                            maestro.materia
                                        )
                                        grupos_horarios[g][dia2][index + 1] += (
                                            maestro.materia
                                        )
                                        assig = True
                                        break
                        except:
                            pass
                for i in range(horas[maestro.materia] - 2):
                    assig2 = False
                    dia_ind = 0
                    for dia in maestro.horarios:
                        if assig2:
                            break
                        for clase in dia:
                            if dia_ind == 5:
                                dia_ind = 0
                            if (
                                maestro.materia
                                in grupos_horarios[g][num_to_dia(dia_ind)]
                            ):
                                dia_ind += 1
                                continue
                            if (
                                grupos_horarios[g][num_to_dia(dia_ind)][clase - 1]
                                == ""
                                == maestros_horarios[maestro.nombre][
                                    num_to_dia(dia_ind)
                                ][clase - 1]
                            ):
                                grupos_horarios[g][num_to_dia(dia_ind)][clase - 1] += (
                                    maestro.materia
                                )
                                maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                    clase - 1
                                ] += g
                                dia_ind += 1
                                assig2 = True
                                break
            else:
                for i in range(horas[maestro.materia]):
                    assig = False
                    dia_ind = 0
                    for dia in maestro.horarios:
                        if assig:
                            break
                        for clase in dia:
                            if dia_ind == 5:
                                dia_ind = 0
                            if (
                                maestro.materia
                                in grupos_horarios[g][num_to_dia(dia_ind)]
                            ):
                                dia_ind += 1
                                continue
                            if (
                                grupos_horarios[g][num_to_dia(dia_ind)][clase - 1]
                                == ""
                                == maestros_horarios[maestro.nombre][
                                    num_to_dia(dia_ind)
                                ][clase - 1]
                            ):
                                grupos_horarios[g][num_to_dia(dia_ind)][clase - 1] += (
                                    maestro.materia
                                )
                                maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][
                                    clase - 1
                                ] += g
                                dia_ind += 1
                                assig = True
                                break


agregar_maestros()
## Acomodar las tutorias con preferencia
for maestro in Profs:
    if maestro.p:
        if maestro.tutoria != None:
            assig = False
            for dia in grupos_horarios[maestro.tutoria]:
                if assig:
                    break
                clase_ind = 0
                for clase in grupos_horarios[maestro.tutoria][dia]:
                    if (
                        clase == ""
                        and maestros_horarios[maestro.nombre][dia][clase_ind] == ""
                        and clase_ind + 1 in maestro.horarios[dia_to_num(dia)]
                    ):
                        maestros_horarios[maestro.nombre][dia][clase_ind] += (
                            maestro.tutoria + "(tutoria)"
                        )
                        grupos_horarios[maestro.tutoria][dia][clase_ind] += "tutoria"
                        assig = True
                        break
                    clase_ind += 1


# Agregamos al resto de los maestros
horas_de_materia_grupo()
for g in horas_grupos:
    for materia in horas_grupos[g]:
        if materia == "tutoria":
            continue
        for i in range(horas_grupos[g][materia]):
            mae = list(filter(lambda p: p.materia == materia and g in p.grupos, Profs))[
                0
            ]
            assig = False
            for dia in maestros_horarios[mae.nombre]:
                if mae.materia in grupos_horarios[g][dia]:
                    continue
                if assig:
                    break
                clase_ind = 0
                for clase in maestros_horarios[mae.nombre][dia]:
                    if clase == "" and grupos_horarios[g][dia][clase_ind] == "":
                        assig = True
                        maestros_horarios[mae.nombre][dia][clase_ind] += g
                        grupos_horarios[g][dia][clase_ind] += mae.materia
                        break
                    clase_ind += 1

# Agregamos las tutorias
for maestro in Profs:
    if maestro.tutoria != None:
        for dia in grupos_horarios[maestro.tutoria]:
            clase_ind = 0
            for clase in grupos_horarios[maestro.tutoria][dia]:
                horas_de_materia_grupo()
                if (
                    clase == maestros_horarios[maestro.nombre][dia][clase_ind] == ""
                    and horas_grupos[maestro.tutoria]["tutoria"] == 1
                ):
                    grupos_horarios[maestro.tutoria][dia][clase_ind] = "tutoria"
                    maestros_horarios[maestro.nombre][dia][clase_ind] = (
                        maestro.tutoria + "(tutoria)"
                    )
                clase_ind += 1

# Corregir cuando el maestro solo tiene una clse por dia
# def corregir():
#    for m in maestros_horarios:
#        for dia in maestros_horarios[m]:
#            total=0
#            grupo = ""
#            for clase in maestros_horarios[m][dia]:
#                if clase == "":
#                    total+=1
#                else: grupo=clase
#            if total == 6: pass #Dia con solo una clase detectado
# corregir()

horas_de_materia_grupo()
for g in grupos_horarios:
    print(g)
    print_horario(grupos_horarios[g])
    print(horas_grupos[g])
