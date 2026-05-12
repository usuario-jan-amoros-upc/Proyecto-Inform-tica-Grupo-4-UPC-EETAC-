import tkinter as tk
from tkinter import messagebox

from Airport import *

from Aircraft import *


root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1")
root.geometry("400x600")
root.configure(bg="#f8f9fa")

lista_airports=[]
lista_vuelos=[]

def accion_cargar():
    global lista_airports, lista_vuelos
    lista_airports= LoadAirports("Airports.txt")
    lista_vuelos= LoadArrivals("Arrivals.txt")

    i=0
    while i<len(lista_airports):
        SetSchengen(lista_airports[i])
        i=i+1

    messagebox.showinfo("INFO", "Datos cargados correctamente.")

def accion_graficas_vuelos():
    if len(lista_vuelos) > 0:   #Llamamos las funciones de la Version 2
        PlotArrivals(lista_vuelos)
        PlotAirlines(lista_vuelos)
    else:
        messagebox.showwarning("Error", "¡La lista de vuelos está vacia.")

def accion_mapa_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0: #Generamos los mapas
        MapFlights(lista_vuelos, lista_airports)
        messagebox.showinfo("INFO", "Mapa KML de vuelos generado.")
    else:
        messagebox.showwarning("Error", "Faltan datos para el mapa.")

def accion_inspeccion():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        #Usamos función de larga distancia
        lejanos = LongDistanceArrivals(lista_vuelos, lista_airports)
        MapFlights(lejanos, lista_airports)
        messagebox.showinfo("INFO", "Mapa de vuelos lejanos generado.")
    else:
        messagebox.showwarning("Error", "No hay datos suficientes.")

#Título
tk.Label(root, text="SISTEMA AEROPORTUARIO", font=("Arial", 14, "bold")).pack(pady=20)

tk.Button(root, text="Cargar Archivos", command=accion_cargar, width=25).pack(pady=5)

tk.Label(root, text="--- Aeropuertos ---").pack(pady=10)
tk.Button(root, text="Ver Gráfica Schengen", command=lambda: PlotAirports(lista_airports), width=25).pack(pady=5)
tk.Button(root, text="Mapa Aeropuertos", command=lambda: MapAirports(lista_airports), width=25).pack(pady=5)

tk.Label(root, text="--- Vuelos ---").pack(pady=10)
tk.Button(root, text="Ver Gráficas de Vuelos", command=accion_graficas_vuelos, width=25).pack(pady=5)
tk.Button(root, text="Generar Mapa Vuelos", command=accion_mapa_vuelos, width=25).pack(pady=5)
tk.Button(root, text="Vuelos Larga Distancia", command=accion_inspeccion, width=25).pack(pady=5)

tk.Button(root, text="SALIR", command=root.destroy, fg="red").pack(pady=30)

root.mainloop()



