from collections import namedtuple
from json import JSONEncoder
import json
import pprint

def prefesor(Dict):
    return namedtuple('Profesor', Dict.keys())(*Dict.values())

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
    if i.nombre not in maestros:
        maestros.append(i.nombre)
    else:
        print(f"Maestro Repetido {i.nombre}")
    if i.horas_grupo<=0: print(f"Profesor {i.nombre} tiene horas de grupo invalidas")
    if i.materia not in materias:
        materias[i.materia]=1
    else:
        materias[i.materia]+=1
    if i.total-(i.horas_grupo+i.horas_servicio)>2:
        print(f'EL profesor {i.nombre} tiene errores en las horas')
print(materias)
print()


grupos_maestro:dict={}
for i in grupos:
    grupos_maestro[i]={}
    for j in profesores:
        if i in j.grupos:
            grupos_maestro[i][j.materia]=j.nombre

#pprint.pprint(grupos_maestro)
for i in grupos_maestro:
    print(f'El grupo {i} tiene {len(grupos_maestro[i])} materias : ',end="")
    print(*grupos_maestro[i].keys())

