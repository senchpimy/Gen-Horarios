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
horas_grupos={}
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
        horas_grupos[g]=horas
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
        if g[1] in "ABC":
            for clase in range(1,4): # Las primeras horas para los primeros grupos
                if grupos_horarios[g]["Viernes"][clase]=="":
                    grupos_horarios[g]["Viernes"][clase]+="tecnologia"
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

grupos_horarios["3D"]["Jueves"][4]="artes"
grupos_horarios["3D"]["Jueves"][6]=""
maestro_tmp = list(filter(lambda p: p.materia=="artes" and "3D" in p.grupos, Profs))[0]
maestros_horarios[maestro_tmp.nombre]["Jueves"][4]="3D"
maestros_horarios[maestro_tmp.nombre]["Miercoles"][6]=""
maestros_horarios[maestro_tmp.nombre]["Jueves"][6]=""

keys = {
        "1A":"1sec1",
        "1B":"1sec1",
        "1C":"1sec1",
        "1D":"1sec2",
        "1E":"1sec2",
        "1F":"1sec2",
        "1G":"1sec2",
        "2A":"2sec1",
        "2B":"2sec1",
        "2C":"2sec1",
        "2D":"2sec2",
        "2E":"2sec2",
        "2F":"2sec2",
        "3A":"3sec1",
        "3B":"3sec1",
        "3C":"3sec1",
        "3D":"3sec2",
        "3E":"3sec2",
        "3F":"3sec2",
        }

for g in grupos_horarios:
    for dia in taller_grupos:
        n = 0
        for clase in taller_grupos[dia]:
            if clase==keys[g]:
                grupos_horarios[g][dia][n]="tecnologia"
            n+=1

for l in "DEF":
    for i in range(4,7):
        taller_grupos["Viernes"][i]="3sec2"
        grupos_horarios[f"3{l}"]["Viernes"][i]="tecnologia"

# Acomodar las tutorias con preferencia
for maestro in Profs:
    if maestro.p:
        brea = False
        if maestro.tutoria!=None:
            di_ind= 0
            for dia in maestro.horarios:
                for clase in dia: 
                    if maestros_horarios[maestro.nombre][num_to_dia(di_ind)][clase-1]=="":
                        brea = True
                        print(clase, "AA", num_to_dia(di_ind), maestro.nombre)
                        grupos_horarios[maestro.tutoria][num_to_dia(di_ind)][clase-1]="tutoria"
                        maestros_horarios[maestro.nombre][num_to_dia(di_ind)][clase-1]=maestro.tutoria+"(tutoria)"
                if brea: break
                di_ind += 1

# Agregamos al resto de los maestros
for g in grupos_horarios:
    maestros_grupo_actual=[]
    horas = {}
    match g[0]:
        case '1':
            horas=horas_1ero.copy()
        case "2":
            horas=horas_2do.copy()
        case "3":
            horas=horas_3ero.copy()
    for dia in grupos_horarios[g]:
        for clase in grupos_horarios[g][dia]:
            if clase == "tecnologia":continue
            if clase != "":
                horas[clase]-=1

    horas_grupos[g]=horas

for prof in Profs:
    if prof.nombre not in maestros_horarios:
        maestros_horarios[prof.nombre]={
    "Lunes":["" for _ in range(7)],
    "Martes":["" for _ in range(7)],
    "Miercoles":["" for _ in range(7)],
    "Jueves":["" for _ in range(7)],
    "Viernes":["" for _ in range(7)],
                }

for g in grupos_maestro:
    maestros_grupo_actual=[]
    horas = horas_grupos[g]

    for prof in Profs: # Encontramos los maestros de este grupo
        if prof.nombre in grupos_maestro[g].values():
            maestros_grupo_actual.append(prof)

    for materia in horas:
        m = 0
        br = True
        for ma in maestros_grupo_actual:
            if ma.materia == materia:
                m = ma
                br = False
        if br:break
        for j in range(horas[materia]):
            agg = False
            n = 0
            #print(horas[materia], materia, "AAAA", g )
            for dia in m.horarios:
                for clase in dia:
                    clase = clase -1
                    if agg: break
                    if  maestros_horarios[m.nombre][num_to_dia(n)][clase]=="" and grupos_horarios[g][num_to_dia(n)][clase]=="":
                        maestros_horarios[m.nombre][num_to_dia(n)][clase]+=g
                        grupos_horarios[g][num_to_dia(n)][clase]+=m.materia
                        agg=True

                    print(m.nombre, m.materia, dia, num_to_dia(n))
                    pass
                if agg:
                    break
                n +=1

for maestro in maestros_horarios: # Eliminar las veces que hay clases mas de 3 veces al dia o 2 no son seguidas
    for dia in maestros_horarios[maestro]:
        dia_dict = {}
        for clase in maestros_horarios[maestro][dia]:
            try: 
                dia_dict[clase]+=1
            except:
                dia_dict[clase]=1
        for grupo in dia_dict:
            if dia_dict[grupo]>=2 and grupo!="":
                mae = list(filter(lambda p: p.nombre==maestro and grupo in p.grupos, Profs))[0]
                if dia_dict[grupo]==2: # TODO comprobar que las dos horas sean seguidas
                    p = 0
                    for grp in maestros_horarios[mae.nombre][dia]:
                        if maestros_horarios[mae.nombre][dia][p]==grupo:
                            #print(grp, "AAAA")
                            if maestros_horarios[mae.nombre][dia][p]==maestros_horarios[mae.nombre][dia][p+1]:
                                continue
                            else: break
                        p+=1
                    
                for i in range(dia_dict[grupo]-1):
                    contador_horas = 0 
                    for lk in maestros_horarios[mae.nombre][dia]:
                        if lk == grupo:
                            maestros_horarios[mae.nombre][dia][contador_horas]=""
                            grupos_horarios[grupo][dia][contador_horas]=""
                            break
                        contador_horas+=1
                    pass


for g in grupos_horarios:
    maestros_grupo_actual=[]
    horas = {}
    match g[0]:
        case '1':
            horas=horas_1ero.copy()
        case "2":
            horas=horas_2do.copy()
        case "3":
            horas=horas_3ero.copy()
    for dia in grupos_horarios[g]:
        for clase in grupos_horarios[g][dia]:
            if clase == "tecnologia":continue
            if clase != "":
                horas[clase]-=1

    horas_grupos[g]=horas
        #print(m)
# Agregamos los que no se pudieron agregar
#for g in grupos_maestro:
#    maestros_grupo_actual=[]
#    horas = horas_grupos[g]
#
#    for prof in Profs: # Encontramos los maestros de este grupo
#        if prof.nombre in grupos_maestro[g].values():
#            maestros_grupo_actual.append(prof)
#    #

#for m in maestros_horarios:
#    print(m)
#    print_horario(maestros_horarios[m])
#
## Imprimir grupos
for g in grupos_horarios:
    print(g)
    print_horario(grupos_horarios[g])
    print(horas_grupos[g])
