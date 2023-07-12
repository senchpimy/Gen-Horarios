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
    grupos_horarios[grupo]={
            "Lunes":["" for _ in range(7)],
            "Martes":["" for _ in range(7)],
            "Miercoles":["" for _ in range(7)],
            "Jueves":["" for _ in range(7)],
            "Viernes":["" for _ in range(7)],
        }

for grupo in grupos_maestro:
    maestros_grupo_actual=[]

    for prof in Profs: # Encontramos los maestros de este grupo
        if prof.nombre in grupos_maestro[grupo].values():
            maestros_grupo_actual.append(prof)

    for maestro in maestros_grupo_actual:
        if maestro.p:
            if maestro.nombre in maestros_horarios:
                _=0 # TODO Ordenar cuando ya esta en el horario
            else:
                maestros_horarios[maestro.nombre]={
                    "Lunes":["_" for _ in range(7)],
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
                        if len(grupos_horarios[maestro.grupos[grupo]][num_to_dia(d)][dia[hora]-1])<2:
                            maestros_horarios[maestro.nombre][num_to_dia(d)][dia[hora]-1]+=maestro.grupos[grupo] # Asignar grupo
                            #print(grupos_horarios[maestro.grupos[grupo]][num_to_dia(d)][dia[hora]-1],"AAA")
                            grupos_horarios[maestro.grupos[grupo]][num_to_dia(d)][dia[hora]-1]+=maestro.materia
                            hora+=1
                            print(hora, len(dia))
                            grupo+=1
                            if grupo== len(maestro.grupos):
                                grupo=0
                        else:
                            _=0 # TODO Hacer algo cuando el lugar en el grupo en cierta hora esta ocupado
                    d+=1 #Avanzamos un dia

# Contamos las horas de materia por grupo Y eliminamos las extras
vel = "1A"
val = grupos_horarios[vel].copy()
for g in grupos_horarios:
    _=0
    horas={}
    match g[0]:
        case '1':
            horas=horas_1ero.copy()
        case "2":
            horas=horas_2do.copy()
        case "3":
            horas=horas_3ero.copy()
    for m in grupos_horarios[g]:
        #m: dia
        for hora in grupos_horarios[g][m]:
            if horas.get(hora)!=None:
                horas[hora]-=1
    for materia in horas:
        #g: grupo
        if horas[materia]<0: # Quitamos horas a la materia que se pasan
            semana_actual=[0 for _ in range(5)]
            dia_actual=0
            for dia in grupos_horarios[g]: # Contamos los dias que contengan 
                for hora in grupos_horarios[g][dia]:
                    #print(hora,"Hora", dia)
                    if hora == materia:
                        semana_actual[dia_actual]+=1
                dia_actual+=1
                
                #print(semana_actual,"AHAHAHA", grupos_horarios[g],"LALALALAL", materia)
            unicos=False
            for dia in semana_actual:
                if dia>1:
                    unicos=True

            if unicos:
                for index in range(horas[materia],0): # Si todos los dias tienen solo un unico dia quitamos desde atras
                    m = list(grupos_horarios[g].keys())[index]
                    try:
                        i = grupos_horarios[g][m].index(materia)
                        #grupos_horarios[g][m][i]=""
                    except:
                        pass
                    _=0
            else:
                for dia in semana_actual:
                    pass
    print(horas)

# Imprimimos

print_horario(grupos_horarios[vel])
print_horario(val)

#for m in maestros_horarios:
#    print(m)
#    print_horario(maestros_horarios[m])
## Imprimir grupos
#for g in grupos_horarios:
#    print(g)
#    print_horario(grupos_horarios[g])
