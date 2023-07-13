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
horas_grupos={}
grupos_horarios={}
maestros_horarios={}
#for grupo in ["1A","1B","1C","1D","1E","1F","1G","2A","2B","2C","2D","2E","2F","3A","3B","3C","3D","3E","3F"]:
for grupo in grupos_maestro:
    grupos_horarios[grupo]={
            "Lunes":["" for _ in range(7)],
            "Martes":["" for _ in range(7)],
            "Miercoles":["" for _ in range(7)],
            "Jueves":["" for _ in range(7)],
            "Viernes":["" for _ in range(7)],
        }

def horas_de_materia_grupo():
    for g in grupos_horarios:
        horas_grupos[g]={}
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

# Agregamos todos los maestros a la lista
for prof in Profs:
    maestros_horarios[prof.nombre]={
        "Lunes":["" for _ in range(7)],
        "Martes":["" for _ in range(7)],
        "Miercoles":["" for _ in range(7)],
        "Jueves":["" for _ in range(7)],
        "Viernes":["" for _ in range(7)],
            }

# Agregamos los talleres
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
    match keys[g]:
        case '1sec1':
            grupos_horarios[g]["Lunes"][4]="tecnologia"
            grupos_horarios[g]["Lunes"][5]="tecnologia"
            grupos_horarios[g]["Lunes"][6]="tecnologia"
        case '1sec2':
            grupos_horarios[g]["Martes"][4]="tecnologia"
            grupos_horarios[g]["Martes"][5]="tecnologia"
            grupos_horarios[g]["Martes"][6]="tecnologia"
        case '2sec1':
            grupos_horarios[g]["Miercoles"][4]="tecnologia"
            grupos_horarios[g]["Miercoles"][5]="tecnologia"
            grupos_horarios[g]["Miercoles"][6]="tecnologia"
        case '2sec2':
            grupos_horarios[g]["Jueves"][4]="tecnologia"
            grupos_horarios[g]["Jueves"][5]="tecnologia"
            grupos_horarios[g]["Jueves"][6]="tecnologia"
        case '3sec1':
            grupos_horarios[g]["Viernes"][1]="tecnologia"
            grupos_horarios[g]["Viernes"][2]="tecnologia"
            grupos_horarios[g]["Viernes"][3]="tecnologia"
        case '3sec2':
            grupos_horarios[g]["Viernes"][4]="tecnologia"
            grupos_horarios[g]["Viernes"][5]="tecnologia"
            grupos_horarios[g]["Viernes"][6]="tecnologia"

#Ordenamos a los maestros
for maestro in Profs:
    if not maestro.p: continue
    if maestro.materia=="tecnologia": continue
    for g in maestro.grupos:
        horas={}
        match g[0]:
            case '1':
                horas=horas_1ero.copy()
            case "2":
                horas=horas_2do.copy()
            case "3":
                horas=horas_3ero.copy()
        if horas[maestro.materia]>5:
            # TODO agregar solo una clase de mas
            assig=False
            for dia2 in grupos_horarios[g]:
                if assig:break
                for index, clase in enumerate(grupos_horarios[g][dia2]):
                    try:
                        if grupos_horarios[g][dia2][index] ==  grupos_horarios[g][dia2][index+1]== "":
                            if maestros_horarios[maestro.nombre][dia2][index] == maestros_horarios[maestro.nombre][dia2][index+1]=="":
                                if index+1 in maestro.horarios[dia_to_num(dia2)] and  index+2 in maestro.horarios[dia_to_num(dia2)]:
                                    maestros_horarios[maestro.nombre][dia2][index+1]+=g
                                    maestros_horarios[maestro.nombre][dia2][index]+=g
                                    grupos_horarios[g][dia2][index]+=maestro.materia
                                    grupos_horarios[g][dia2][index+1]+=maestro.materia
                                    assig=True
                                    break
                    except:pass
            for i in range(horas[maestro.materia]-2):
                assig2=False
                dia_ind=0
                for dia in maestro.horarios:
                    if assig2:break
                    for clase in dia:
                        if dia_ind==5:dia_ind=0
                        if maestro.materia in grupos_horarios[g][num_to_dia(dia_ind)]: dia_ind+=1; continue
                        if grupos_horarios[g][num_to_dia(dia_ind)][clase-1]==""==maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][clase-1]:
                            grupos_horarios[g][num_to_dia(dia_ind)][clase-1]+=maestro.materia
                            maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][clase-1]+=g
                            dia_ind+=1
                            assig2=True
                            break
        else:
            for i in range(horas[maestro.materia]):
                assig=False
                dia_ind=0
                for dia in maestro.horarios:
                    if assig:break
                    for clase in dia:
                        if dia_ind==5:dia_ind=0
                        if maestro.materia in grupos_horarios[g][num_to_dia(dia_ind)]: dia_ind+=1; continue
                        if grupos_horarios[g][num_to_dia(dia_ind)][clase-1]==""==maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][clase-1]:
                            grupos_horarios[g][num_to_dia(dia_ind)][clase-1]+=maestro.materia
                            maestros_horarios[maestro.nombre][num_to_dia(dia_ind)][clase-1]+=g
                            dia_ind+=1
                            assig=True
                            break


## Acomodar las tutorias con preferencia
for maestro in Profs:
    if maestro.p:
        if maestro.tutoria!=None:
            assig = False
            for dia in grupos_horarios[maestro.tutoria]:
                if assig: break
                clase_ind=0
                for clase in grupos_horarios[maestro.tutoria][dia]:
                    if clase =="" and maestros_horarios[maestro.nombre][dia][clase_ind]=="" and clase_ind+1 in maestro.horarios[dia_to_num(dia)]:
                        print("AAA")
                        maestros_horarios[maestro.nombre][dia][clase_ind]+=maestro.tutoria+"(tutoria)"
                        grupos_horarios[maestro.tutoria][dia][clase_ind]+="tutoria"
                        assig=True
                        break
                    clase_ind+=1



# Agregamos al resto de los maestros
horas_de_materia_grupo()
for g in horas_grupos:
    for materia in horas_grupos[g]:
        for i in range(horas_grupos[g][materia]):
                mae = list(filter(lambda p: p.materia==materia and g in p.grupos, Profs))[0]
                print(mae)
#for g in grupos_maestro:
#    maestros_grupo_actual=[]
#    horas = horas_grupos[g]
#
#    for prof in Profs: # Encontramos los maestros de este grupo
#        if prof.nombre in grupos_maestro[g].values():
#            maestros_grupo_actual.append(prof)
#
#    for materia in horas:
#        m = 0
#        br = True
#        for ma in maestros_grupo_actual:
#            if ma.materia == materia:
#                m = ma
#                br = False
#        if br:break
#        for j in range(horas[materia]):
#            agg = False
#            n = 0
#            #print(horas[materia], materia, "AAAA", g )
#            for dia in m.horarios:
#                for clase in dia:
#                    clase = clase -1
#                    if agg: break
#                    if  maestros_horarios[m.nombre][num_to_dia(n)][clase]=="" and grupos_horarios[g][num_to_dia(n)][clase]=="":
#                        maestros_horarios[m.nombre][num_to_dia(n)][clase]+=g
#                        grupos_horarios[g][num_to_dia(n)][clase]+=m.materia
#                        agg=True
#
#                    print(m.nombre, m.materia, dia, num_to_dia(n))
#                    pass
#                if agg:
#                    break
#                n +=1

horas_de_materia_grupo()
for g in grupos_horarios:
    print(g)
    print_horario(grupos_horarios[g])
    print(horas_grupos[g])
#
#for g in grupos_horarios:
#    maestros_grupo_actual=[]
#    horas = {}
#    match g[0]:
#        case '1':
#            horas=horas_1ero.copy()
#        case "2":
#            horas=horas_2do.copy()
#        case "3":
#            horas=horas_3ero.copy()
#    for dia in grupos_horarios[g]:
#        for clase in grupos_horarios[g][dia]:
#            if clase == "tecnologia":continue
#            if clase != "":
#                horas[clase]-=1
#
#    horas_grupos[g]=horas
#        #print(m)
#
## Agregamos los que no se pudieron agregar
#for g in grupos_maestro:
#    maestros_grupo_actual=[]
#    horas = horas_grupos[g]
#
#    for prof in Profs: # Encontramos los maestros de este grupo
#        if prof.nombre in grupos_maestro[g].values():
#            maestros_grupo_actual.append(prof)
#    for materia in horas_grupos[g]:
#        if horas_grupos[g][materia]==0:
#            continue
#        if materia== "tutoria": continue
#        mae = list(filter(lambda p: p.materia==materia and g in p.grupos, Profs))[0]
#        for i in range(horas_grupos[g][materia]):
#            br = False
#            for dia in grupos_horarios[g]:
#                if br: break
#                clase_ind = 0
#                for clase in grupos_horarios[g][dia]:
#                    if br:break
#                    if  grupos_horarios[g][dia][clase_ind]=="":
#                        try: 
#                            prev = grupos_horarios[g][dia][clase_ind-1]
#                            if clase_ind==0:prev=None
#                        except: prev = None
#
#                        try: 
#                            next = grupos_horarios[g][dia][clase_ind+1]
#                        except: next = None
#                        if prev == materia == next: break
#                        if prev == materia:
#                            try:
#                                if grupos_horarios[g][dia][clase_ind-2]==materia:
#                                    break
#                            except: pass
#                            if maestros_horarios[mae.nombre][dia][clase_ind]!="":break
#                            grupos_horarios[g][dia][clase_ind]+=materia
#                            br = True
#                        elif next==materia:
#                            try:
#                                if grupos_horarios[g][dia][clase_ind+2]==materia:
#                                    break
#                            except: pass
#                            if maestros_horarios[mae.nombre][dia][clase_ind]!="":break
#                            grupos_horarios[g][dia][clase_ind]+=materia
#                            br = True
#                    clase_ind+=1
#            pass
#        _=0
#        pass
#
#for g in grupos_horarios:
#    maestros_grupo_actual=[]
#    horas = {}
#    match g[0]:
#        case '1':
#            horas=horas_1ero.copy()
#        case "2":
#            horas=horas_2do.copy()
#        case "3":
#            horas=horas_3ero.copy()
#    for dia in grupos_horarios[g]:
#        for clase in grupos_horarios[g][dia]:
#            if clase == "tecnologia":continue
#            if clase != "":
#                horas[clase]-=1
#
#    horas_grupos[g]=horas
#
## Agregar como sea
#
#for g in grupos_maestro:#
#    maestros_grupo_actua#l=[]
#    horas = horas_grupos#[g]
#                        #
#    for prof in Profs: ## Encontramos los maestros de este grupo
#        if prof.nombre in grupos_maestro[g].values():
#            maestros_grupo_actual.append(prof)
#    for materia in horas_grupos[g]:
#        if horas_grupos[g][materia]==0:
#            continue
#        print(materia, g)
#        if materia== "tutoria": continue
#    for clase in horas_grupos[g]:
#        if clase == "tutoria":continue
#        mae = list(filter(lambda p: p.materia==clase and g in p.grupos, Profs))[0]
#        if horas_grupos[g][clase]==0:continue
#        for i in range(horas_grupos[g][clase]):
#            dia_ind=0
#            #for clase in maestros_horarios[mae.nombre][num_to_dia(dia_ind)]
#            enc = False
#            clase_ind = 0
#            while True:
#                if clase not in grupos_horarios[g][num_to_dia(dia_ind)] and ""==grupos_horarios[g][num_to_dia(dia_ind)][clase_ind-1]==maestros_horarios[mae.nombre][num_to_dia(dia_ind)][clase_ind-1]: enc=True; break
#                if clase_ind==7:clase_ind=0; dia_ind+=1
#                clase_ind+=1
#                if dia_ind==4:
#                    break
#            if enc:
#                grupos_horarios[g][num_to_dia(dia_ind)][clase_ind-1]+=mae.materia
#                maestros_horarios[mae.nombre][num_to_dia(dia_ind)][clase_ind-1]+=g
#
#
##for j in horas_grupos:
##    print(j)
##    print_horario(grupos_horarios[j])
##    print(horas_grupos[j])
#for m in maestros_horarios:
#    mae = list(filter(lambda p: p.nombre==m , Profs))[0]
#    print(m,mae.materia)
#    print_horario(maestros_horarios[m])
#
## Imprimir grupos
