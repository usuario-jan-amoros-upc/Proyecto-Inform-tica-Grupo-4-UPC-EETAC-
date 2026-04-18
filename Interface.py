import tkinter as tk
from tkinter import messagebox
from Airport import *

root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1")
root.geometry("300x400")

lista_global = []

def accion_cargar():
    global lista_global
    lista_global = LoadAirports("airports.txt")
    messagebox.showinfo("INFO", f"Cargados {len(lista_global)} aeropuertos.")

def accion_grafica():
    if len(lista_global) > 0:
        PlotAirports(lista_global)
    else:
        messagebox.showwarning("Error", "La lista está vacía. ¡Cárgala primero!")

def accion_mapa():
    if len(lista_global) > 0:
        MapAirports(lista_global)
        messagebox.showinfo("INFO", "Mapa KML generado con éxito.")
    else:
        messagebox.showwarning("Error", "No hay datos para el mapa.")

tk.Label(root, text="Panel de Aeropuertos", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Cargar Datos", command=accion_cargar, width=20).pack(pady=10)
tk.Button(root, text="Ver Gráfica", command=accion_grafica, width=20).pack(pady=10)
tk.Button(root, text="Generar Mapa", command=accion_mapa, width=20).pack(pady=10)

tk.Button(root, text="Salir", command=root.destroy, fg="red").pack(pady=30)

root.mainloop()