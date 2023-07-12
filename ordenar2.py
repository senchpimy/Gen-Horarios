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
    
    n=0
    for i in range(max_rows):
        row = [d[key][i] for key in headers]
        table_data.append([i+1]+row)
        n+=1
    
    print(tabulate(table_data, headers=["Hora"]+headers))
    print()

horas_1ero={
        "español":5,
        "ingles":3,
        "matematicas":5,
        "ciencias":4, # biologia
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
        "ciencias":6, # fisica
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
        "ciencias":6, # Quimica
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
#grupo_actual=0
for grupo in grupos_maestro:
    s = grupo
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
                    "Lunes":["" for _ in range(7)],
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
                            grupos_horarios[maestro.grupos[grupo]][num_to_dia(d)][dia[hora]-1]+=maestro.materia
                            hora+=1
                            print(hora, len(dia))
                            grupo+=1
                            if grupo== len(maestro.grupos):
                                grupo=0
                        else:
                            pass # TODO Hacer algo cuando el lugar en el grupo en cierta hora esta ocupado
                    d+=1 #Avanzamos un dia

# Agregamos los que faltaron
def agregar():
    for g in grupos_horarios:
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
           if horas[materia]==1 and materia != "tutoria":
                maestro = list(filter(lambda p: p.materia==materia and g in p.grupos, Profs))[0]
                print_horario(grupos_horarios[g])
                for l in range(len(grupos_horarios[g])):
                    if maestro.materia not in grupos_horarios[g][num_to_dia(l)]:
                        for h in maestro.horarios[l]:
                            if maestros_horarios[maestro.nombre][num_to_dia(l)][h-1]=="":
                                maestros_horarios[maestro.nombre][num_to_dia(l)][h-1]=g
                                grupos_horarios[g][num_to_dia(l)][h-1]=maestro.materia

agregar()

# Contamos las horas de materia por grupo Y eliminamos las extras
def eliminar_repetidos():
    for g in grupos_horarios:
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
        print(horas, g)
        for materia in horas:
            #g: grupo
            if horas[materia]<0: # Quitamos horas a la materia que se pasan
                semana_actual=[0 for _ in range(5)]
                dia_actual=0
                for dia in grupos_horarios[g]: # Contamos los dias que contengan 
                    for hora in grupos_horarios[g][dia]:
                        if hora == materia:
                            semana_actual[dia_actual]+=1
                    dia_actual+=1
                    
                unicos=True
                for dia in semana_actual:
                    if dia>1:
                        unicos=False
    
                if unicos:
                    #print("Unicos valores")
                    for index in range(horas[materia],0): # Si todos los dias tienen solo un unico dia quitamos desde atras
                        m = list(grupos_horarios[g].keys())[index]
                        try:
                            i = grupos_horarios[g][m].index(materia)
                            grupos_horarios[g][m][i]="" # Eliminamos el elemento que se repite
                            maestro = list(filter(lambda person: person.materia == materia and g in person.grupos, Profs))[0]
                            maestros_horarios[maestro.nombre][m][i]="" # Eliminamos el elemento que se repite
                        except:
                            pass
                else:
                    ind = 0
                    for dia in semana_actual:
                        if dia > 1:
                            li = grupos_horarios[g][num_to_dia(ind)]
                            indice= len(li) - 1 - li[::-1].index(materia) # Encontramos el indice del ultimo elemento en el mismo dia
                            grupos_horarios[g][num_to_dia(ind)][indice]="" # Lo eliminamos
                            maestro = list(filter(lambda person: person.materia == materia and g in person.grupos, Profs))[0]
                            maestros_horarios[maestro.nombre][num_to_dia(ind)][indice]="" # Lo eliminamos
                        ind+=1
# Repetimos el Proceso dos veces para evitar cualquier posible error
eliminar_repetidos()
print()
eliminar_repetidos()
print()
eliminar_repetidos()


# Añadimos los talleres
HORAS_TALLER = 3
taller = {}

for j in range(1,4):
    key=""
    for l in "ABCDEFGH":
        momentos_posibles={
        "Lunes":[0 for _ in range(7)],
        "Martes":[0 for _ in range(7)],
        "Miercoles":[0 for _ in range(7)],
        "Jueves":[0 for _ in range(7)],
        "Viernes":[0 for _ in range(7)]
        }
        if l in ['A', 'B', 'C']:
            key = f'{j}sec1'
        elif l in ['D', 'E', 'F', 'G', 'H']:
            key = f'{j}sec2'
        taller[key] = momentos_posibles

horas_taller={}
for key in taller:
    horas_taller[key]=HORAS_TALLER

# Contamos los espacios disponibles
for g in grupos_horarios:
    key=""
    espacios_requeridos=0
    if g[1] in ['A', 'B', 'C']:
        key = f'{g[0]}sec1'
        espacios_requeridos=3
    elif g[1] in ['D', 'E', 'F', 'G',]:
        key = f'{g[0]}sec2'
        espacios_requeridos=3
        if g[0]=="1":
            espacios_requeridos=4
    for j in range(5):
        for hora in range(7):
            if grupos_horarios[g][num_to_dia(j)][hora]=="":
                taller[key][num_to_dia(j)][hora]+=1

    for j in range(5):
        for hora in taller[key][num_to_dia(j)][4:]:
            if espacios_requeridos ==hora:
                horas_taller[key]-=1
                #grupos_horarios[g][num_to_dia(j)][hora]="tecnologia"
                #print(f"Hora posible {key}",horas_taller[key])

print(taller)
print()
print(horas_taller)

taller_grupos={
    "Lunes":["" for _ in range(7)],
    "Martes":["" for _ in range(7)],
    "Miercoles":["" for _ in range(7)],
    "Jueves":["" for _ in range(7)],
    "Viernes":["" for _ in range(7)],
}


for key in taller: # Ordenar
    espacios_requeridos=3
    if key[0] == "1" and key[-1]=="2":
        espacios_requeridos=4

    if horas_taller[key]<=0:
        t = HORAS_TALLER
        for dia in taller[key]:
            for ind,hora in enumerate(taller[key][dia]):
                #if hora == espacios_requeridos and taller_grupos[dia][ind]=="":
                if hora == espacios_requeridos and ind > 3 and t>0 and taller_grupos[dia][ind]=="":
                    t-=1
                    print(horas_taller[key])
                    taller_grupos[dia][ind]+=key


# Ordenar los 3ros
f = 0
l="3F"
for g in grupos_horarios:
    if g[0]=="3":
        if g[1] in "ABCD":
            for clase in range(1,4): # Las primeras horas para los primeros grupos
                grupos_horarios[g]["Viernes"][clase]="tecnologia"
                taller_grupos["Viernes"][clase]="3sec1"
        else:
            n = 4
            for clase in grupos_horarios[g]["Viernes"][4:]: # Las segundas horas para los que quedan
                if clase!= "":
                    maestro = list(filter(lambda p: p.materia==clase and g in p.grupos, Profs))[0]
                    d_ind=0
                    for dia in maestro.horarios:
                        for clase in dia:
                            if maestros_horarios[maestro.nombre][num_to_dia(d_ind)][clase-2]=="":
                                if maestros_horarios[maestro.nombre][num_to_dia(d_ind)][clase-1]==g: # Hacer horas dobles
                                    maestros_horarios[maestro.nombre][num_to_dia(d_ind)][clase-2]=g
                                    maestros_horarios[maestro.nombre]["Viernes"][n]=""
                                    grupos_horarios[g]["Viernes"][n]="" # Eliminamos la clase
                                    f = maestro
                                    grupos_horarios[g][num_to_dia(d_ind)][clase-2]+=maestro.materia
                                    pass
                        d_ind+=1
                n+=1
# Movimiento manual 
maestros_horarios[f.nombre]["Viernes"][4]=""
maestros_horarios[f.nombre]["Miercoles"][6]=l
grupos_horarios[l]["Viernes"][4]=""
grupos_horarios[l]["Miercoles"][6]+=f.materia

for l in "EF":
    for i in range(4,7):
        taller_grupos["Viernes"][i]="3sec2"
        #grupos_horarios[f"3{l}"][i]="tecnologia"

print_horario(taller_grupos)

#for m in maestros_horarios:
#    print(m)
#    print_horario(maestros_horarios[m])
## Imprimir grupos
#for g in grupos_horarios:
#    print(g)
#    print_horario(grupos_horarios[g])
