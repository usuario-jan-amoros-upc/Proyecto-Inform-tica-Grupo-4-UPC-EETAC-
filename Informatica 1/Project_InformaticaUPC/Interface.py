import tkinter as tk
from tkinter import messagebox

from Airport import *
from Aircraft import *
from LEBL import *


root = tk.Tk()
root.title("Gestor de Aeropuertos - INFO1 - Versión 4")
root.geometry("1820x980")
root.configure(bg="#FAF3E0")


lista_airports = []
lista_vuelos = []

# Lista donde guardaremos los vuelos de salida.
lista_departures = []

# Aquí guardaremos la ocupación calculada para cada hora del día.
# Más adelante esta lista tendrá 24 posiciones: una por cada hora.
lista_ocupacion_horas = []

# Aquí guardaremos la foto completa de todas las puertas en cada hora.
# Esto sirve para que el dibujo de puertas cambie al mover la línea del tiempo.
lista_fotos_horas = []

# Guardamos qué terminal está viendo el usuario en la gráfica de puertas.
terminal_grafica_actual = ""

bcn = ""


def cambiar_estado(texto):
    etiqueta_estado.config(text=texto)

# Esta función carga los vuelos de salida desde Departures.txt.
def accion_cargar_departures():
    # Indicamos que vamos a modificar la lista global de salidas.
    global lista_departures

    # De momento suponemos que luego crearemos LoadDepartures en Aircraft.py.
    lista_departures = LoadDepartures("Departures.txt")

    # Si la lista está vacía, avisamos al usuario.
    if len(lista_departures) == 0:
        messagebox.showwarning("Error", "No se han podido cargar las salidas.")

        cambiar_estado("Error al cargar Departures.txt.")

    # Si hay salidas cargadas, informamos al usuario.
    else:
        messagebox.showinfo("INFO", "Salidas cargadas correctamente.")

        cambiar_estado("Departures cargado correctamente.")


def crear_fotos_ocupacion_por_hora():
    # Esta función guarda una foto completa de las puertas en cada hora del día.
    # Así la gráfica de ocupación puede cambiar cuando movemos la línea del tiempo.
    fotos = []

    if bcn == "" or bcn == -1:
        return fotos

    if len(lista_vuelos) == 0 or len(lista_departures) == 0:
        return fotos

    # Juntamos las llegadas y las salidas usando el ID del avión.
    aircrafts = MergeMovements(lista_vuelos, lista_departures)

    if len(aircrafts) == 0:
        return fotos

    # Empezamos con todas las puertas libres y colocamos los aviones nocturnos.
    ResetGates(bcn)
    AssignNightGates(bcn, aircrafts)

    h = 0
    while h < 24:
        if h < 10:
            hora_texto = "0" + str(h) + ":00"
        else:
            hora_texto = str(h) + ":00"

        # Aplicamos salidas y llegadas de esta hora.
        AssignGatesAtTime(bcn, aircrafts, hora_texto)

        # Guardamos una copia de la ocupación de esta hora.
        foto = GateOccupancy(bcn)
        copia = []

        i = 0
        while i < len(foto):
            copia.append([foto[i][0], foto[i][1], foto[i][2], foto[i][3], foto[i][4]])
            i = i + 1

        fotos.append(copia)
        h = h + 1

    return fotos


# Esta función actualizará la pantalla cuando el usuario mueva la línea de horas.
def actualizar_ocupacion_hora(valor):
    # Convertimos el valor recibido a número entero.
    hora = int(valor)

    # Actualizamos el texto que indica la hora seleccionada.
    etiqueta_hora_actual.config(text="Hora seleccionada: " + str(hora) + ":00")

    # Ahora la ocupación por horas se muestra en la pantalla grande de ocupación.
    caja_ocupacion.delete("1.0", tk.END)

    caja_ocupacion.insert(tk.END, "OCUPACIÓN A LAS " + str(hora) + ":00\n")
    caja_ocupacion.insert(tk.END, "----------------------------------------\n")

    # Si todavía no hemos calculado la ocupación por horas, avisamos.
    if len(lista_ocupacion_horas) == 0:
        caja_ocupacion.insert(tk.END, "Primero debes asignar puertas por horas.\n")

    # Si ya existe la ocupación por horas, mostramos la hora seleccionada.
    else:
        ocupacion = lista_ocupacion_horas[hora]

        i = 0
        while i < len(ocupacion):
            caja_ocupacion.insert(tk.END, ocupacion[i] + "\n")
            i = i + 1

        # Si el usuario ya ha elegido T1 o T2, actualizamos también la gráfica.
        if terminal_grafica_actual != "" and len(lista_fotos_horas) == 24:
            dibujar_mapa_grafico_con_ocupacion(terminal_grafica_actual, lista_fotos_horas[hora])



# Esta función llamará más adelante a la función que asigna puertas teniendo en cuenta las horas.
def accion_asignar_puertas_horas():
    # Indicamos que vamos a modificar la ocupación por horas.
    global lista_ocupacion_horas, lista_fotos_horas

    # Comprobamos que LEBL esté cargado.
    if bcn == "" or bcn == -1:
        messagebox.showwarning("Error", "Primero debes cargar la estructura de LEBL.")

    # Comprobamos que las llegadas estén cargadas.
    elif len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Primero debes cargar las llegadas.")

    # Comprobamos que las salidas estén cargadas.
    elif len(lista_departures) == 0:
        messagebox.showwarning("Error", "Primero debes cargar las salidas.")

    else:
        # Calculamos el texto de ocupación por horas.
        lista_ocupacion_horas = AssignGatesByHour(bcn, lista_vuelos, lista_departures)

        # Calculamos también la foto de puertas de cada hora para poder dibujarla.
        lista_fotos_horas = crear_fotos_ocupacion_por_hora()

        # Actualizamos la pantalla con la hora que tenga seleccionada la línea.
        actualizar_ocupacion_hora(linea_horas.get())

        cambiar_estado("Puertas asignadas por horas correctamente.")

        messagebox.showinfo("INFO", "Puertas asignadas por horas correctamente.")


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
def dibujar_mapa_grafico_con_ocupacion(nombre_terminal, ocupacion):
    # Esta función dibuja la gráfica antigua de puertas dentro de la interfaz.
    # La diferencia es que ahora recibe la ocupación que debe dibujar.
    canvas_ocupacion_puertas.delete("all")

    # Filtramos solo las puertas de la terminal elegida.
    puertas_terminal = []
    i = 0
    while i < len(ocupacion):
        if ocupacion[i][0] == nombre_terminal:
            puertas_terminal.append(ocupacion[i])
        i = i + 1

    if len(puertas_terminal) == 0:
        canvas_ocupacion_puertas.create_text(
            ANCHO_CANVAS_OCUPACION // 2,
            ALTO_CANVAS_OCUPACION // 2,
            text="No hay datos de ocupación para " + nombre_terminal,
            font=("Arial", 10, "bold"),
            fill=COLOR_TITULO
        )
        return

    # Sacamos las áreas sin repetirlas.
    areas = []
    i = 0
    while i < len(puertas_terminal):
        area = puertas_terminal[i][1]
        if area not in areas:
            areas.append(area)
        i = i + 1

    COLOR_PASILLO = "#185c7a"
    COLOR_LIBRE = "#00a650"
    COLOR_OCUPADO = "#ff0000"

    canvas_ocupacion_puertas.create_text(
        50,
        50,
        text=nombre_terminal,
        font=("Arial", 26, "bold"),
        anchor="e"
    )

    # Pasillo horizontal principal.
    ancho_total = len(areas) * 240 + 120
    canvas_ocupacion_puertas.create_rectangle(
        80,
        35,
        ancho_total,
        65,
        fill=COLOR_PASILLO,
        outline="black"
    )

    # Dibujamos las áreas y sus puertas.
    a = 0
    max_largo = 160
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

        if largo_pasillo > max_largo:
            max_largo = largo_pasillo

        # Pasillo vertical.
        canvas_ocupacion_puertas.create_rectangle(
            x_centro - 12,
            65,
            x_centro + 12,
            largo_pasillo,
            fill=COLOR_PASILLO,
            outline="black"
        )

        nombre_base = nombre_terminal + "BA" + area_actual.lower()
        canvas_ocupacion_puertas.create_text(
            x_centro,
            largo_pasillo + 20,
            text=nombre_base,
            font=("Arial", 12, "bold")
        )

        g = 0
        while g < len(puertas_area):
            nombre_puerta = puertas_area[g][2]
            ocupado = puertas_area[g][3]
            avion = puertas_area[g][4]

            y_pos = 100 + (g // 2) * 45

            if g % 2 == 0:
                x_fin_linea = x_centro + 40
                x_caja_1 = x_fin_linea
                x_caja_2 = x_fin_linea + 22
                x_texto_avion = x_caja_2 + 6
                anclaje_avion = "w"
                x_texto_puerta = x_fin_linea + 4
                anclaje_puerta = "w"
            else:
                x_fin_linea = x_centro - 40
                x_caja_1 = x_fin_linea - 22
                x_caja_2 = x_fin_linea
                x_texto_avion = x_caja_1 - 6
                anclaje_avion = "e"
                x_texto_puerta = x_fin_linea - 4
                anclaje_puerta = "e"

            canvas_ocupacion_puertas.create_line(
                x_centro,
                y_pos,
                x_fin_linea,
                y_pos,
                width=3,
                fill=COLOR_PASILLO
            )

            if ocupado == True:
                color_caja = COLOR_OCUPADO
            else:
                color_caja = COLOR_LIBRE

            canvas_ocupacion_puertas.create_rectangle(
                x_caja_1,
                y_pos - 6,
                x_caja_2,
                y_pos + 6,
                fill=color_caja,
                outline="black"
            )

            canvas_ocupacion_puertas.create_text(
                x_texto_puerta,
                y_pos - 12,
                text=nombre_puerta,
                font=("Arial", 7),
                anchor=anclaje_puerta
            )

            if ocupado == True:
                canvas_ocupacion_puertas.create_text(
                    x_texto_avion,
                    y_pos,
                    text=avion,
                    font=("Arial", 9, "bold"),
                    anchor=anclaje_avion
                )

            g = g + 1

        a = a + 1

    # Permitimos mover la gráfica con las barras de scroll.
    canvas_ocupacion_puertas.update_idletasks()
    canvas_ocupacion_puertas.config(scrollregion=(0, 0, ancho_total + 80, max_largo + 80))


def mostrar_mapa_grafico(nombre_terminal):
    # Esta función decide qué ocupación se debe dibujar.
    # Si ya se ha calculado la versión por horas, usa la hora de la línea.
    global terminal_grafica_actual

    if bcn == "" or bcn == -1:
        messagebox.showwarning("Error", "Primero debes cargar la estructura.")
    else:
        terminal_grafica_actual = nombre_terminal
        hora = int(linea_horas.get())

        if len(lista_fotos_horas) == 24:
            dibujar_mapa_grafico_con_ocupacion(nombre_terminal, lista_fotos_horas[hora])
        else:
            dibujar_mapa_grafico_con_ocupacion(nombre_terminal, GateOccupancy(bcn))


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


# Estos botones muestran la gráfica antigua de puertas, pero integrada en la pantalla central.
def accion_grafica_puertas_T1():
    actualizar_ocupacion("T1")
    mostrar_mapa_grafico("T1")


def accion_grafica_puertas_T2():
    actualizar_ocupacion("T2")
    mostrar_mapa_grafico("T2")



def limpiar_grafica():
    canvas_grafica.delete("all")


def dibujar_grafica_barras(titulo, etiquetas, valores, colores):
    limpiar_grafica()

    # Usamos el tamaño grande de la pantalla de gráficas.
    ancho = ANCHO_CANVAS_GRAFICA
    alto = ALTO_CANVAS_GRAFICA
    margen_izq = 42
    margen_abajo = 34
    margen_arriba = 34

    canvas_grafica.create_text(
        ancho // 2,
        18,
        text=titulo,
        font=("Arial", 11, "bold"),
        fill=COLOR_TITULO
    )

    canvas_grafica.create_line(margen_izq, alto - margen_abajo, ancho - 20, alto - margen_abajo)
    canvas_grafica.create_line(margen_izq, margen_arriba, margen_izq, alto - margen_abajo)

    if len(valores) == 0:
        canvas_grafica.create_text(ancho // 2, alto // 2, text="No hay datos para mostrar.")
        return

    maximo = valores[0]
    i = 1
    while i < len(valores):
        if valores[i] > maximo:
            maximo = valores[i]
        i = i + 1

    if maximo == 0:
        maximo = 1

    espacio = (ancho - margen_izq - 25) / len(valores)

    i = 0
    while i < len(valores):
        valor = valores[i]

        x1 = margen_izq + i * espacio + 4
        x2 = margen_izq + (i + 1) * espacio - 4

        altura_barra = (valor / maximo) * (alto - margen_abajo - margen_arriba - 10)
        y1 = alto - margen_abajo - altura_barra
        y2 = alto - margen_abajo

        # Elegimos el color de la barra.
        if len(colores) == 0:
            color_barra = COLOR_GRAFICAS
        elif len(colores) == 1:
            color_barra = colores[0]
        else:
            if i < len(colores):
                color_barra = colores[i]
            else:
                color_barra = colores[len(colores) - 1]

        canvas_grafica.create_rectangle(x1, y1, x2, y2, fill=color_barra, outline=COLOR_TITULO)
        canvas_grafica.create_text((x1 + x2) / 2, y1 - 8, text=str(valor), font=("Arial", 8))

        # Si hay pocas etiquetas, se escriben todas. Si hay muchas, se escriben algunas.
        if len(etiquetas) <= 12 or i % 2 == 0:
            canvas_grafica.create_text((x1 + x2) / 2, alto - 15, text=str(etiquetas[i]), font=("Arial", 7))

        i = i + 1


def accion_grafica_airports():
    if len(lista_airports) > 0:
        schengen = 0
        no_schengen = 0

        i = 0
        while i < len(lista_airports):
            if lista_airports[i].Schengen == True:
                schengen = schengen + 1
            else:
                no_schengen = no_schengen + 1
            i = i + 1

        dibujar_grafica_barras(
            "Aeropuertos Schengen / No Schengen",
            ["Schengen", "No Schengen"],
            [schengen, no_schengen],
            ["#9BB8CD", "#FFD6BA"]
        )
        cambiar_estado("Gráfica de aeropuertos mostrada en la interfaz.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar aeropuertos.")


def accion_grafica_llegadas():
    if len(lista_vuelos) > 0:
        horas = [0] * 24

        i = 0
        while i < len(lista_vuelos):
            avion = lista_vuelos[i]
            partes = avion.arrival_time.split(":")
            hora = int(partes[0])

            if 0 <= hora < 24:
                horas[hora] = horas[hora] + 1

            i = i + 1

        etiquetas = []
        i = 0
        while i < 24:
            etiquetas.append(i)
            i = i + 1

        dibujar_grafica_barras("Llegadas por hora", etiquetas, horas, ["#9BB8CD"])
        cambiar_estado("Gráfica de llegadas mostrada en la interfaz.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar vuelos.")


def accion_grafica_airlines():
    if len(lista_vuelos) > 0:
        nombres = []
        cantidades = []

        i = 0
        while i < len(lista_vuelos):
            avion = lista_vuelos[i]
            nombre_actual = avion.airline

            encontrado = False
            j = 0
            while j < len(nombres) and encontrado == False:
                if nombres[j] == nombre_actual:
                    encontrado = True
                else:
                    j = j + 1

            if encontrado == True:
                cantidades[j] = cantidades[j] + 1
            else:
                nombres.append(nombre_actual)
                cantidades.append(1)

            i = i + 1

        dibujar_grafica_barras("Vuelos por aerolínea", nombres, cantidades, ["#FFD6BA"])
        cambiar_estado("Gráfica de aerolíneas mostrada en la interfaz.")
    else:
        messagebox.showwarning("Error", "Primero debes cargar vuelos.")


def accion_grafica_tipo_vuelos():
    if len(lista_vuelos) > 0 and len(lista_airports) > 0:
        vuelos_schengen = 0
        vuelos_no_schengen = 0

        i = 0
        while i < len(lista_vuelos):
            avion = lista_vuelos[i]
            codigo_origen = avion.origin

            encontrado = False
            j = 0
            while j < len(lista_airports) and encontrado == False:
                if lista_airports[j].ICAOcode == codigo_origen:
                    encontrado = True

                    if lista_airports[j].Schengen == True:
                        vuelos_schengen = vuelos_schengen + 1
                    else:
                        vuelos_no_schengen = vuelos_no_schengen + 1
                else:
                    j = j + 1

            i = i + 1

        dibujar_grafica_barras(
            "Vuelos Schengen / No Schengen",
            ["Schengen", "No Schengen"],
            [vuelos_schengen, vuelos_no_schengen],
            ["#BEE3DB", "#F5B7B1"]
        )
        cambiar_estado("Gráfica de tipo de vuelos mostrada en la interfaz.")
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


# ---------------- INTERFAZ RETOCADA ----------------
# La ventana se separa en tres columnas:
# izquierda = cargar datos, añadir aviones, gráficas y mapas
# centro = pantallas de información y pantalla de gráficas
# derecha = puertas, salidas y ocupación por horas
# abajo = estado y botón salir

COLOR_FONDO = "#FAF3E0"
COLOR_PANEL = "#FFF8E7"
COLOR_TITULO = "#374151"
COLOR_DATOS = "#A8DADC"
COLOR_AVION = "#C7D9B7"
COLOR_VERSION4 = "#BDE0FE"
COLOR_GRAFICAS = "#F6E7A9"
COLOR_PUERTAS = "#F4B183"
COLOR_MAPAS = "#E5989B"
COLOR_MAPA_GRAFICO = "#CDB4DB"

# Tamaños de las pantallas centrales.
# La columna de texto es más pequeña y la de gráficos es más grande.
ANCHO_CANVAS_OCUPACION = 760
ALTO_CANVAS_OCUPACION = 520
ANCHO_CANVAS_GRAFICA = 540
ALTO_CANVAS_GRAFICA = 190


def titulo_seccion(frame, texto):
    tk.Label(
        frame,
        text=texto,
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TITULO
    ).pack(pady=(6, 4))


def boton(frame, texto, comando, color, ancho=30):
    tk.Button(
        frame,
        text=texto,
        command=comando,
        width=ancho,
        height=1,
        bg=color,
        font=("Arial", 10, "bold")
    ).pack(pady=3)


tk.Label(
    root,
    text="SISTEMA AEROPORTUARIO - VERSIÓN 4",
    font=("Arial", 20, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TITULO
).pack(pady=(8, 4))


frame_principal = tk.Frame(root, bg=COLOR_FONDO)
frame_principal.pack(padx=10, pady=4, fill=tk.BOTH, expand=True)


# ---------------- COLUMNA IZQUIERDA ----------------
frame_izquierda = tk.Frame(
    frame_principal,
    bg=COLOR_PANEL,
    bd=2,
    relief="groove",
    width=320,
    height=835
)
frame_izquierda.grid(row=0, column=0, padx=8, pady=5, sticky="n")
frame_izquierda.grid_propagate(False)


titulo_seccion(frame_izquierda, "--- CARGA DE DATOS ---")

boton(
    frame_izquierda,
    "Cargar aeropuertos y vuelos",
    accion_cargar,
    COLOR_DATOS,
    34
)

boton(
    frame_izquierda,
    "Cargar estructura LEBL",
    accion_cargar_LEBL,
    COLOR_DATOS,
    34
)

boton(
    frame_izquierda,
    "Cargar Departures",
    accion_cargar_departures,
    COLOR_DATOS,
    34
)


titulo_seccion(frame_izquierda, "--- NUEVO AVIÓN ---")

frame_formulario = tk.Frame(frame_izquierda, bg=COLOR_PANEL)
frame_formulario.pack(pady=2)

tk.Label(frame_formulario, text="ID avión:", bg=COLOR_PANEL, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=3, sticky="e")
entrada_id = tk.Entry(frame_formulario, width=21, font=("Arial", 10))
entrada_id.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Origen ICAO:", bg=COLOR_PANEL, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=3, sticky="e")
entrada_origen = tk.Entry(frame_formulario, width=21, font=("Arial", 10))
entrada_origen.grid(row=1, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Hora llegada:", bg=COLOR_PANEL, font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=3, sticky="e")
entrada_llegada = tk.Entry(frame_formulario, width=21, font=("Arial", 10))
entrada_llegada.grid(row=2, column=1, padx=5, pady=3)

tk.Label(frame_formulario, text="Aerolínea ICAO:", bg=COLOR_PANEL, font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=3, sticky="e")
entrada_aerolinea = tk.Entry(frame_formulario, width=21, font=("Arial", 10))
entrada_aerolinea.grid(row=3, column=1, padx=5, pady=3)


boton(
    frame_izquierda,
    "Añadir avión a la lista",
    accion_anadir_avion,
    COLOR_AVION,
    34
)

boton(
    frame_izquierda,
    "Añadir avión y asignar puerta",
    accion_anadir_y_asignar,
    COLOR_AVION,
    34
)


titulo_seccion(frame_izquierda, "--- GRÁFICAS ---")

boton(
    frame_izquierda,
    "Gráfica Aeropuertos",
    accion_grafica_airports,
    COLOR_GRAFICAS,
    34
)

boton(
    frame_izquierda,
    "Gráfica Llegadas",
    accion_grafica_llegadas,
    COLOR_GRAFICAS,
    34
)

boton(
    frame_izquierda,
    "Gráfica Aerolíneas",
    accion_grafica_airlines,
    COLOR_GRAFICAS,
    34
)

boton(
    frame_izquierda,
    "Gráfica Schengen Vuelos",
    accion_grafica_tipo_vuelos,
    COLOR_GRAFICAS,
    34
)


titulo_seccion(frame_izquierda, "--- MAPAS GOOGLE EARTH ---")

boton(
    frame_izquierda,
    "Mapa Aeropuertos Google Earth",
    accion_mapa_airports,
    COLOR_MAPAS,
    34
)

boton(
    frame_izquierda,
    "Mapa Vuelos Google Earth",
    accion_mapa_vuelos,
    COLOR_MAPAS,
    34
)


# ---------------- COLUMNA CENTRAL ----------------
frame_centro = tk.Frame(
    frame_principal,
    bg=COLOR_PANEL,
    bd=2,
    relief="groove",
    width=1160,
    height=855
)
frame_centro.grid(row=0, column=1, padx=8, pady=5, sticky="n")
frame_centro.grid_propagate(False)

# Dentro del centro hacemos dos columnas:
# izquierda = pantallas de texto más pequeñas
# derecha = pantallas de gráficos más grandes
frame_textos = tk.Frame(frame_centro, bg=COLOR_PANEL, width=345, height=840)
frame_textos.grid(row=0, column=0, padx=(8, 4), pady=5, sticky="n")
frame_textos.grid_propagate(False)

frame_graficas_centro = tk.Frame(frame_centro, bg=COLOR_PANEL, width=795, height=840)
frame_graficas_centro.grid(row=0, column=1, padx=(4, 8), pady=5, sticky="n")
frame_graficas_centro.grid_propagate(False)


# ---------- PANTALLAS DE TEXTO ----------
titulo_seccion(frame_textos, "Vuelos cargados / añadidos")

frame_texto_vuelos = tk.Frame(frame_textos, bg=COLOR_PANEL)
frame_texto_vuelos.pack(pady=3)

scroll_vuelos = tk.Scrollbar(frame_texto_vuelos, orient=tk.VERTICAL)

caja_vuelos = tk.Text(
    frame_texto_vuelos,
    width=39,
    height=13,
    font=("Arial", 10),
    yscrollcommand=scroll_vuelos.set
)

scroll_vuelos.config(command=caja_vuelos.yview)
caja_vuelos.grid(row=0, column=0)
scroll_vuelos.grid(row=0, column=1, sticky="ns")


titulo_seccion(frame_textos, "Ocupación de puertas")

frame_texto_ocupacion = tk.Frame(frame_textos, bg=COLOR_PANEL)
frame_texto_ocupacion.pack(pady=3)

scroll_ocupacion_texto = tk.Scrollbar(frame_texto_ocupacion, orient=tk.VERTICAL)

caja_ocupacion = tk.Text(
    frame_texto_ocupacion,
    width=39,
    height=18,
    font=("Arial", 10),
    yscrollcommand=scroll_ocupacion_texto.set
)

scroll_ocupacion_texto.config(command=caja_ocupacion.yview)
caja_ocupacion.grid(row=0, column=0)
scroll_ocupacion_texto.grid(row=0, column=1, sticky="ns")


# ---------- PANTALLAS DE GRÁFICOS ----------
titulo_seccion(frame_graficas_centro, "Gráfica de ocupación de puertas")

frame_canvas_ocupacion = tk.Frame(frame_graficas_centro, bg=COLOR_PANEL)
frame_canvas_ocupacion.pack(pady=3)

scroll_y_ocupacion = tk.Scrollbar(frame_canvas_ocupacion, orient=tk.VERTICAL)
scroll_x_ocupacion = tk.Scrollbar(frame_canvas_ocupacion, orient=tk.HORIZONTAL)

canvas_ocupacion_puertas = tk.Canvas(
    frame_canvas_ocupacion,
    width=ANCHO_CANVAS_OCUPACION,
    height=ALTO_CANVAS_OCUPACION,
    bg=COLOR_FONDO,
    highlightthickness=1,
    yscrollcommand=scroll_y_ocupacion.set,
    xscrollcommand=scroll_x_ocupacion.set
)

scroll_y_ocupacion.config(command=canvas_ocupacion_puertas.yview)
scroll_x_ocupacion.config(command=canvas_ocupacion_puertas.xview)

canvas_ocupacion_puertas.grid(row=0, column=0)
scroll_y_ocupacion.grid(row=0, column=1, sticky="ns")
scroll_x_ocupacion.grid(row=1, column=0, sticky="ew")

canvas_ocupacion_puertas.create_text(
    ANCHO_CANVAS_OCUPACION // 2,
    ALTO_CANVAS_OCUPACION // 2,
    text="Aquí aparecerá la gráfica de ocupación de puertas T1 o T2.",
    font=("Arial", 10, "bold"),
    fill=COLOR_TITULO
)


titulo_seccion(frame_graficas_centro, "Pantalla de gráficas")

frame_recuadro_grafica = tk.Frame(
    frame_graficas_centro,
    bg="black",
    padx=2,
    pady=2
)
frame_recuadro_grafica.pack(pady=3)

canvas_grafica = tk.Canvas(
    frame_recuadro_grafica,
    width=ANCHO_CANVAS_GRAFICA,
    height=ALTO_CANVAS_GRAFICA,
    bg=COLOR_FONDO,
    highlightthickness=0
)
canvas_grafica.pack()


# ---------------- COLUMNA DERECHA ----------------
frame_derecha = tk.Frame(
    frame_principal,
    bg=COLOR_PANEL,
    bd=2,
    relief="groove",
    width=320,
    height=835
)
frame_derecha.grid(row=0, column=2, padx=8, pady=5, sticky="n")
frame_derecha.grid_propagate(False)


titulo_seccion(frame_derecha, "--- GESTIÓN DE PUERTAS ---")

boton(
    frame_derecha,
    "Asignar puertas a todos los vuelos",
    accion_asignar_todos,
    COLOR_PUERTAS,
    34
)

boton(
    frame_derecha,
    "Ver ocupación T1",
    accion_ver_T1,
    COLOR_PUERTAS,
    34
)

boton(
    frame_derecha,
    "Ver ocupación T2",
    accion_ver_T2,
    COLOR_PUERTAS,
    34
)


titulo_seccion(frame_derecha, "--- SALIDAS Y HORAS ---")

boton(
    frame_derecha,
    "Asignar puertas por horas",
    accion_asignar_puertas_horas,
    COLOR_PUERTAS,
    34
)

tk.Label(
    frame_derecha,
    text="Mueve la línea para cambiar la hora",
    font=("Arial", 10, "bold"),
    bg=COLOR_PANEL,
    fg=COLOR_TITULO
).pack(pady=(10, 2))

linea_horas = tk.Scale(
    frame_derecha,
    from_=0,
    to=23,
    orient="horizontal",
    length=260,
    command=actualizar_ocupacion_hora,
    bg=COLOR_PANEL,
    highlightthickness=0
)
linea_horas.pack(pady=2)

etiqueta_hora_actual = tk.Label(
    frame_derecha,
    text="Hora seleccionada: 0:00",
    font=("Arial", 10, "bold"),
    bg=COLOR_PANEL,
    fg=COLOR_TITULO
)
etiqueta_hora_actual.pack(pady=4)


titulo_seccion(frame_derecha, "--- MAPA GRÁFICO DE PUERTAS ---")

boton(
    frame_derecha,
    "Ver gráfica de puertas T1",
    accion_grafica_puertas_T1,
    COLOR_MAPA_GRAFICO,
    34
)

boton(
    frame_derecha,
    "Ver gráfica de puertas T2",
    accion_grafica_puertas_T2,
    COLOR_MAPA_GRAFICO,
    34
)


# ---------------- PARTE INFERIOR ----------------
frame_inferior = tk.Frame(root, bg=COLOR_FONDO)
frame_inferior.pack(fill=tk.X, padx=12, pady=(4, 8))

etiqueta_estado = tk.Label(
    frame_inferior,
    text="Estado: esperando cargar archivos.",
    bg=COLOR_FONDO,
    fg=COLOR_TITULO,
    font=("Arial", 10, "bold")
)
etiqueta_estado.pack(side=tk.LEFT, padx=10)

tk.Button(
    frame_inferior,
    text="SALIR",
    command=root.destroy,
    fg="red",
    width=22,
    height=1,
    font=("Arial", 10, "bold")
).pack(side=tk.RIGHT, padx=10)


actualizar_pantalla_vuelos()
actualizar_ocupacion_hora(0)

root.mainloop()
