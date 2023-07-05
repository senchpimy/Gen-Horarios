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
    p = json.dumps(i)
    pp = json.loads(p,object_hook=prefesor)
    profesores.append(pp)
