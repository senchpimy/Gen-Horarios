# Generador y Editor de Horarios Escolares

Este proyecto consiste en un conjunto de herramientas de Python diseñadas para automatizar y facilitar la creación y gestión de horarios escolares. A partir de un archivo de datos (`.json`), el sistema puede generar un horario completo, analizarlo en busca de conflictos y permitir su edición manual a través de una interfaz de consola interactiva.

## Características Principales

### 1. Análisis de Datos (`analizar_maestros.py`)
- **Lista de Maestros Únicos:** Genera una lista de todos los maestros en el sistema.
- **Detección de Tutorías Inconsistentes:** Identifica a los maestros que tienen horas de tutoría asignadas pero no un grupo específico de tutoría.
- **Detección de Empalmes:** Advierte si dos maestros están asignados a la misma materia y grupo.
- **Verificación de Grupos sin Tutor:** Muestra una lista de todos los grupos que no tienen un tutor asignado.

### 2. Generación Automática de Horarios (`generador_horarios.py`)
- **Generación Basada en Reglas:** Crea horarios completos que respetan las horas semanales requeridas para cada materia por año escolar.
- **Manejo de Casos Complejos:** Distribuye correctamente las horas de materias como "Tecnología", donde varios maestros imparten clases al mismo grupo.
- **Optimización Básica:** Intenta crear horarios compactos para los maestros, minimizando las horas libres entre clases.
- **Exportación a Excel:** Guarda el horario generado en un archivo `.xlsx` con una pestaña para cada grupo, una para cada maestro y una para el análisis de horas.

### 3. Edición Manual Interactiva (`editor_horarios.py`)
- **Interfaz de Consola (TUI):** Ofrece un menú interactivo fácil de usar para modificar los horarios.
- **Carga Robusta:** Lee el archivo `.xlsx` generado, leyendo los datos celda por celda para evitar errores de formato.
- **Movimiento de Clases Inteligente:** Permite seleccionar una clase y moverla a otro slot.
- **Resolución de Conflictos "en Cascada":** Si el slot de destino está ocupado, intercambia automáticamente las clases, moviendo la clase desplazada al slot de origen.
- **Verificación de Selección:** Antes de pedir el destino, confirma la clase que el usuario ha seleccionado para mover, evitando errores.
- **Guardado Seguro:** Guarda los cambios en un nuevo archivo para no sobrescribir el original.

## Estructura del Proyecto
```
/
|-- 1.json                  # Datos de entrada de maestros y materias
|-- analizar_maestros.py    # Script para análisis inicial de los datos
|-- generador_horarios.py   # Script para la generación automática de horarios
|-- editor_horarios.py      # Script para la edición manual de horarios generados
|-- horarios.xlsx           # Archivo de salida del generador (ejemplo)
|-- horarios_modificados.xlsx # Archivo de salida del editor (ejemplo)
`-- README.md               # Este archivo
```

## Requisitos
- Python 3.x
- Librerías de Python: `pandas`, `openpyxl`

## Instalación
1.  Asegúrate de tener Python 3 instalado en tu sistema.
2.  Clona este repositorio o descarga los archivos en una carpeta.
3.  Abre una terminal o línea de comandos en esa carpeta e instala las dependencias necesarias:
    ```bash
    pip install pandas openpyxl
    ```

## Flujo de Trabajo y Uso

El uso del proyecto está pensado para seguir un flujo lógico de 3 o 4 pasos.

### Paso 1: Preparar los Datos
Asegúrate de que el archivo `1.json` contiene toda la información correcta de los maestros, sus materias, grupos asignados y horas. Este archivo es la única fuente de verdad para la generación de horarios.

### Paso 2: Analizar los Datos (Opcional pero recomendado)
Antes de generar el horario, es una buena práctica analizar los datos de entrada para encontrar posibles problemas.
```bash
python analizar_maestros.py
```
Este script imprimirá en la consola los conflictos, inconsistencias y listas de maestros y grupos, permitiéndote corregir el archivo `1.json` antes de continuar.

### Paso 3: Generar el Horario Automático
Este es el paso principal. El script leerá el archivo `1.json` y creará una primera versión del horario.
```bash
python generador_horarios.py
```
Al finalizar, se creará un archivo llamado `horarios.xlsx` en la misma carpeta. Este archivo contendrá el horario completo.

### Paso 4: Editar y Ajustar el Horario Manualmente
Una vez que tengas el archivo `horarios.xlsx`, puedes usar el editor interactivo para hacer ajustes finos.
```bash
python editor_horarios.py
```
Sigue los pasos en el menú de la consola:
1.  **Selecciona la opción [1]** para mover una clase.
2.  **Elige un maestro** de la lista numerada.
3.  **Selecciona la clase de ORIGEN** indicando el día y el período.
4.  El programa te mostrará una **pantalla de verificación** para confirmar que has seleccionado la clase correcta.
5.  **Selecciona el slot de DESTINO**. El programa intercambiará las clases y te mostrará el horario actualizado del maestro.
6.  Cuando estés satisfecho con los cambios, **selecciona la opción [2]** para guardar tu trabajo. Se te pedirá un nuevo nombre de archivo (ej. `horarios_final.xlsx`). El programa te indicará la ruta completa donde se guardó el archivo.

---
*Este proyecto fue desarrollado como una herramienta práctica para la gestión de recursos académicos, combinando la automatización con la flexibilidad de la edición manual.*
