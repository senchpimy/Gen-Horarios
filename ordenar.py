from profesor import profesores as Profs
from tabulate import tabulate
import termcolor

print()
print()

def dia_to_num(dia):
    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miercoles": 2,
        "Jueves": 3,
        "Viernes": 4,
    }
    
    return dias.get(dia.capitalize(), None)

def print_horario_1(d):
    v = ("{:<15} {:<15} {:<15} {:<15} {:<15}".format(*d.keys()))
    val = termcolor.colored(v,"white",attrs=["reverse"])
    print(val)
    for j in range(7):
        try:
            ju = d["Jueves"][j]
        except:
            ju = "000"
        try:
            vi = d["Viernes"][j]
        except:
            vi = "0000"
        v = ("{:<15} {:<15} {:<15} {:<15} {:<15}".format(d["Lunes"][j], d["Martes"][j], d["Miercoles"][j],ju ,vi ))
        print(v)
    print()


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

maestros1A = []
materias = []

# Escojemos los maestros de 1A
for i in Profs:
    if "1B" in i.grupos:
        maestros1A.append(i)
# Calculamos cuantas horas son por semana
horas_materia = {}
for i in maestros1A:
    horas_materia[i.materia]=int(i.horas_grupo/len(i.grupos))

# Hacemos el primer acomodo
horario_posible={}
for i in ["Lunes","Martes","Miercoles","Jueves","Viernes"]:
    dia = []
    for materia in horas_materia:
        if horas_materia[materia]>0:
            dia.append(materia)
            horas_materia[materia]-=1
    horario_posible[i]=dia

print_horario(horario_posible)

# Mapeamos las materias con los maestros
horario_posible_maestros = {}
for i in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]:

    horario_posible_maestros[i] = []
    
    for j in horario_posible[i]:
        for maestro in maestros1A:
            if maestro.materia == j:
                horario_posible_maestros[i].append(maestro.nombre)
                break
        else:
            horario_posible_maestros[i].append(j)
print_horario(horario_posible_maestros)

# Acomodamos a los que tienen preferencia
for maestro in maestros1A:
    for dia in horario_posible_maestros:
        if maestro.nombre in horario_posible_maestros[dia] and maestro.p:
            hora = horario_posible_maestros[dia].index(maestro.nombre) + 1 # hora en la que esta elmaestro
            if hora not in maestro.horarios[dia_to_num(dia)]:
                seleccion = 0
                while True: # Emepzamos un loop para buscar al maestro con el cual cambiar, este no debe tener preferencia
                    nuevo_indice = maestro.horarios[dia_to_num(dia)][seleccion]-1 # Seleccionamos una hora de los que el maestro prefiere
                    maestro_int = horario_posible_maestros[dia][nuevo_indice] # El maestro por el cual va a cambiar lugar
                    result = list(filter(lambda person: person.nombre == maestro_int, maestros1A))
                    if not result[0].p: #Si no tiene preferencia lo encontramos y terminamos el loop
                        break
                    seleccion+=1

                horario_posible_maestros[dia][nuevo_indice],horario_posible_maestros[dia][hora-1] = maestro.nombre ,maestro_int # Se hace el intercambio con el profresor
                print(hora-1,nuevo_indice)

            print(maestro.nombre,dia,hora)
print_horario(horario_posible_maestros)
