import json
while True:
    x={
        "nombre":input("nombre: "),
        "materia":input("materia: "),
        "horas_grupo":int(input("horas_grupo: ")),
        "horas_servicio":int(input("horas_servicio: ")),
        "p":(True if len(input("p: "))!=0 else False),
        "horarios":{}
        }
    for i in ['Lunes','Martes','Miercoles','Jueves','viernes']:
        print(f"Horas {i}")
        y=input("Leer: ")
        if len(y)==0:
            x["horarios"][i]=None
        else:
            l = []
            for j in y.split(','):
                if len(j)==0:pass
                try:
                    l.append(int(j))
                except:
                    l.append(j)
            x["horarios"][i]=l
    w = input("Grupos: ")
    p = []
    for j in w.split(','):
        p.append(j)
        x["grupos"]=p
    print(x)
    print(json.dumps(x))
    with open('maestros.json', 'a') as f:
        print(f'{json.dumps(x)},',file=f)
