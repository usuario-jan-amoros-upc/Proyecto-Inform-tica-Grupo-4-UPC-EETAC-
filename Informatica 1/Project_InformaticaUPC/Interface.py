import tkinter as tk
from tkinter import messagebox

from Airport import *
from Aircraft import *
from LEBL import *


root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1 - Versión 3")
root.geometry("1180x780")
root.configure(bg="#f8f9fa")


lista_airports = []
lista_vuelos = []
bcn = ""


def cambiar_estado(texto):
    etiqueta_estado.config(text=texto)


def actualizar_pantalla_vuelos():
    caja_vuelos.delete("1.0", tk.END)

    caja_vuelos.insert(tk.END, "ID AVIÓN | ORIGEN | LLEGADA | AEROLÍNEA\n")
    caja_vuelos.insert(tk.END, "----------------------------------------\n")

    i = 0
    while i < len(lista_vuelos):
        avion = lista_vuelos[i]

        linea = (
            avion.aircraft_id + " | "
            + avion.origin + " | "
            + avion.arrival_time + " | "
            + avion.airline + "\n"
        )

        caja_vuelos.insert(tk.END, linea)

        i = i + 1


def actualizar_ocupacion(nombre_terminal):
    caja_ocupacion.delete("1.0", tk.END)

    if bcn == "" or bcn == -1:
        caja_ocupacion.insert(tk.END, "Primero debes cargar la estructura de LEBL.\n")

    else:
        ocupacion = GateOccupancy(bcn)

        caja_ocupacion.insert(tk.END, "OCUPACIÓN " + nombre_terminal + "\n")
        caja_ocupacion.insert(tk.END, "----------------------------------------\n")

        total = 0
        libres = 0
        ocupadas = 0

        i = 0
        while i < len(ocupacion):
            terminal = ocupacion[i][0]
            area = ocupacion[i][1]
            gate = ocupacion[i][2]
            ocupado = ocupacion[i][3]
            avion = ocupacion[i][4]

            if terminal == nombre_terminal:
                total = total + 1

                if ocupado == True:
                    estado = "OCUPADA"
                    ocupadas = ocupadas + 1
                else:
                    estado = "LIBRE"
                    libres = libres + 1

                linea = terminal + " | " + area + " | " + gate + " | " + estado + " | " + avion + "\n"
                caja_ocupacion.insert(tk.END, linea)

            i = i + 1

        caja_ocupacion.insert(tk.END, "\nTOTAL: " + str(total))
        caja_ocupacion.insert(tk.END, " | LIBRES: " + str(libres))
        caja_ocupacion.insert(tk.END, " | OCUPADAS: " + str(ocupadas))


def accion_cargar():
    global lista_airports, lista_vuelos

    lista_airports = LoadAirports("airports.txt")
    lista_vuelos = LoadArrivals("Arrivals.txt")

    i = 0
    while i < len(lista_airports):
        SetSchengen(lista_airports[i])
        i = i + 1

    actualizar_pantalla_vuelos()
    cambiar_estado("Datos cargados correctamente.")
    messagebox.showinfo("INFO", "Datos cargados correctamente.")


def accion_cargar_LEBL():
    global bcn

    bcn = LoadAirportStructure("LEBL.txt")

    if bcn == -1:
        cambiar_estado("Error al cargar LEBL.txt.")
        messagebox.showwarning("Error", "No se ha podido cargar LEBL.txt.")
    else:
        cambiar_estado("Estructura LEBL cargada correctamente.")
        messagebox.showinfo("INFO", "Estructura LEBL cargada correctamente.")


def accion_anadir_avion():
    id_avion = entrada_id.get()
    origen = entrada_origen.get()
    llegada = entrada_llegada.get()
    aerolinea = entrada_aerolinea.get()

    if id_avion == "" or origen == "" or llegada == "" or aerolinea == "":
        messagebox.showwarning("Error", "Debes rellenar todos los campos.")

    else:
        nuevo = Aircraft(id_avion, aerolinea, origen, llegada)
        lista_vuelos.append(nuevo)

        entrada_id.delete(0, tk.END)
        entrada_origen.delete(0, tk.END)
        entrada_llegada.delete(0, tk.END)
        entrada_aerolinea.delete(0, tk.END)

        actualizar_pantalla_vuelos()
        cambiar_estado("Avión añadido a la lista: " + id_avion)


def accion_anadir_y_asignar():
    global bcn

    id_avion = entrada_id.get()
    origen = entrada_origen.get()
    llegada = entrada_llegada.get()
    aerolinea = entrada_aerolinea.get()

    if id_avion == "" or origen == "" or llegada == "" or aerolinea == "":
        messagebox.showwarning("Error", "Debes rellenar todos los campos.")

    else:
        if bcn == "" or bcn == -1:
            messagebox.showwarning("Error", "Primero debes cargar la estructura LEBL.")

        else:
            nuevo = Aircraft(id_avion, aerolinea, origen, llegada)
            lista_vuelos.append(nuevo)

            resultado = AssignGate(bcn, nuevo)

            entrada_id.delete(0, tk.END)
            entrada_origen.delete(0, tk.END)
            entrada_llegada.delete(0, tk.END)
            entrada_aerolinea.delete(0, tk.END)

            actualizar_pantalla_vuelos()

            if resultado == -1:
                cambiar_estado("Avión añadido, pero no se pudo asignar puerta.")
                messagebox.showwarning("Aviso", "Avión añadido, pero no se pudo asignar puerta.")
            else:
                cambiar_estado("Avión añadido y puerta asignada: " + id_avion)


def accion_asignar_todos():
    if bcn == "" or bcn == -1:
        messagebox.showwarning("Error", "Primero debes cargar la estructura LEBL.")

    else:
        if len(lista_vuelos) == 0:
            messagebox.showwarning("Error", "Primero debes cargar o añadir vuelos.")

        else:
            asignados = 0
            errores = 0

            i = 0
            while i < len(lista_vuelos):
                resultado = AssignGate(bcn, lista_vuelos[i])

                if resultado == -1:
                    errores = errores + 1
                else:
                    asignados = asignados + 1

                i = i + 1

            cambiar_estado("Asignados: " + str(asignados) + " | Sin puerta: " + str(errores))
            messagebox.showinfo("INFO", "Asignación finalizada.")


def accion_ver_T1():
    actualizar_ocupacion("T1")


def accion_ver_T2():
    actualizar_ocupacion("T2")


def accion_grafica_airports():
    if len(lista_airports) > 0:
        PlotAirports(lista_airports)
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos.")


def accion_grafica_llegadas():
    if len(lista_vuelos) > 0:
        PlotArrivals(lista_vuelos)
    else:
        messagebox.showwarning("Error", "Primero debes cargar vuelos.")


def accion_grafica_airlines():
    if len(lista_vuelos) > 0:
        PlotAirlines(lista_vuelos)
    else:
        messagebox.showwarning("Error", "Primero debes cargar vuelos.")


def accion_grafica_tipo_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        PlotFlightsType(lista_vuelos, lista_airports)
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos y vuelos.")


def accion_mapa_airports():
    if len(lista_airports) > 0:
        MapAirports(lista_airports)
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos.")


def accion_mapa_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        MapFlights(lista_vuelos, lista_airports)
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos y vuelos.")


# ---------------- INTERFAZ ----------------

tk.Label(
    root,
    text="SISTEMA AEROPORTUARIO - VERSIÓN 3",
    font=("Arial", 19, "bold"),
    bg="#f8f9fa"
).pack(pady=8)


# Frame principal con las 3 columnas.
frame_principal = tk.Frame(root, bg="#f8f9fa")
frame_principal.pack(pady=2)


# ---------------- COLUMNA IZQUIERDA ----------------
# Carga de datos, nuevo avión y gestión de puertas.

frame_izquierda = tk.Frame(frame_principal, bg="#f8f9fa")
frame_izquierda.grid(row=0, column=0, padx=12, pady=0, sticky="n")


tk.Label(
    frame_izquierda,
    text="--- CARGA DE DATOS ---",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=5)

tk.Button(
    frame_izquierda,
    text="Cargar aeropuertos y vuelos",
    command=accion_cargar,
    width=34,
    height=1,
    bg="#dbeafe",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Cargar estructura LEBL",
    command=accion_cargar_LEBL,
    width=34,
    height=1,
    bg="#dbeafe",
    font=("Arial", 10, "bold")
).pack(pady=3)


tk.Label(
    frame_izquierda,
    text="--- NUEVO AVIÓN ---",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=8)

frame_formulario = tk.Frame(frame_izquierda, bg="#f8f9fa")
frame_formulario.pack(pady=2)

tk.Label(frame_formulario, text="ID avión:", bg="#f8f9fa", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=3)
entrada_id = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_id.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Origen ICAO:", bg="#f8f9fa", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=3)
entrada_origen = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_origen.grid(row=1, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Hora llegada:", bg="#f8f9fa", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=3)
entrada_llegada = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_llegada.grid(row=2, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Aerolínea ICAO:", bg="#f8f9fa", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=3)
entrada_aerolinea = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_aerolinea.grid(row=3, column=1, padx=5, pady=3)

tk.Button(
    frame_izquierda,
    text="Añadir avión a la lista",
    command=accion_anadir_avion,
    width=34,
    height=1,
    bg="#fde68a",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Añadir avión y asignar puerta",
    command=accion_anadir_y_asignar,
    width=34,
    height=1,
    bg="#fde68a",
    font=("Arial", 10, "bold")
).pack(pady=3)


tk.Label(
    frame_izquierda,
    text="--- GESTIÓN DE PUERTAS ---",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=8)

tk.Button(
    frame_izquierda,
    text="Asignar puertas a todos los vuelos",
    command=accion_asignar_todos,
    width=34,
    height=1,
    bg="#dcfce7",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Ver ocupación T1",
    command=accion_ver_T1,
    width=34,
    height=1,
    bg="#dcfce7",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Ver ocupación T2",
    command=accion_ver_T2,
    width=34,
    height=1,
    bg="#dcfce7",
    font=("Arial", 10, "bold")
).pack(pady=3)


# ---------------- COLUMNA CENTRAL ----------------
# Gráficas y mapas separados, colocados arriba.

frame_centro = tk.Frame(frame_principal, bg="#f8f9fa")
frame_centro.grid(row=0, column=1, padx=12, pady=0, sticky="n")


tk.Label(
    frame_centro,
    text="--- GRÁFICAS ---",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=5)

tk.Button(
    frame_centro,
    text="Gráfica Aeropuertos",
    command=accion_grafica_airports,
    width=32,
    height=1,
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_centro,
    text="Gráfica Llegadas",
    command=accion_grafica_llegadas,
    width=32,
    height=1,
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_centro,
    text="Gráfica Aerolíneas",
    command=accion_grafica_airlines,
    width=32,
    height=1,
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_centro,
    text="Gráfica Schengen Vuelos",
    command=accion_grafica_tipo_vuelos,
    width=32,
    height=1,
    font=("Arial", 10, "bold")
).pack(pady=3)


tk.Label(
    frame_centro,
    text="--- MAPAS GOOGLE EARTH ---",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=15)

tk.Button(
    frame_centro,
    text="Mapa Aeropuertos Google Earth",
    command=accion_mapa_airports,
    width=32,
    height=1,
    bg="#bbf7d0",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_centro,
    text="Mapa Vuelos Google Earth",
    command=accion_mapa_vuelos,
    width=32,
    height=1,
    bg="#bbf7d0",
    font=("Arial", 10, "bold")
).pack(pady=3)


# ---------------- COLUMNA DERECHA ----------------
# Pantallas de datos visibles desde que se abre la interfaz.

frame_derecha = tk.Frame(frame_principal, bg="#f8f9fa")
frame_derecha.grid(row=0, column=2, padx=12, pady=0, sticky="n")


tk.Label(
    frame_derecha,
    text="Vuelos cargados / añadidos",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=5)

caja_vuelos = tk.Text(frame_derecha, width=57, height=16, font=("Arial", 10))
caja_vuelos.pack(pady=3)


tk.Label(
    frame_derecha,
    text="Ocupación de puertas",
    font=("Arial", 12, "bold"),
    bg="#f8f9fa"
).pack(pady=8)

caja_ocupacion = tk.Text(frame_derecha, width=57, height=18, font=("Arial", 10))
caja_ocupacion.pack(pady=3)


etiqueta_estado = tk.Label(
    root,
    text="Estado: esperando cargar archivos.",
    bg="#f8f9fa",
    fg="#374151",
    font=("Arial", 10, "bold")
)
etiqueta_estado.pack(pady=6)


tk.Button(
    root,
    text="SALIR",
    command=root.destroy,
    fg="red",
    width=34,
    height=1,
    font=("Arial", 10, "bold")
).pack(pady=4)


# Esto hace que la pantalla de vuelos aparezca ya con cabecera al abrir el programa.
actualizar_pantalla_vuelos()

root.mainloop()
