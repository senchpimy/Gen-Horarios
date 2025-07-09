from profesor import profesores as Profs
#from ordenar import horarios_maestros
#from ordenar import horarios_grupo
from ordenar2 import maestros_horarios as horarios_maestros,grupos_maestro, horas_grupos, num_to_dia
from ordenar2 import grupos_horarios as horarios_grupo
comienzo = """
\\documentclass{article}
\\usepackage{titlesec}
\\usepackage{titling}
\\usepackage{graphicx}
\\graphicspath{ {.} }
\\usepackage[a4paper, total={6in, 8in},margin=3em]{geometry}
\\usepackage{hyperref}


	\\titleformat{\\section}
	{\\huge\\bfseries}
	{}
	{0em}
	{}
\\title{Horarios}




\\begin{document}

"""
for grupo in horarios_grupo:
    for j in ["Lunes","Martes","Miercoles","Jueves","Viernes"]:
        for i in range(7):
            try:
                if horarios_grupo[grupo][j][i]=="":
                    horarios_grupo[grupo][j][i]="\\_"
            except:
                    horarios_grupo[grupo][j].append("\\_")

for grupo in horarios_grupo:
    grupo_str=f"""    
	{{\\huge \\textbf{{{grupo} }}}}
          \\begin{{center}}
        \\begin{{tabular}}{{||c c c c c c||}} 
         \\hline
          Horas & Lunes & Martes  & Miercoles & Jueves & Viernes\\\\
         \\hline\\hline
          7:30-8:20 &  {horarios_grupo[grupo]["Lunes"][0]}  & {horarios_grupo[grupo]["Martes"][0]} & {horarios_grupo[grupo]["Miercoles"][0]}  & {horarios_grupo[grupo]["Jueves"][0]} & {horarios_grupo[grupo]["Viernes"][0]} \\\\
         \\hline
           8:20-9:10 &  {horarios_grupo[grupo]["Lunes"][1]}  & {horarios_grupo[grupo]["Martes"][1]} & {horarios_grupo[grupo]["Miercoles"][1]}  & {horarios_grupo[grupo]["Jueves"][1]} & {horarios_grupo[grupo]["Viernes"][1]}  \\\\
         \\hline
           9:10-10:00 &  {horarios_grupo[grupo]["Lunes"][2]} & {horarios_grupo[grupo]["Martes"][2]} & {horarios_grupo[grupo]["Miercoles"][2]}  & {horarios_grupo[grupo]["Jueves"][2]} & {horarios_grupo[grupo]["Viernes"][2]}  \\\\
         \\hline
           10:00-10:50 &  {horarios_grupo[grupo]["Lunes"][3]} & {horarios_grupo[grupo]["Martes"][3]} & {horarios_grupo[grupo]["Miercoles"][3]}  & {horarios_grupo[grupo]["Jueves"][3]} & {horarios_grupo[grupo]["Viernes"][3]}  \\\\
         \\hline
           11:10-12:00 &  {horarios_grupo[grupo]["Lunes"][4]} & {horarios_grupo[grupo]["Martes"][4]} & {horarios_grupo[grupo]["Miercoles"][4]}  & {horarios_grupo[grupo]["Jueves"][4]} & {horarios_grupo[grupo]["Viernes"][4]}  \\\\
         \\hline
           12:00-12:50 &  {horarios_grupo[grupo]["Lunes"][5]} & {horarios_grupo[grupo]["Martes"][5]} & {horarios_grupo[grupo]["Miercoles"][5]}  & {horarios_grupo[grupo]["Jueves"][5]} & {horarios_grupo[grupo]["Viernes"][5]}  \\\\
         \\hline
           12:50-13:40 & {horarios_grupo[grupo]["Lunes"][6]} & {horarios_grupo[grupo]["Martes"][6]} & {horarios_grupo[grupo]["Miercoles"][6]}  & {horarios_grupo[grupo]["Jueves"][6]} & {horarios_grupo[grupo]["Viernes"][6]}  \\\\
         \\hline
        \\end{{tabular}}
        \\end{{center}}
        \\vspace{{2em}}
        \\textbf{{Horas que faltan por cubrir:}}

    """
    for materia in horas_grupos[grupo]:
        if materia == "tutoria":
            m = list(filter(lambda person: person.tutoria == grupo, Profs))[0]
            st= f"\\textbf{{{materia}::{m.nombre}:}}{horas_grupos[grupo][materia]}\n\n"
            grupo_str+=st
        else:
            m = list(filter(lambda person: person.materia == materia and grupo in person.grupos, Profs))[0]
            st= f"\\textbf{{{materia}::{m.nombre}:}}{horas_grupos[grupo][materia]}\n\n"
            grupo_str+=st
    l = """
	\\pagebreak

    """
    comienzo+=grupo_str+l

for maestro in horarios_maestros:
    m = list(filter(lambda person: person.nombre == maestro, Profs))[0]
    print(horarios_maestros[maestro])
    maestro_str=f"""    
	{{\\huge \\textbf{{{maestro} }}}}
	{{\\huge \\textbf{{{m.materia} }}}}
    \\begin{{center}}
    \\begin{{tabular}}{{||c c c c c c||}} 
     \\hline
      Horas & Lunes & Martes  & Miercoles & Jueves & Viernes\\\\ [1ex] 
     \\hline\\hline
      7:30-8:20 &  {horarios_maestros[maestro]["Lunes"][0]}  & {horarios_maestros[maestro]["Martes"][0]} & {horarios_maestros[maestro]["Miercoles"][0]}  & {horarios_maestros[maestro]["Jueves"][0]} & {horarios_maestros[maestro]["Viernes"][0]}  \\\\
     \\hline
       8:20-9:10 &  {horarios_maestros[maestro]["Lunes"][1]}  & {horarios_maestros[maestro]["Martes"][1]} & {horarios_maestros[maestro]["Miercoles"][1]}  & {horarios_maestros[maestro]["Jueves"][1]} & {horarios_maestros[maestro]["Viernes"][1]}  \\\\
     \\hline
       9:10-10:00 &  {horarios_maestros[maestro]["Lunes"][2]} & {horarios_maestros[maestro]["Martes"][2]} & {horarios_maestros[maestro]["Miercoles"][2]}  & {horarios_maestros[maestro]["Jueves"][2]} & {horarios_maestros[maestro]["Viernes"][2]}  \\\\
     \\hline
       10:00-10:50 &  {horarios_maestros[maestro]["Lunes"][3]} & {horarios_maestros[maestro]["Martes"][3]} & {horarios_maestros[maestro]["Miercoles"][3]}  & {horarios_maestros[maestro]["Jueves"][3]} & {horarios_maestros[maestro]["Viernes"][3]}  \\\\
     \\hline
       11:10-12:00 &  {horarios_maestros[maestro]["Lunes"][4]} & {horarios_maestros[maestro]["Martes"][4]} & {horarios_maestros[maestro]["Miercoles"][4]}  & {horarios_maestros[maestro]["Jueves"][4]} & {horarios_maestros[maestro]["Viernes"][4]}  \\\\
     \\hline
       12:00-12:50 &  {horarios_maestros[maestro]["Lunes"][5]} & {horarios_maestros[maestro]["Martes"][5]} & {horarios_maestros[maestro]["Miercoles"][5]}  & {horarios_maestros[maestro]["Jueves"][5]} & {horarios_maestros[maestro]["Viernes"][5]}  \\\\
     \\hline
       12:50-13:40 & {horarios_maestros[maestro]["Lunes"][6]} & {horarios_maestros[maestro]["Martes"][6]} & {horarios_maestros[maestro]["Miercoles"][6]}  & {horarios_maestros[maestro]["Jueves"][6]} & {horarios_maestros[maestro]["Viernes"][6]}  \\\\
     \\hline
    \\end{{tabular}}
    \\end{{center}}
    \\vspace{{2em}}
    """
    horas_totales=0
    for dia in horarios_maestros[maestro]:
            for clase in horarios_maestros[maestro][dia]:
                if len(clase)>0 and clase[0] in "123":horas_totales+=1
    fff = f"""
    \\textbf{{Horas de grupo:}}: {horas_totales}/{m.horas_grupo}


    \\textbf{{Horas de servicio:}}: {0}/{m.horas_servicio}
    """
    maestro_str+=fff
    semana = {
        "Lunes":["\\_" for _ in range(7)],
        "Martes":["\\_" for _ in range(7)],
        "Miercoles":["\\_" for _ in range(7)],
        "Jueves":["\\_" for _ in range(7)],
        "Viernes":["\\_" for _ in range(7)],
            }
    for dia,cont in enumerate(m.horarios):
        d = num_to_dia(dia)
        for clase in cont:
            semana[d][clase-1]="x"
            pass
    lel = """
        \\textbf{Horario preferido:}
    \\begin{center}
    \\begin{tabular}{||c c c c c c||}
     \\hline
      Horas & Lunes & Martes  & Miercoles & Jueves & Viernes\\\\ [1ex] 
     \\hline\\hline
    """
    for i in range(7):
        lel += f"""
            7:30-8:20 &  {semana["Lunes"][i]}  & {semana["Martes"][i]}  & {semana["Miercoles"][i]}  & {semana["Jueves"][i]}  & {semana["Viernes"][i]} \\\\
             \\hline
            """
    lel+=f"""
    \\end{{tabular}}
    \\end{{center}}

    \\textbf{{Tutoria:}}{m.tutoria}
    """
    maestro_str+=lel

    comienzo+=maestro_str+"""
	\\pagebreak
    """

final = """
\\end{document}
"""
comienzo+=final

with open("horarios.tex","w") as f:
    print(comienzo,file=f)

