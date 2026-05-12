# Importamos tkinter para crear la interfaz gráfica.
import tkinter as tk

# Importamos messagebox para mostrar ventanas de aviso o información.
from tkinter import messagebox

# Importamos todas las funciones y clases de Airport.py.
from Airport import *

# Importamos todas las funciones y clases de Aircraft.py.
from Aircraft import *

# Importamos todas las funciones y clases de LEBL.py.
from LEBL import *


# Creamos la ventana principal de la aplicación.
root = tk.Tk()

# Ponemos el título de la ventana principal.
root.title("Gestor de Aeropuertos - INFO1")

# Definimos el tamaño de la ventana principal.
root.geometry("430x760")

# Ponemos color de fondo a la ventana principal.
root.configure(bg="#f8f9fa")

# Lista donde guardaremos los aeropuertos cargados desde airports.txt.
lista_airports = []

# Lista donde guardaremos los vuelos cargados desde Arrivals.txt.
lista_vuelos = []

# Variable donde guardaremos la estructura de LEBL cuando se cargue.
bcn = ""


# Esta función cambia el texto de estado de la parte inferior de la ventana.
def cambiar_estado(texto):
    # Actualizamos el texto de la etiqueta de estado.
    etiqueta_estado.config(text=texto)


# Esta función carga aeropuertos y vuelos desde sus archivos .txt.
def accion_cargar():
    # Indicamos que vamos a modificar las listas globales.
    global lista_airports, lista_vuelos

    # Cargamos los aeropuertos desde airports.txt.
    lista_airports = LoadAirports("airports.txt")

    # Cargamos los vuelos desde Arrivals.txt.
    lista_vuelos = LoadArrivals("Arrivals.txt")

    # Empezamos a recorrer la lista de aeropuertos.
    i = 0

    # Recorremos todos los aeropuertos cargados.
    while i < len(lista_airports):
        # Calculamos si el aeropuerto actual es Schengen.
        SetSchengen(lista_airports[i])

        # Pasamos al siguiente aeropuerto.
        i = i + 1

    # Cambiamos el mensaje de estado.
    cambiar_estado("Datos cargados correctamente.")

    # Mostramos un mensaje informativo al usuario.
    messagebox.showinfo("INFO", "Datos cargados correctamente.")


# Esta función carga la estructura de terminales, áreas y puertas de LEBL.
def accion_cargar_lebl():
    # Indicamos que vamos a modificar la variable global bcn.
    global bcn

    # Cargamos la estructura del aeropuerto desde LEBL.txt.
    bcn = LoadAirportStructure("LEBL.txt")

    # Si devuelve -1 significa que ha habido un error.
    if bcn == -1:
        # Mostramos un aviso de error al usuario.
        messagebox.showwarning("Error", "No se ha podido cargar LEBL.txt.")

        # Actualizamos el estado de la aplicación.
        cambiar_estado("Error al cargar estructura LEBL.")

    # Si no devuelve -1, la estructura se ha cargado bien.
    else:
        # Actualizamos el estado de la aplicación.
        cambiar_estado("Estructura LEBL cargada correctamente.")

        # Mostramos un mensaje informativo al usuario.
        messagebox.showinfo("INFO", "Estructura de LEBL cargada correctamente.")


# Esta función asigna puertas a todos los vuelos cargados.
def accion_asignar_puertas():
    # Indicamos que vamos a usar la variable global bcn.
    global bcn

    # Si bcn está vacío o tiene error, todavía no se ha cargado LEBL.
    if bcn == "" or bcn == -1:
        # Avisamos al usuario de que primero debe cargar LEBL.
        messagebox.showwarning("Error", "Primero debes cargar la estructura de LEBL.")

    # Si no hay vuelos cargados, no se pueden asignar puertas.
    elif len(lista_vuelos) == 0:
        # Avisamos al usuario de que debe cargar vuelos.
        messagebox.showwarning("Error", "Primero debes cargar los vuelos.")

    # Si hay estructura y vuelos, podemos asignar puertas.
    else:
        # Contador de vuelos que sí reciben puerta.
        asignados = 0

        # Contador de vuelos que no reciben puerta.
        no_asignados = 0

        # Empezamos a recorrer la lista de vuelos.
        i = 0

        # Recorremos todos los vuelos.
        while i < len(lista_vuelos):
            # Intentamos asignar puerta al vuelo actual.
            resultado = AssignGate(bcn, lista_vuelos[i])

            # Si resultado es 0, se ha asignado una puerta.
            if resultado == 0:
                # Sumamos uno al contador de asignados.
                asignados = asignados + 1

            # Si resultado no es 0, no se ha podido asignar puerta.
            else:
                # Sumamos uno al contador de no asignados.
                no_asignados = no_asignados + 1

            # Pasamos al siguiente vuelo.
            i = i + 1

        # Actualizamos el estado con el resultado.
        cambiar_estado("Puertas asignadas: " + str(asignados) + " | No asignados: " + str(no_asignados))

        # Mostramos el resultado en una ventana informativa.
        messagebox.showinfo("INFO", "Puertas asignadas: " + str(asignados) + "\nNo asignados: " + str(no_asignados))


# Esta función muestra una ventana con la ocupación de todas las puertas.
def accion_mostrar_ocupacion():
    # Si bcn está vacío o tiene error, todavía no se ha cargado LEBL.
    if bcn == "" or bcn == -1:
        # Avisamos al usuario de que debe cargar LEBL.
        messagebox.showwarning("Error", "Primero debes cargar la estructura de LEBL.")

    # Si LEBL está cargado, podemos mostrar la ocupación.
    else:
        # Obtenemos la lista de ocupación de puertas.
        ocupacion = GateOccupancy(bcn)

        # Creamos una ventana secundaria.
        pantalla = tk.Toplevel(root)

        # Ponemos título a la ventana secundaria.
        pantalla.title("Ocupación de Puertas")

        # Definimos el tamaño de la ventana secundaria.
        pantalla.geometry("600x500")

        # Ponemos color de fondo a la ventana secundaria.
        pantalla.configure(bg="#f8f9fa")

        # Creamos el título de la ventana de ocupación.
        tk.Label(
            # Indicamos que el Label pertenece a la ventana secundaria.
            pantalla,
            # Texto que verá el usuario.
            text="OCUPACIÓN DE PUERTAS",
            # Fuente del texto.
            font=("Arial", 13, "bold"),
            # Color de fondo del texto.
            bg="#f8f9fa"
        # Colocamos el Label en pantalla.
        ).pack(pady=10)

        # Creamos una caja de texto donde se escribirá la ocupación.
        caja = tk.Text(pantalla, width=75, height=25)

        # Colocamos la caja de texto en pantalla.
        caja.pack(pady=10)

        # Empezamos a recorrer la lista de ocupación.
        i = 0

        # Recorremos todos los elementos de ocupación.
        while i < len(ocupacion):
            # Guardamos el nombre de la terminal.
            terminal = ocupacion[i][0]

            # Guardamos el nombre del área.
            area = ocupacion[i][1]

            # Guardamos el nombre de la puerta.
            gate = ocupacion[i][2]

            # Guardamos si la puerta está ocupada.
            ocupado = ocupacion[i][3]

            # Guardamos el avión que ocupa la puerta.
            avion = ocupacion[i][4]

            # Si la puerta está ocupada, el estado será OCUPADA.
            if ocupado == True:
                # Texto para puertas ocupadas.
                estado = "OCUPADA"

            # Si no está ocupada, el estado será LIBRE.
            else:
                # Texto para puertas libres.
                estado = "LIBRE"

            # Creamos una línea de texto con toda la información de la puerta.
            linea = terminal + " | " + area + " | " + gate + " | " + estado + " | " + avion + "\n"

            # Insertamos la línea en la caja de texto.
            caja.insert(tk.END, linea)

            # Pasamos a la siguiente puerta.
            i = i + 1

        # Creamos un botón para cerrar la ventana secundaria.
        tk.Button(
            # El botón pertenece a la ventana secundaria.
            pantalla,
            # Texto del botón.
            text="Cerrar",
            # Al pulsarlo se destruye la ventana secundaria.
            command=pantalla.destroy,
            # Color del texto del botón.
            fg="red",
            # Ancho del botón.
            width=25
        # Colocamos el botón en pantalla.
        ).pack(pady=10)


# Esta función muestra la gráfica de aeropuertos Schengen y no Schengen.
def accion_grafica_airports():
    # Comprobamos que haya aeropuertos cargados.
    if len(lista_airports) > 0:
        # Llamamos a la función que dibuja la gráfica.
        PlotAirports(lista_airports)

        # Actualizamos el estado.
        cambiar_estado("Gráfica Schengen de aeropuertos mostrada.")

    # Si no hay aeropuertos cargados, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Primero debes cargar los aeropuertos.")


# Esta función genera el mapa KML de aeropuertos.
def accion_mapa_airports():
    # Comprobamos que haya aeropuertos cargados.
    if len(lista_airports) > 0:
        # Llamamos a la función que genera el KML de aeropuertos.
        MapAirports(lista_airports)

        # Actualizamos el estado.
        cambiar_estado("Mapa de aeropuertos generado.")

    # Si no hay aeropuertos cargados, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Primero debes cargar los aeropuertos.")


# Esta función muestra la gráfica de llegadas por hora.
def accion_grafica_llegadas():
    # Comprobamos que haya vuelos cargados.
    if len(lista_vuelos) > 0:
        # Llamamos a la función que dibuja las llegadas por hora.
        PlotArrivals(lista_vuelos)

        # Actualizamos el estado.
        cambiar_estado("Gráfica de llegadas por hora mostrada.")

    # Si no hay vuelos cargados, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Primero debes cargar los vuelos.")


# Esta función muestra la gráfica de vuelos por compañía.
def accion_grafica_airlines():
    # Comprobamos que haya vuelos cargados.
    if len(lista_vuelos) > 0:
        # Llamamos a la función que dibuja vuelos por compañía.
        PlotAirlines(lista_vuelos)

        # Actualizamos el estado.
        cambiar_estado("Gráfica de vuelos por compañía mostrada.")

    # Si no hay vuelos cargados, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Primero debes cargar los vuelos.")


# Esta función muestra la gráfica de vuelos Schengen y no Schengen.
def accion_grafica_tipo_vuelos():
    # Comprobamos que haya vuelos y aeropuertos cargados.
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        # Llamamos a la función que dibuja la gráfica por tipo de vuelo.
        PlotFlightsType(lista_vuelos, lista_airports)

        # Actualizamos el estado.
        cambiar_estado("Gráfica Schengen / No Schengen de vuelos mostrada.")

    # Si falta algún dato, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos y vuelos.")


# Esta función genera el mapa KML de vuelos.
def accion_mapa_vuelos():
    # Comprobamos que haya vuelos y aeropuertos cargados.
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        # Llamamos a la función que genera el KML de vuelos.
        MapFlights(lista_vuelos, lista_airports)

        # Actualizamos el estado.
        cambiar_estado("Mapa de vuelos generado.")

    # Si falta algún dato, mostramos aviso.
    else:
        # Avisamos al usuario.
        messagebox.showwarning("Error", "Faltan datos para abrir el mapa.")


# Esta función abre una ventana secundaria con los botones de gráficas.
def abrir_pantalla_graficas():
    # Creamos una ventana secundaria.
    pantalla = tk.Toplevel(root)

    # Ponemos título a la ventana secundaria.
    pantalla.title("Pantalla de Gráficas")

    # Definimos el tamaño de la ventana secundaria.
    pantalla.geometry("400x420")

    # Ponemos color de fondo a la ventana secundaria.
    pantalla.configure(bg="#f8f9fa")

    # Creamos el título de la pantalla de gráficas.
    tk.Label(
        # Indicamos que el Label pertenece a la pantalla secundaria.
        pantalla,
        # Texto que verá el usuario.
        text="PANTALLA DE GRÁFICAS",
        # Fuente del texto.
        font=("Arial", 14, "bold"),
        # Color de fondo.
        bg="#f8f9fa"
    # Colocamos el título.
    ).pack(pady=20)

    # Creamos botón para la gráfica de aeropuertos.
    tk.Button(
        # El botón pertenece a la pantalla secundaria.
        pantalla,
        # Texto del botón.
        text="Gráfica Aeropuertos Schengen",
        # Función que se ejecuta al pulsarlo.
        command=accion_grafica_airports,
        # Ancho del botón.
        width=30
    # Colocamos el botón.
    ).pack(pady=5)

    # Creamos botón para la gráfica de llegadas por hora.
    tk.Button(
        # El botón pertenece a la pantalla secundaria.
        pantalla,
        # Texto del botón.
        text="Gráfica Llegadas por Hora",
        # Función que se ejecuta al pulsarlo.
        command=accion_grafica_llegadas,
        # Ancho del botón.
        width=30
    # Colocamos el botón.
    ).pack(pady=5)

    # Creamos botón para la gráfica de vuelos por compañía.
    tk.Button(
        # El botón pertenece a la pantalla secundaria.
        pantalla,
        # Texto del botón.
        text="Gráfica Vuelos por Compañía",
        # Función que se ejecuta al pulsarlo.
        command=accion_grafica_airlines,
        # Ancho del botón.
        width=30
    # Colocamos el botón.
    ).pack(pady=5)

    # Creamos botón para la gráfica de vuelos Schengen/no Schengen.
    tk.Button(
        # El botón pertenece a la pantalla secundaria.
        pantalla,
        # Texto del botón.
        text="Gráfica Vuelos Schengen",
        # Función que se ejecuta al pulsarlo.
        command=accion_grafica_tipo_vuelos,
        # Ancho del botón.
        width=30
    # Colocamos el botón.
    ).pack(pady=5)

    # Creamos botón para cerrar la pantalla secundaria.
    tk.Button(
        # El botón pertenece a la pantalla secundaria.
        pantalla,
        # Texto del botón.
        text="Cerrar Pantalla",
        # Función para cerrar la pantalla secundaria.
        command=pantalla.destroy,
        # Color del texto.
        fg="red",
        # Ancho del botón.
        width=30
    # Colocamos el botón.
    ).pack(pady=25)


# ---------------- INTERFAZ ----------------
# A partir de aquí se construyen los elementos visibles de la ventana principal.

# Creamos el título principal de la aplicación.
tk.Label(
    # El Label pertenece a la ventana principal.
    root,
    # Texto principal.
    text="SISTEMA AEROPORTUARIO",
    # Fuente del texto.
    font=("Arial", 15, "bold"),
    # Color de fondo.
    bg="#f8f9fa"
# Colocamos el título en la ventana.
).pack(pady=15)

# Creamos el botón para cargar aeropuertos y vuelos.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Cargar Airports y Arrivals",
    # Función que se ejecuta al pulsarlo.
    command=accion_cargar,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#dbeafe"
# Colocamos el botón.
).pack(pady=5)


# Creamos el título de la sección de versión 3.
tk.Label(
    # El Label pertenece a la ventana principal.
    root,
    # Texto de la sección.
    text="--- Versión 3: Puertas LEBL ---",
    # Fuente del texto.
    font=("Arial", 11, "bold"),
    # Color de fondo.
    bg="#f8f9fa"
# Colocamos el Label.
).pack(pady=10)

# Creamos el botón para cargar la estructura LEBL.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Cargar estructura LEBL",
    # Función que se ejecuta al pulsarlo.
    command=accion_cargar_lebl,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#fde68a"
# Colocamos el botón.
).pack(pady=5)

# Creamos el botón para asignar puertas.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Asignar puertas a vuelos",
    # Función que se ejecuta al pulsarlo.
    command=accion_asignar_puertas,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#fde68a"
# Colocamos el botón.
).pack(pady=5)

# Creamos el botón para mostrar ocupación de puertas.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Mostrar ocupación de puertas",
    # Función que se ejecuta al pulsarlo.
    command=accion_mostrar_ocupacion,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#fde68a"
# Colocamos el botón.
).pack(pady=5)


# Creamos el título de la sección de gráficas.
tk.Label(
    # El Label pertenece a la ventana principal.
    root,
    # Texto de la sección.
    text="--- Gráficas ---",
    # Fuente del texto.
    font=("Arial", 11, "bold"),
    # Color de fondo.
    bg="#f8f9fa"
# Colocamos el Label.
).pack(pady=10)

# Creamos el botón que abre la pantalla de gráficas.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Abrir Pantalla de Gráficas",
    # Función que se ejecuta al pulsarlo.
    command=abrir_pantalla_graficas,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#e0e7ff"
# Colocamos el botón.
).pack(pady=5)


# Creamos el título de la sección de mapas.
tk.Label(
    # El Label pertenece a la ventana principal.
    root,
    # Texto de la sección.
    text="--- Mapas Google Earth ---",
    # Fuente del texto.
    font=("Arial", 11, "bold"),
    # Color de fondo.
    bg="#f8f9fa"
# Colocamos el Label.
).pack(pady=10)

# Creamos el botón del mapa de vuelos.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Mapa Vuelos Google Earth",
    # Función que se ejecuta al pulsarlo.
    command=accion_mapa_vuelos,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#dcfce7"
# Colocamos el botón.
).pack(pady=5)

# Creamos el botón del mapa de aeropuertos.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="Mapa Aeropuertos Google Earth",
    # Función que se ejecuta al pulsarlo.
    command=accion_mapa_airports,
    # Ancho del botón.
    width=30,
    # Color de fondo del botón.
    bg="#dcfce7"
# Colocamos el botón.
).pack(pady=5)

# Creamos la etiqueta donde se mostrará el estado de la aplicación.
etiqueta_estado = tk.Label(
    # La etiqueta pertenece a la ventana principal.
    root,
    # Texto inicial de la etiqueta.
    text="Estado: esperando cargar archivos.",
    # Color de fondo.
    bg="#f8f9fa",
    # Color del texto.
    fg="#374151",
    # Fuente del texto.
    font=("Arial", 9)
)

# Colocamos la etiqueta de estado.
etiqueta_estado.pack(pady=15)

# Creamos el botón para salir de la aplicación.
tk.Button(
    # El botón pertenece a la ventana principal.
    root,
    # Texto del botón.
    text="SALIR",
    # Función que cierra la ventana principal.
    command=root.destroy,
    # Color del texto.
    fg="red",
    # Ancho del botón.
    width=30
# Colocamos el botón.
).pack(pady=15)

# Iniciamos el bucle principal de tkinter para que la ventana se mantenga abierta.
root.mainloop()
