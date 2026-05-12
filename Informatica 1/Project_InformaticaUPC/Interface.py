import tkinter as tk
from tkinter import messagebox

from Airport import *
from Aircraft import *


root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1")
root.geometry("430x700")
root.configure(bg="#f8f9fa")

lista_airports = []
lista_vuelos = []


def cambiar_estado(texto):
    etiqueta_estado.config(text=texto)


def accion_cargar():
    global lista_airports, lista_vuelos

    lista_airports = LoadAirports("Airports.txt")
    lista_vuelos = LoadArrivals("Arrivals.txt")

    i = 0
    while i < len(lista_airports):
        SetSchengen(lista_airports[i])
        i = i + 1

    cambiar_estado("Datos cargados correctamente.")
    messagebox.showinfo("INFO", "Datos cargados correctamente.")


def accion_grafica_airports():
    if len(lista_airports) > 0:
        PlotAirports(lista_airports)
        cambiar_estado("Gráfica Schengen de aeropuertos mostrada.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar los aeropuertos.")


def accion_mapa_airports():
    if len(lista_airports) > 0:
        MapAirports(lista_airports)
        cambiar_estado("Mapa de aeropuertos abierto en Google Earth.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar los aeropuertos.")


def accion_grafica_llegadas():
    if len(lista_vuelos) > 0:
        PlotArrivals(lista_vuelos)
        cambiar_estado("Gráfica de llegadas por hora mostrada.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar los vuelos.")


def accion_grafica_airlines():
    if len(lista_vuelos) > 0:
        PlotAirlines(lista_vuelos)
        cambiar_estado("Gráfica de vuelos por compañía mostrada.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar los vuelos.")


def accion_grafica_tipo_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        PlotFlightsType(lista_vuelos, lista_airports)
        cambiar_estado("Gráfica Schengen / No Schengen de vuelos mostrada.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos y vuelos.")


def accion_mapa_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        MapFlights(lista_vuelos, lista_airports)
        cambiar_estado("Mapa de vuelos abierto en Google Earth.")
    else:
        messagebox.showwarning("Error", "Faltan datos para abrir el mapa.")


def accion_inspeccion():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        lejanos = LongDistanceArrivals(lista_vuelos, lista_airports)

        if len(lejanos) > 0:
            MapFlights(lejanos, lista_airports)
            cambiar_estado("Mapa de vuelos de larga distancia abierto en Google Earth.")
        else:
            cambiar_estado("No hay vuelos de larga distancia.")
            messagebox.showinfo("INFO", "No hay vuelos de larga distancia.")
    else:
        messagebox.showwarning("Error", "No hay datos suficientes.")


# ---------------- INTERFAZ ----------------

tk.Label(
    root,
    text="SISTEMA AEROPORTUARIO",
    font=("Arial", 15, "bold"),
    bg="#f8f9fa"
).pack(pady=20)

tk.Button(
    root,
    text="Cargar Archivos",
    command=accion_cargar,
    width=30,
    bg="#dbeafe"
).pack(pady=5)


tk.Label(
    root,
    text="--- Gráfica Aeropuertos ---",
    font=("Arial", 11, "bold"),
    bg="#f8f9fa"
).pack(pady=10)

tk.Button(
    root,
    text="Gráfica Aeropuertos Schengen",
    command=accion_grafica_airports,
    width=30
).pack(pady=5)

tk.Label(
    root,
    text="--- Gráficas de Vuelos ---",
    font=("Arial", 11, "bold"),
    bg="#f8f9fa"
).pack(pady=10)

tk.Button(
    root,
    text="Gráfica Llegadas por Hora",
    command=accion_grafica_llegadas,
    width=30
).pack(pady=5)

tk.Button(
    root,
    text="Gráfica Vuelos por Compañía",
    command=accion_grafica_airlines,
    width=30
).pack(pady=5)

tk.Button(
    root,
    text="Gráfica Vuelos Schengen",
    command=accion_grafica_tipo_vuelos,
    width=30
).pack(pady=5)


tk.Label(
    root,
    text="--- Mapas Google Earth ---",
    font=("Arial", 11, "bold"),
    bg="#f8f9fa"
).pack(pady=10)

tk.Button(
    root,
    text="Mapa Vuelos Google Earth",
    command=accion_mapa_vuelos,
    width=30,
    bg="#dcfce7"
).pack(pady=5)

tk.Button(
    root,
    text="Mapa Aeropuertos Google Earth",
    command=accion_mapa_airports,
    width=30,
    bg="#dcfce7"
).pack(pady=5)

etiqueta_estado = tk.Label(
    root,
    text="Estado: esperando cargar archivos.",
    bg="#f8f9fa",
    fg="#374151",
    font=("Arial", 9)
)
etiqueta_estado.pack(pady=15)

tk.Button(
    root,
    text="SALIR",
    command=root.destroy,
    fg="red",
    width=30
).pack(pady=20)

root.mainloop()


