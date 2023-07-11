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
        0:"Lunes",
        1:"Martes",
        2:"Miercoles",
        3:"Jueves",
        4:"Viernes",
    }
    
    return dias.get(num, None)

def print_horario(d):
    headers = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    table_data = []
    
    max_rows = max(len(d[key]) for key in d)
    
    for key in d:
        while len(d[key]) < max_rows:
            d[key].append("")
    
    for i in range(max_rows):
        row = [d[key][i] for key in headers]
        table_data.append(row)
    
    print(tabulate(table_data, headers=headers))
    print()

horas_1ero={
        "español":5,
        "ingles":3,
        "matematicas":5,
        "ciencia":4, # biologia
        "historia":2,
        "geografia":4,
        "civica":2,
        "artes":3,
        "tutoria":1,
        "ef":2,
            }

horas_2do={
        "español":5,
        "ingles":3,
        "matematicas":5,
        "ciencia":6, # fisica
        "historia":4,
        "civica":2,
        "artes":3,
        "tutoria":1,
        "ef":2,
            }

horas_3ero={
        "español":5,
        "ingles":3,
        "matematicas":5,
        "ciencia":6, # Quimica
        "historia":4,
        "civica":2,
        "artes":3,
        "ef":2,
        "tutoria":1,
            }

#for grupo in ["1A","1B","1C","1D","1E","1F","1G","2A","2B","2C","2D","2E","2F","3A","3B","3C","3D","3E","3F"]:
grupos_horarios={}
maestros_horarios={}
for grupo in grupos_maestro:
    maestros_grupo_actual=[]
    grupos_horarios[grupo]={
            "Lunes":[],
            "Martes":[],
            "Miercoles":[],
            "Jueves":[],
            "Viernes":[],
            }

    for prof in Profs: # Encontramos los maestros de este grupo
        if prof.nombre in grupos_maestro[grupo].values():
            maestros_grupo_actual.append(prof)

    for maestro in maestros_grupo_actual:
        if maestro.p:
            if maestro.nombre in maestros_horarios:
                _=0 # TODO Ordenar cuando ya esta en el horario
            else:
                maestros_horarios[maestro.nombre]={
                    "Lunes":[f"{i}" for i in range(7)],
                    "Martes":["" for _ in range(7)],
                    "Miercoles":["" for _ in range(7)],
                    "Jueves":["" for _ in range(7)],
                    "Viernes":["" for _ in range(7)],
                        }
                d = 0 # Dia actual
                grupo = 0
                for dia in maestro.horarios:
                    print(num_to_dia(d))
                    print(dia)
                    #for g in maestro.grupos:
                    for hora in range(len(dia)):
                        if dia[hora]==0:continue
                        maestros_horarios[maestro.nombre][num_to_dia(d)][dia[hora]-1]+=maestro.grupos[grupo] # Asignar grupo
                        hora+=1
                        print(hora, len(dia))
                        grupo+=1
                        if grupo== len(maestro.grupos):
                            grupo=0
                    d+=1 #Avanzamos un dia
                    
for m in maestros_horarios:
    print(m)
    print_horario(maestros_horarios[m])
