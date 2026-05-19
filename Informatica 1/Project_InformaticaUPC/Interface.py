import tkinter as tk
from tkinter import messagebox

from Airport import *
from Aircraft import *
from LEBL import *


root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1 - Versión 3")
root.geometry("1180x780")
root.configure(bg="#FAF3E0")


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


# --- FUNCIÓN DE TEXTO ORIGINAL (Para los botones verdes) ---
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


# --- FUNCIÓN INDEPENDIENTE PARA EL MAPA GRÁFICO (Para los botones naranjas) ---
def mostrar_mapa_grafico(nombre_terminal):
    if bcn == "" or bcn == -1:
        messagebox.showwarning("Error", "Primero debes cargar la estructura.")
    else:
        ventana_mapa = tk.Toplevel()
        ventana_mapa.transient(root)
        ventana_mapa.title("Mapa Estructural - " + nombre_terminal)
        ventana_mapa.geometry("1000x700")
        ventana_mapa.configure(bg="#f4f4f0")
        ocupacion = GateOccupancy(bcn)

        # 2. Contenedor y barras de scroll (¡Todas van dentro del else!)
        frame_canvas = tk.Frame(ventana_mapa)
        frame_canvas.pack(fill=tk.BOTH, expand=True)

        vbar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL)
        hbar = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)

        canvas = tk.Canvas(frame_canvas, bg="#f4f4f0", highlightthickness=0,
                           yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        vbar.config(command=canvas.yview)
        hbar.config(command=canvas.xview)

        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 3. Filtrado de datos por terminal
        puertas_terminal = []
        i = 0
        while i < len(ocupacion):
            if ocupacion[i][0] == nombre_terminal:
                puertas_terminal.append(ocupacion[i])
            i = i + 1

        areas = []
        i = 0
        while i < len(puertas_terminal):
            area = puertas_terminal[i][1]
            if area not in areas:
                areas.append(area)
            i = i + 1

        COLOR_PASILLO = "#185c7a"
        COLOR_LIBRE = "#00a650"    # Verde puro
        COLOR_OCUPADO = "#ff0000"  # Rojo puro

        canvas.create_text(50, 50, text=nombre_terminal, font=("Arial", 26, "bold"), anchor="e")

        # Pasillo horizontal principal
        ancho_total = len(areas) * 240 + 120
        canvas.create_rectangle(80, 35, ancho_total, 65, fill=COLOR_PASILLO, outline="black")

        # 4. Dibujo de pasillos y puertas compactas
        a = 0
        while a < len(areas):
            area_actual = areas[a]
            x_centro = 160 + (a * 240)

            puertas_area = []
            p = 0
            while p < len(puertas_terminal):
                if puertas_terminal[p][1] == area_actual:
                    puertas_area.append(puertas_terminal[p])
                p = p + 1

            num_puertas = len(puertas_area)
            largo_pasillo = 80 + ((num_puertas // 2) + 1) * 45

            # Pasillo vertical
            canvas.create_rectangle(x_centro - 12, 65, x_centro + 12, largo_pasillo, fill=COLOR_PASILLO, outline="black")

            nombre_base = nombre_terminal + "BA" + area_actual.lower()
            canvas.create_text(x_centro, largo_pasillo + 20, text=nombre_base, font=("Arial", 12, "bold"))

            g = 0
            while g < len(puertas_area):
                nombre_puerta = puertas_area[g][2]
                ocupado = puertas_area[g][3]
                avion = puertas_area[g][4]

                y_pos = 100 + (g // 2) * 45

                if g % 2 == 0:  # Derecha
                    x_fin_linea = x_centro + 40
                    x_caja_1 = x_fin_linea
                    x_caja_2 = x_fin_linea + 22
                    x_texto_avion = x_caja_2 + 6
                    anclaje_avion = "w"
                    x_texto_puerta = x_fin_linea + 4
                    anclaje_puerta = "w"
                else:  # Izquierda
                    x_fin_linea = x_centro - 40
                    x_caja_1 = x_fin_linea - 22
                    x_caja_2 = x_fin_linea
                    x_texto_avion = x_caja_1 - 6
                    anclaje_avion = "e"
                    x_texto_puerta = x_fin_linea - 4
                    anclaje_puerta = "e"

                # Líneas de los jetways
                canvas.create_line(x_centro, y_pos, x_fin_linea, y_pos, width=3, fill=COLOR_PASILLO)

                # Cajas Rojo/Verde según ocupación
                if ocupado == True:
                    color_caja = COLOR_OCUPADO
                else:
                    color_caja = COLOR_LIBRE
                canvas.create_rectangle(x_caja_1, y_pos - 6, x_caja_2, y_pos + 6, fill=color_caja, outline="black")

                # Letra tamaño 7 para las puertas
                canvas.create_text(x_texto_puerta, y_pos - 12, text=nombre_puerta, font=("Arial", 7), anchor=anclaje_puerta)

                if ocupado == True:
                    canvas.create_text(x_texto_avion, y_pos, text=avion, font=("Arial", 9, "bold"), anchor=anclaje_avion)

                g = g + 1
            a = a + 1

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

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


# Funciones puente para los nuevos botones naranjas
def accion_grafica_puertas_T1():
    mostrar_mapa_grafico("T1")


def accion_grafica_puertas_T2():
    mostrar_mapa_grafico("T2")


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
    text="SISTEMA AEROPORTUARIO ",
    font=("Arial", 19, "bold"),
    bg="#FAF3E0"
).pack(pady=8)


frame_principal = tk.Frame(root, bg="#FAF3E0")
frame_principal.pack(pady=2)


# ---------------- COLUMNA IZQUIERDA ----------------
frame_izquierda = tk.Frame(frame_principal, bg="#FAF3E0")
frame_izquierda.grid(row=0, column=0, padx=12, pady=150, sticky="n")


tk.Label(
    frame_izquierda,
    text="--- CARGA DE DATOS ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=5)

tk.Button(
    frame_izquierda,
    text="Cargar aeropuertos y vuelos",
    command=accion_cargar,
    width=34,
    height=1,
    bg="#A8DADC",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Cargar estructura LEBL",
    command=accion_cargar_LEBL,
    width=34,
    height=1,
    bg="#A8DADC",
    font=("Arial", 10, "bold")
).pack(pady=3)


tk.Label(
    frame_izquierda,
    text="--- NUEVO AVIÓN ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=8)

frame_formulario = tk.Frame(frame_izquierda, bg="#FAF3E0")
frame_formulario.pack(pady=2)

tk.Label(frame_formulario, text="ID avión:", bg="#FAF3E0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=3)
entrada_id = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_id.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Origen ICAO:", bg="#FAF3E0", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=3)
entrada_origen = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_origen.grid(row=1, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Hora llegada:", bg="#FAF3E0", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=3)
entrada_llegada = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_llegada.grid(row=2, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Aerolínea ICAO:", bg="#FAF3E0", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=3)
entrada_aerolinea = tk.Entry(frame_formulario, width=22, font=("Arial", 10))
entrada_aerolinea.grid(row=3, column=1, padx=5, pady=3)

tk.Button(
    frame_izquierda,
    text="Añadir avión a la lista",
    command=accion_anadir_avion,
    width=34,
    height=1,
    bg="#C7D9B7",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_izquierda,
    text="Añadir avión y asignar puerta",
    command=accion_anadir_y_asignar,
    width=34,
    height=1,
    bg="#C7D9B7",
    font=("Arial", 10, "bold")
).pack(pady=3)


# ---------------- COLUMNA CENTRAL ----------------
frame_centro = tk.Frame(frame_principal, bg="#FAF3E0")
frame_centro.grid(row=0, column=1, padx=12, pady=0, sticky="n")

tk.Label(
    frame_centro,
    text="Vuelos cargados / añadidos",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=5)

caja_vuelos = tk.Text(frame_centro, width=57, height=16, font=("Arial", 10))
caja_vuelos.pack(pady=3)

tk.Label(
    frame_centro,
    text="Ocupación de puertas",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=8)

caja_ocupacion = tk.Text(frame_centro, width=57, height=18, font=("Arial", 10))
caja_ocupacion.pack(pady=3)


etiqueta_estado = tk.Label(
    root,
    text="Estado: esperando cargar archivos.",
    bg="#FAF3E0",
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


# ---------------- COLUMNA DERECHA ----------------
frame_derecha = tk.Frame(frame_principal, bg="#FAF3E0")
frame_derecha.grid(row=0, column=2, padx=12, pady=50, sticky="n")

tk.Label(
    frame_derecha,
    text="--- GRÁFICAS ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=5)

tk.Button(
    frame_derecha,
    text="Gráfica Aeropuertos",
    command=accion_grafica_airports,
    width=32,
    height=1,
    bg="#F6E7A9",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Gráfica Llegadas",
    command=accion_grafica_llegadas,
    width=32,
    height=1,
    bg="#F6E7A9",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Gráfica Aerolíneas",
    command=accion_grafica_airlines,
    width=32,
    height=1,
    bg="#F6E7A9",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Gráfica Schengen Vuelos",
    command=accion_grafica_tipo_vuelos,
    width=32,
    height=1,
    bg="#F6E7A9",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Label(
    frame_derecha,
    text="--- GESTIÓN DE PUERTAS ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=8)

tk.Button(
    frame_derecha,
    text="Asignar puertas a todos los vuelos",
    command=accion_asignar_todos,
    width=34,
    height=1,
    bg="#F4B183",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Ver ocupación T1",
    command=accion_ver_T1,
    width=34,
    height=1,
    bg="#F4B183",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Ver ocupación T2",
    command=accion_ver_T2,
    width=34,
    height=1,
    bg="#F4B183",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Label(
    frame_derecha,
    text="--- MAPA GRÁFICO DE PUERTAS ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=8)

tk.Button(
    frame_derecha,
    text="Ver gráfica de puertas T1",
    command=accion_grafica_puertas_T1,
    width=34,
    height=1,
    bg="#CDB4DB",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Ver gráfica de puertas T2",
    command=accion_grafica_puertas_T2,
    width=34,
    height=1,
    bg="#CDB4DB",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Label(
    frame_derecha,
    text="--- MAPAS GOOGLE EARTH ---",
    font=("Arial", 12, "bold"),
    bg="#FAF3E0"
).pack(pady=15)

tk.Button(
    frame_derecha,
    text="Mapa Aeropuertos Google Earth",
    command=accion_mapa_airports,
    width=32,
    height=1,
    bg="#E5989B",
    font=("Arial", 10, "bold")
).pack(pady=3)

tk.Button(
    frame_derecha,
    text="Mapa Vuelos Google Earth",
    command=accion_mapa_vuelos,
    width=32,
    height=1,
    bg="#E5989B",
    font=("Arial", 10, "bold")
).pack(pady=3)


actualizar_pantalla_vuelos()

root.mainloop()