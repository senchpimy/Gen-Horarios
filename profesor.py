from collections import namedtuple
from json import JSONEncoder
import json

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

file = open('maestros.json','r')
obj = json.load(file)
file.close()
profesores=[]

for i in obj["maestros"]:
    total = i["horas_grupo"] +i["horas_servicio"]
    print(f"El Total de horas para el profesor {i['nombre']} es de {total}")
    y = input("es esto correcto?: ")
    if len(y)==0:
        i["tutoria"]=None
        i["total"]=total
    else:
        i["total"]=input("Ingrese nuevo total")
        i["tutoria"]=y
    #p = json.dumps(i)
    #pp = json.loads(p,object_hook=prefesor)
    #profesores.append(pp)
with open("maestros_final.json", "w") as f:
    print(json.dumps(obj),file=f)


maestros = []
materias = []
for i in profesores:
    if i.nombre not in maestros:
        maestros.append(i.nombre)
    else:
        print(f"Maestro Repetido {i.nombre}")
    if i.horas_grupo<=0: print(f"Profesor {i.nombre} tiene horas de grupo invalidas")
    if i.materia not in materias:
        materias.append(i.materia)
print(materias)
