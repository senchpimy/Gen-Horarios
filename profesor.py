from collections import namedtuple
from json import JSONEncoder
import json
from os import confstr
import pprint

def prefesor(Dict):
    return namedtuple('Profesor', Dict.keys())(*Dict.values())

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
#class Profesor:
#    def __init__(self,nombre:str,hg:int,hs:int,p:bool,horarios:dict,grupos:list) -> None:
#        self.nombre=nombre
#        self.horas_grupo=hg
#        self.horas_servicio=hs
#        self.p=p
#        self.horarios=horarios
#        self.grupos=grupos

file = open('maestros_final.json','r')
obj = json.load(file)
file.close()
profesores=[]

#for i in obj["maestros"]:
#    total = i["horas_grupo"] +i["horas_servicio"]
#    print(f"El Total de horas para el profesor {i['nombre']}  que da {i['materia']} es de {total}")
#    y = input("es esto correcto?: ")
#    if len(y)==0:
#        i["tutoria"]=None
#        i["total"]=total
#    else:
#        i["total"]=input("Ingrese nuevo total")
#        i["tutoria"]=y
#with open("maestros_final.json", "w") as f:
#    print(json.dumps(obj),file=f)
#

grupos = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "2A", "2B", "2C", "2D", "2E", "2F", "3A", "3B", "3C", "3D", "3E", "3F"]

for i in obj["maestros"]:
    p = json.dumps(i)
    pp = json.loads(p,object_hook=prefesor)
    profesores.append(pp)

maestros = []
materias = {}
for i in profesores:
    if i.materia==None:
        continue
    if i.nombre not in maestros:
        maestros.append(i.nombre)
    else:
        print(f"Maestro Repetido {i.nombre}")
    if i.horas_grupo<=0: print(f"Profesor {i.nombre} tiene horas de grupo invalidas")
    if i.materia not in materias:
        materias[i.materia]=1
    else:
        materias[i.materia]+=1
    if i.total-(i.horas_grupo+i.horas_servicio+(1 if i.tutoria!=None else 0))!=0:
        print(f'EL profesor {i.nombre} tiene errores en las horas')
print(materias)
print()


grupos_maestro:dict={}
for i in grupos:
    grupos_maestro[i]={}
    for j in profesores:
        if i in j.grupos:
            grupos_maestro[i][j.materia]=j.nombre

pprint.pprint(grupos_maestro)

for i in profesores:
    _=1
    if len(i.grupos)==1:continue
    #if i.horas_grupo%len(i.grupos)>0: print(i)
    #print(i.horas_grupo/len(i.grupos))
    #print(f'El grupo {i} tiene {len(grupos_maestro[i])} materias : ',end="")
    #print(*grupos_maestro[i].keys())

#for i in profesores:
 #   if i.tutoria != None: print(i.nombre,i.tutoria)

#pprint.pprint(grupos_maestro["1A"])

# Verificamos que todos los maestros tengan las horas necesarias para cubrir sus grupos
for grupo in grupos:
    horas_requeridas={}
    match grupo[0]:
        case "1":
            horas_requeridas=horas_1ero
        case "2":
            horas_requeridas=horas_2do
        case "3":
            horas_requeridas=horas_3ero
    for prof in profesores:
        if  grupo in prof.grupos:
            if horas_requeridas[prof.materia] > prof.horas_grupo/len(prof.grupos):
                print(f"El maestro {prof.nombre} no puede cumplir sus horas requeridas con el total de sus grupos, pues la matera {prof.materia} para el grupo {grupo} requiere de {horas_requeridas[prof.materia]} horas y con {len(prof.grupos)} grupos y con {prof.horas_grupo} de horas de grupo serian un total de {prof.horas_grupo/len(prof.grupos)} horas por grupo")
