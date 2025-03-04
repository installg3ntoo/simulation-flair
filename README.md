# Simulación Flair

## Instalación y ejecución

Esta aplicación se probó en **Python 3.12.2**, por lo que es la versión recomendable 
para ejecutar el proyecto.

Para la instalación sólo es necesario descargar el repositorio:
```bash
git clone https://github.com/installg3ntoo/simulation-flair.git
```

Para ejecutar la aplicación, usar el siguiente comando (dentro de la carpeta del proyecto):
```bash
python main.py
```

## Arquitectura y Lógica

La aplicación está estructurada de la siguiente manera:

- **main.py**: El punto de entrada de la aplicación.
- **clases.py**: Contiene las clases principales utilizadas en la simulación.
  - **Simulacion**: Clase principal que maneja la lógica de la simulación.
    - **Building**: Clase que contiene una lista de los pisos del edificio.
        - **Floor**: Clase que contiene una lista de las habitaciones de un piso del edificio.
        - **Room**: Clase que representa una habitación, cada una tiene un sensor.
        - **Sensor**: Clase que representa un Sensor, tiene un estado ON o Alert.


La lógica de la aplicación funciona en que en cada _update_ de la simulación, los zombies se
moverán a las habitaciones de los lados, arriba y abajo de la habitación que estaban actualmente,
y tienen una probabilidad de 50% de dejar la habitación dónde estaban o seguir en la misma
habitación (multiplicándose). 

También cuando se resetee un sensor su estado pasará a ON independiente si hay zombies en la sala
o no, y este se actualizará cuando se actualize la simulación (o se actualizen todos los sensores
simplemente).


## Comandos

La aplicación se maneja a través de un menú de opciones en la línea de comandos. Los comandos disponibles son:

1. **Añadir zombies**: Genera zombies en una habitación seleccionada, hay que colocar el número de piso y habitación.
2. **Bloquear habitación**: Bloquea una habitación lo que impide que zombies entren o salgan de esa habitación (tienen 50% de probabilidad de "morir" en la habitación cuando se pase un turno).
3. **Mostrar estado**: Muestra el estado del edificio en base a los sensores de cada habitación (pueden no estar correctos si se resetearon).
4. **Actualizar sensores**: Actualiza todos los sensores a su estado actual, basado en la presencia de zombies en las habitaciones.
5. **Resetear sensor**: Resetea un sensor, pasándolo al estado ON.
6. **Actualizar simulación**: Actualiza la simulación avanzando un turno, moviendo los zombies y actualizando los sensores.
7. **Guardar**: Guarda el estado actual.
8. **Salir**: Salir sin guardar.

Para seleccionar una opción, simplemente ingresa el número correspondiente y presiona Enter.

Al comienzo del programa se preguntará si se quiere cargar una simulación anterior o no, las 
simulaciones se cargan y guardan en un archivo JSON `simulation.json`. Si no se carga ningún
archivo se pedirá ingresar el número de pisos y de habitaciones por piso, lo que creará un
edificio vacío (sin zombies) para empezar una simulación.