from Airport import IsSchengenAirport


class Gate:
    def __init__(self, name,distancia_a_control=100):
        self.name = name  # Nombre de la puerta (ej: T1AG01)
        self.occupied = False  # Al empezar, la puerta siempre está libre (False)
        self.aircraft_id = ""  # Matrícula del avión que aparque aquí
        self.distancia_a_control=distancia_a_control   #distancia en metros a la zona central


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name  # Nombre de la zona (A, B, C...)
        self.type = area_type  # Si es zona Schengen o No-Schengen
        self.gates = []  # Lista vacía para rellenarla con objetos de tipo Gate


class Terminal:
    def __init__(self, name):
        self.name = name  # Nombre de la terminal (T1 o T2)
        self.boarding_areas = []  # Lista para guardar sus zonas de embarque
        self.airlines = []  # Lista con los códigos de las aerolíneas que operan aquí


# Guardamos una referencia a la clase Terminal
terminal = Terminal


class BarcelonaAP:
    def __init__(self, code):
        self.code = code  # Código del aeropuerto (LEBL)
        self.terminals = []  # Lista para guardar los objetos Terminal

def SetGates(area, init_gate, end_gate, prefix):
    # Control de seguridad: que el número final no sea menor al de inicio
    if end_gate <= init_gate:
        return -1

    area.gates = []  # Limpiamos las puertas que pudiera tener el área
    i = init_gate
    # Bucle para ir sumando números y fabricar las puertas una a una
    while i <= end_gate:
        area.gates.append(Gate(prefix + str(i)))  # Combinamos el texto con el número y creamos la Gate
        i = i + 1
    return 0


def LoadAirlines(terminal, terminal_name):
    # Montamos el nombre del archivo según la terminal (ej: T1_Airlines.txt)
    filename = terminal_name + "_Airlines.txt"

    try:
        f = open(filename, "r")  # Intentamos abrir el archivo
    except:
        return -1  # Si no existe, devolvemos error -1

    terminal.airlines = []  # Vaciamos la lista de aerolíneas de la terminal
    linea = f.readline()  # Leemos la primera línea para arrancar

    # El bucle sigue leyendo líneas una a una hasta que el archivo se quede vacío ("")
    while linea != "":
        parts = linea.strip().split("\t")  # Limpiamos espacios y cortamos por el tabulador
        if len(parts) == 2:
            terminal.airlines.append(parts[1])  # Si la línea es correcta, guardamos la aerolínea

        linea = f.readline()  # Avanzamos leyendo la siguiente línea antes de repetir el bucle

    f.close()  # Cerramos el archivo al terminar
    return 0


def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")  # Abrimos el archivo maestro del aeropuerto (LEBL.txt)
    except:
        return -1

    # Leemos la primera línea para sacar el código principal
    primera_linea = f.readline()
    if primera_linea == "":
        f.close()
        return -1

    first_line_parts = primera_linea.split()
    if len(first_line_parts) < 1:
        f.close()
        return -1

    # Creamos el objeto principal del aeropuerto con el código leído
    bcn = BarcelonaAP(first_line_parts[0])
    current_terminal = ""

    # Leemos la siguiente línea para empezar el bucle principal
    linea = f.readline()

    # Bucle para procesar el archivo entero línea a línea usando readline()
    while linea != "":
        parts = linea.split()  # Troceamos la línea por palabras

        # Si la línea define una terminal, creamos el objeto Terminal y cargamos sus aerolíneas
        if len(parts) > 0 and parts[0] == "Terminal":
            current_terminal = Terminal(parts[1])
            LoadAirlines(current_terminal, parts[1])
            bcn.terminals.append(current_terminal)  # Añadimos la terminal al aeropuerto

        # Si define un área, creamos la zona y llamamos a SetGates para inyectarle sus puertas
        elif len(parts) >= 7 and parts[0] == "Area" and current_terminal != "":
            area = BoardingArea(parts[1], parts[2])
            prefix = current_terminal.name + area.name + "G"  # Prefijo automático (ej: T1AG)
            SetGates(area, int(parts[4]), int(parts[6]), prefix)
            current_terminal.boarding_areas.append(area)  # Añadimos el área a la terminal actual

        # Leemos la siguiente línea para que el while avance y no se quede infinito
        linea = f.readline()

    f.close()  # Cerramos el archivo
    return bcn  # Devolvemos el aeropuerto entero ya montado


# Duplicamos la función con un alias por si se usa el nombre en plural en otra parte
LoadAirportsStructure = LoadAirportStructure



def GateOccupancy(bcn):
    occupancy = []  # Aquí guardaremos la matriz con la foto del estado de las puertas
    t = 0

    # Bucle 1: Recorremos cada Terminal
    while t < len(bcn.terminals):
        term = bcn.terminals[t]
        a = 0

        # Bucle 2: Entramos en cada Área de la terminal
        while a < len(term.boarding_areas):
            area = term.boarding_areas[a]
            g = 0

            # Bucle 3: Revisamos cada Puerta física del área
            while g < len(area.gates):
                gate = area.gates[g]
                # Guardamos los 5 datos clave de la puerta en una sublista
                occupancy.append([term.name, area.name, gate.name, gate.occupied, gate.aircraft_id])
                g = g + 1

            a = a + 1

        t = t + 1

    return occupancy  # Devolvemos la lista gigante con todos los datos ordenados


def IsAirlineInTerminal(terminal, name):
    # Si no nos pasan nombre o la terminal no tiene aerolíneas asociadas, devolvemos False
    if name == "" or len(terminal.airlines) == 0:
        return False

    i = 0
    # Bucle para comprobar si el nombre de la aerolínea está en la lista de la terminal
    while i < len(terminal.airlines):
        if terminal.airlines[i] == name:
            return True  # ¡Encontrada! Opera en esta terminal
        i = i + 1

    return False  # Si termina el bucle y no la ve, es que no opera aquí


def SearchTerminal(bcn, name):
    t = 0
    # Recorremos las terminales buscando cuál tiene contratada a esta aerolínea
    while t < len(bcn.terminals):
        if IsAirlineInTerminal(bcn.terminals[t], name) == True:
            return bcn.terminals[t].name  # Devuelve "T1" o "T2" si la encuentra
        t = t + 1

    return ""  # Si ninguna terminal la tiene, devolvemos un texto vacío


def AssignGate(bcn, aircraft):
    # 1. Buscamos en qué terminal tiene que operar el avión según su aerolínea
    terminal_name = SearchTerminal(bcn, aircraft.airline)
    if terminal_name == "":
        return -1  # Error -1: La aerolínea no tiene terminal asignada en este aeropuerto

    # 2. Comprobamos si el avión viene de un aeropuerto Schengen.
    # Si es un vuelo nocturno de salida, no tiene origen, así que usamos el destino.
    codigo_tipo = aircraft.origin
    if codigo_tipo == "" and aircraft.destination != "":
        codigo_tipo = aircraft.destination

    is_schengen = IsSchengenAirport(codigo_tipo)
    t = 0

    # 3. Empezamos a buscar una puerta libre que cumpla los requisitos
    while t < len(bcn.terminals):
        term = bcn.terminals[t]

        # Solo buscamos dentro de la terminal que le corresponde al avión
        if term.name == terminal_name:
            a = 0
            while a < len(term.boarding_areas):
                area = term.boarding_areas[a]

                # Filtramos: el tipo de área (Schengen/No-Schengen) debe coincidir con el tipo de vuelo
                if (is_schengen == True and area.type == "Schengen") or (
                        is_schengen == False and area.type == "non-Schengen"):
                    g = 0
                    while g < len(area.gates):
                        gate = area.gates[g]

                        # Si encontramos una puerta vacía, metemos al avión inmediatamente
                        if gate.occupied == False:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.aircraft_id
                            return 0  # Éxito: puerta asignada correctamente
                        g = g + 1

                a = a + 1

        t = t + 1

    return -2  # Error -2: No quedan puertas libres compatibles para este tipo de vuelo


def ResetGates(bcn):
    t = 0
    # Tres bucles anidados para resetear
    while t < len(bcn.terminals):
        a = 0
        while a < len(bcn.terminals[t].boarding_areas):
            g = 0
            while g < len(bcn.terminals[t].boarding_areas[a].gates):
                gate = bcn.terminals[t].boarding_areas[a].gates[g]
                gate.occupied = False  # Liberamos la puerta
                gate.aircraft_id = ""  # Quitamos el avión
                g = g + 1
            a = a + 1
        t = t + 1
    return 0


def AssignNightGates(bcn, aircrafts):
    # Si la lista está vacía, devolvemos un código de error -1
    if len(aircrafts) == 0:
        return -1

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]

        # Verificamos la condición: solo vuelos de salida (llegada vacía)
        if avion.arrival_time == "" and avion.departure_time != "":
            # Usamos tu función AssignGate para asignarle puerta
            AssignGate(bcn, avion)

        # Si no cumple la condición, el bucle simplemente pasa al siguiente avión
        i = i + 1

    return 0


def FreeGate(bcn, id):
    # Usamos tu misma estructura de 3 bucles while anidados para recorrer todo el aeropuerto
    encontrado = False

    t = 0
    while t < len(bcn.terminals) and encontrado == False:
        term = bcn.terminals[t]

        a = 0
        while a < len(term.boarding_areas) and encontrado == False:
            area = term.boarding_areas[a]

            g = 0
            while g < len(area.gates) and encontrado == False:
                gate = area.gates[g]

                # Si la puerta está ocupada y la matrícula coincide con el id que buscamos
                if gate.occupied == True and gate.aircraft_id == id:
                    gate.occupied = False  # Liberamos la puerta
                    gate.aircraft_id = ""  # Borramos el id del avión
                    encontrado = True  # Activamos la bandera para salir de los bucles

                g = g + 1
            a = a + 1
        t = t + 1

    # Si se encontró y se liberó devolvemos 0, si no se encontró devolvemos un error -1
    if encontrado == True:
        return 0
    else:
        return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    # Si no hay aeropuerto o la lista de aviones está vacía, salimos con error
    if bcn == "" or bcn == -1 or len(aircrafts) == 0:
        return -1

    # Descomponemos la hora que nos pasan (ej: "12:00" -> nos quedamos con "12")
    partes_tiempo = time.split(":")
    hora_objetivo = partes_tiempo[0]

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]

        # Si el avión tiene hora de salida programada
        if avion.departure_time != "":
            partes_despegue = avion.departure_time.split(":")
            hora_despegue = partes_despegue[0]

            # Si despega en esta hora, liberamos su puerta con tu función FreeGate
            if hora_despegue == hora_objetivo:
                FreeGate(bcn, avion.aircraft_id)

        i = i + 1

    aviones_rechazados = 0
    j = 0
    while j < len(aircrafts):
        avion = aircrafts[j]

        # Si el avión tiene hora de llegada programada
        if avion.arrival_time != "":
            partes_llegada = avion.arrival_time.split(":")
            hora_llegada = partes_llegada[0]

            # Si aterriza en esta hora, intentamos buscarle sitio
            if hora_llegada == hora_objetivo:
                resultado = AssignGateOptimized(bcn, avion)

                # Si tu función AssignGate devuelve -1 o -2, es que no hay sitio compatible
                if resultado < 0:
                    aviones_rechazados = aviones_rechazados + 1

        j = j + 1

    # Devolvemos el número de aviones que no han cabido en esta hora
    return aviones_rechazados


def AssignGatesByHour(bcn, arrivals, departures):
    # Esta función prepara la ocupación de puertas para cada hora del día.
    # Devuelve una lista con 24 posiciones: una posición por cada hora.

    if bcn == "" or bcn == -1:
        return []

    if len(arrivals) == 0 or len(departures) == 0:
        return []

    # Juntamos llegadas y salidas para que un mismo avión tenga llegada y salida.
    from Aircraft import MergeMovements
    aircrafts = MergeMovements(arrivals, departures)

    if len(aircrafts) == 0:
        return []

    # Empezamos con todas las puertas libres y colocamos los aviones nocturnos.
    ResetGates(bcn)
    AssignNightGates(bcn, aircrafts)

    ocupacion_horas = []

    h = 0
    while h < 24:
        if h < 10:
            hora_texto = "0" + str(h) + ":00"
        else:
            hora_texto = str(h) + ":00"

        rechazados = AssignGatesAtTime(bcn, aircrafts, hora_texto)
        foto = GateOccupancy(bcn)

        lineas = []
        lineas.append("Hora: " + hora_texto)
        lineas.append("Vuelos rechazados: " + str(rechazados))
        lineas.append("")

        # Resumen por terminal.
        t = 0
        while t < len(bcn.terminals):
            nombre_terminal = bcn.terminals[t].name

            total = 0
            ocupadas = 0
            libres = 0

            i = 0
            while i < len(foto):
                if foto[i][0] == nombre_terminal:
                    total = total + 1

                    if foto[i][3] == True:
                        ocupadas = ocupadas + 1
                    else:
                        libres = libres + 1

                i = i + 1

            lineas.append(nombre_terminal + " | TOTAL: " + str(total) +
                          " | OCUPADAS: " + str(ocupadas) +
                          " | LIBRES: " + str(libres))
            t = t + 1

        lineas.append("")
        lineas.append("PUERTAS OCUPADAS:")

        hay_ocupadas = False
        i = 0
        while i < len(foto):
            terminal = foto[i][0]
            area = foto[i][1]
            gate = foto[i][2]
            ocupada = foto[i][3]
            avion = foto[i][4]

            if ocupada == True:
                hay_ocupadas = True
                lineas.append(terminal + " | " + area + " | " + gate + " | " + avion)

            i = i + 1

        if hay_ocupadas == False:
            lineas.append("No hay puertas ocupadas.")

        ocupacion_horas.append(lineas)
        h = h + 1

    return ocupacion_horas


import matplotlib.pyplot as plt

def PlotDayOccupancy(bcn, aircrafts):
    if bcn == "" or bcn == -1 or len(aircrafts) == 0:
        return -1

    # 1. Preparamos el aeropuerto para empezar desde cero
    ResetGates(bcn)
    AssignNightGates(bcn, aircrafts)

    # Creamos las listas para el eje X y para los aviones rechazados
    lista_horas = []
    lista_rechazados = []

    # Creamos listas dinámicas para guardar la ocupación de cada terminal de tu bcn
    nombres_terminales = []
    datos_ocupacion_terminales = []  # Será una lista de listas

    t = 0
    while t < len(bcn.terminals):
        nombres_terminales.append(bcn.terminals[t].name)
        datos_ocupacion_terminales.append([])  # Guardará los 24 datos de esa terminal
        t = t + 1

    # 2. Simulamos el día hora a hora (de 0 a 23)
    h = 0
    while h < 24:
        # Fabricamos el string de la hora de forma manual y limpia
        if h < 10:
            hora_actual_texto = "0" + str(h) + ":00"
        else:
            hora_actual_texto = str(h) + ":00"

        lista_horas.append(hora_actual_texto)

        # Ejecutamos los movimientos de esta hora y guardamos los rechazados
        rechazados_en_esta_hora = AssignGatesAtTime(bcn, aircrafts, hora_actual_texto)
        lista_rechazados.append(rechazados_en_esta_hora)

        # Hacemos un recuento de cómo ha quedado el aeropuerto tras los movimientos
        foto_ocupacion = GateOccupancy(bcn)

        # Contamos cuántas puertas ocupadas hay en cada terminal
        idx_t = 0
        while idx_t < len(nombres_terminales):
            term_actual = nombres_terminales[idx_t]
            puertas_ocupadas = 0

            o = 0
            while o < len(foto_ocupacion):
                # Si la puerta pertenece a esta terminal y está ocupada (True)
                if foto_ocupacion[o][0] == term_actual and foto_ocupacion[o][3] == True:
                    puertas_ocupadas = puertas_ocupadas + 1
                o = o + 1

            # Guardamos el total de ocupadas de esta hora en la lista de la terminal
            datos_ocupacion_terminales[idx_t].append(puertas_ocupadas)
            idx_t = idx_t + 1

        h = h + 1

    # 3. Construimos el gráfico interactivo
    plt.figure(figsize=(12, 6))

    # Dibujamos las líneas de ocupación para cada terminal usando un bucle while
    idx_t = 0
    while idx_t < len(nombres_terminales):
        plt.plot(lista_horas, datos_ocupacion_terminales[idx_t], marker='o', linewidth=2, label="Ocupación " + nombres_terminales[idx_t])
        idx_t = idx_t + 1

    # Dibujamos las barras rojas para los aviones rechazados (sin puerta)
    plt.bar(lista_horas, lista_rechazados, color='#F5B7B1', alpha=0.7, label='Vuelos rechazados (Aero. Lleno)')

    # Ajustes estéticos para que combine con tu interfaz original
    plt.title("Evolución Temporal de la Ocupación en Barcelona (LEBL)")
    plt.xlabel("Hora del Día")
    plt.ylabel("Número de Puertas / Aviones")
    plt.xticks(rotation=45)
    plt.gcf().set_facecolor("#FAF3E0")
    plt.gca().set_facecolor("#FAF3E0")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    return 0

#EXTRAS
def AssignGateOptimized(bcn, aircraft):
    # 1. Buscamos en qué terminal tiene que operar el avión según su aerolínea
    terminal_name = SearchTerminal(bcn, aircraft.airline)
    if terminal_name == "":
        return -1  # Error -1: La aerolínea no tiene terminal asignada

    # 2. Comprobamos si el avión viene de un aeropuerto Schengen
    codigo_tipo = aircraft.origin
    if codigo_tipo == "" and aircraft.destination != "":
        codigo_tipo = aircraft.destination

    is_schengen = IsSchengenAirport(codigo_tipo)

    # --- AQUÍ EMPIEZA LA OPTIMIZACIÓN ---
    # En lugar de quedarnos con la primera que veamos, vamos a buscar TODAS las compatibles
    # y elegiremos la que tenga menor distancia.
    puerta_optima = None
    distancia_minima = 999999  # Empezamos con un número muy alto para poder ir rebajándolo

    t = 0
    while t < len(bcn.terminals):
        term = bcn.terminals[t]

        if term.name == terminal_name:
            a = 0
            while a < len(term.boarding_areas):
                area = term.boarding_areas[a]

                # Filtramos por tipo de vuelo (Schengen o No-Schengen)
                if (is_schengen == True and area.type == "Schengen") or (
                        is_schengen == False and area.type == "non-Schengen"):

                    g = 0
                    while g < len(area.gates):
                        gate = area.gates[g]

                        # Si la puerta está libre, comprobamos si es la más cercana que hemos visto hasta ahora
                        if gate.occupied == False:
                            if gate.distancia_a_control < distancia_minima:
                                distancia_minima = gate.distancia_a_control
                                puerta_optima = gate  # Guardamos la referencia temporalmente

                        g = g + 1
                a = a + 1
        t = t + 1

    # 3. Una vez revisadas todas las opciones, si encontramos una puerta óptima, la asignamos
    if puerta_optima is not None:
        puerta_optima.occupied = True
        puerta_optima.aircraft_id = aircraft.aircraft_id
        return 0  # Éxito

    return -2  # Error -2: No quedan puertas libres compatibles



import os


def MapGatesToGoogleEarth(bcn, filename="lebl_gates_live.kml"):

    # --- 1. CÁLCULO DE ESTADÍSTICAS EN TIEMPO REAL ---
    t1_totales = 0
    t1_ocupadas = 0
    t2_totales = 0
    t2_ocupadas = 0

    # Recorremos los objetos para hacer las matemáticas del aeropuerto
    for t in bcn.terminals:
        es_t1 = "T1" in str(t.name).upper()
        for area in t.boarding_areas:
            for gate in area.gates:
                if es_t1:
                    t1_totales += 1
                    if gate.occupied:
                        t1_ocupadas += 1
                else:
                    t2_totales += 1
                    if gate.occupied:
                        t2_ocupadas += 1

    # Calculamos los porcentajes finales de ocupación
    porcentaje_t1 = (t1_ocupadas / t1_totales * 100) if t1_totales > 0 else 0
    porcentaje_t2 = (t2_ocupadas / t2_totales * 100) if t2_totales > 0 else 0

    # Coordenadas base en la silueta para el centro de cada área
    COORDENADAS_AREAS = {
        'A': (41.2894, 2.0728), 'B': (41.2877, 2.0662), 'C': (41.2870, 2.0706),
        'D': (41.2919, 2.0763), 'E': (41.2844, 2.0725),
        'M': (41.3037, 2.0736), 'R': (41.3020, 2.0765), 'S': (41.3000, 2.0795)
    }

    f = open(filename, "w", encoding="utf-8")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    # --- 2. PANEL DE CONTROL NATIVO EN HTML ---
    f.write('  <name>LEBL - Control de Áreas Profesional</name>\n')
    f.write('  <open>1</open>\n')  # Hace que el árbol de carpetas izquierdo se expanda solo
    f.write('  <description><![CDATA[\n')
    f.write(
        '    <div style="background-color: #1c1d22; color: #ffffff; padding: 15px; border-radius: 10px; font-family: Segoe UI, Arial, sans-serif; width: 280px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">\n')
    f.write(
        '      <h3 style="color: #00e676; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #2e3035; padding-bottom: 6px; font-size: 16px; letter-spacing: 1px;">📊 RADAR LEBL LIVE</h3>\n')

    # Barra de progreso para la Terminal 1
    f.write(
        f'      <p style="margin: 6px 0; font-size: 13px;"><b>Terminal 1:</b> <span style="color: #ffca28; float: right;">{porcentaje_t1:.1f}%</span></p>\n')
    f.write(
        '      <div style="background: #2e3035; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 12px;">\n')
    f.write(f'        <div style="background: #ffca28; height: 100%; width: {int(porcentaje_t1)}%;"></div>\n')
    f.write('      </div>\n')

    # Barra de progreso para la Terminal 2
    f.write(
        f'      <p style="margin: 6px 0; font-size: 13px;"><b>Terminal 2:</b> <span style="color: #00e676; float: right;">{porcentaje_t2:.1f}%</span></p>\n')
    f.write(
        '      <div style="background: #2e3035; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 12px;">\n')
    f.write(f'        <div style="background: #00e676; height: 100%; width: {int(porcentaje_t2)}%;"></div>\n')
    f.write('      </div>\n')

    f.write(
        '      <p style="font-size: 11px; color: #aaaaaa; margin-top: 10px; line-height: 1.4; border-top: 1px solid #2e3035; padding-top: 8px;">• Datos calculados automáticamente en Python.<br/>• Haz clic en los iconos blancos para desplegar las puertas de esa zona.</p>\n')
    f.write('    </div>\n')
    f.write('  ]]></description>\n')

    # --- 3. ESTILOS DE CHINCHETAS Y PUERTAS ---
    # Estilo de chincheta blanca limpia para los centros de las áreas
    f.write('  <Style id="centro_area">\n')
    f.write('    <IconStyle>\n')
    f.write('      <scale>1.4</scale>\n')
    f.write('      <Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>\n')
    f.write('    </IconStyle>\n')
    f.write('    <LabelStyle><scale>1.1</scale></LabelStyle>\n')  # Hace que el texto del nombre flote en el mapa
    f.write('  </Style>\n')

    # Estilos circulares para las puertas (Verde = Libre, Rojo = Ocupado)
    f.write(
        '  <Style id="libre"><IconStyle><color>ff00ff00</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle></Style>\n')
    f.write(
        '  <Style id="ocupado"><IconStyle><color>ff0000ff</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle></Style>\n')

    # --- 4. CONSTRUCCIÓN DEL MAPA (Efecto Abanico Puro) ---
    i = 0
    while i < len(bcn.terminals):
        t = bcn.terminals[i]
        es_t1 = "T1" in str(t.name).upper()

        f.write('  <Folder>\n')
        f.write(f'    <name>Terminal {t.name}</name>\n')

        j = 0
        while j < len(t.boarding_areas):
            area = t.boarding_areas[j]
            nombre_area = str(area.name).upper().strip()

            if nombre_area in COORDENADAS_AREAS:
                lat_area, lon_area = COORDENADAS_AREAS[nombre_area]
            else:
                lat_area, lon_area = (41.2882, 2.0705) if es_t1 else (41.3015, 2.0775)

            f.write('    <Folder>\n')
            f.write(f'      <name>Área {nombre_area}</name>\n')

            # Marcador principal Blanco con el nombre grabado en la silueta
            f.write('      <Placemark>\n')
            f.write(f'        <name>ÁREA {nombre_area}</name>\n')
            f.write(
                f'        <description><![CDATA[<h3>Área de Embarque {nombre_area}</h3><p>Haz clic en este punto físico para desplegar todas sus puertas.</p>]]></description>\n')
            f.write('        <styleUrl>#centro_area</styleUrl>\n')
            f.write('        <Point>\n')
            f.write(f'          <coordinates>{lon_area},{lat_area},0</coordinates>\n')
            f.write('        </Point>\n')
            f.write('      </Placemark>\n')

            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                nombre_real = str(gate.name).strip().upper()

                # EFECTO ABANICO: Forzamos a que todas las puertas mueran exactamente en el mismo punto
                lat_gate = lat_area
                lon_gate = lon_area

                # Comprobación de aviones y colores (Verde / Rojo)
                if gate.occupied:
                    estilo = "#ocupado"
                    estado_txt = "<font color='red'><b>OCUPADA</b></font>"
                    info_avion = f"<b>AVIÓN:</b> {gate.aircraft_id}<br/>"
                else:
                    estilo = "#libre"
                    estado_txt = "<font color='green'><b>LIBRE</b></font>"
                    info_avion = ""

                desc_html = f"<b>PUERTA:</b> {nombre_real}<br/><b>ESTADO:</b> {estado_txt}<br/>{info_avion}<b>UBICACIÓN:</b> Terminal {t.name} - Zona {nombre_area}"

                f.write('        <Placemark>\n')
                f.write(f'          <name>{nombre_real}</name>\n')
                f.write(f'          <description><![CDATA[{desc_html}]]></description>\n')
                f.write(f'          <styleUrl>{estilo}</styleUrl>\n')
                f.write('          <Point>\n')
                f.write(f'            <coordinates>{lon_gate},{lat_gate},0</coordinates>\n')
                f.write('          </Point>\n')
                f.write('        </Placemark>\n')

                k += 1

            f.write('    </Folder>\n')
            j += 1

        f.write('  </Folder>\n')
        i += 1

    f.write('  </Document>\n</kml>\n')
    f.close()

    os.startfile(filename)
    return True

import time


def ManejarRadarTiempo(segundos_espera=5):
    from Aircraft import LoadArrivals  # Importación local para evitar conflictos

    print(
        f"\n[⏱️] Motor de tiempo iniciado. Escaneando cambios cada {segundos_espera}s..."
    )
    print(
        "[💡] Para detener el programa, presiona Ctrl+C aquí en la consola.\n"
    )

    try:
        while True:
            # Pausa de los segundos configurados
            time.sleep(segundos_espera)

            # Volvemos a leer y procesar tus archivos en cada ciclo
            bcn_live = LoadAirportStructure("LEBL.txt")
            aircrafts_live = LoadArrivals("Arrivals.txt")

            if bcn_live != -1:
                j = 0
                while j < len(aircrafts_live):
                    AssignGate(bcn_live, aircrafts_live[j])
                    j += 1

                # Sobrescribimos el KML. Google Earth lo leerá solo en segundo plano.
                MapGatesToGoogleEarth(bcn_live, filename="lebl_gates_live.kml")
                print("• [Radar Sync] Archivos escaneados y mapa actualizado.")
            else:
                print("[!] Error leyendo 'LEBL.txt' en este ciclo.")

    except KeyboardInterrupt:
        print("\n[INFO] El motor de tiempo del radar se ha apagado de forma segura.")

if __name__ == "__main__":
    from Aircraft import LoadArrivals

    # Cargamos la estructura del aeropuerto y la lista de vuelos que van a llegar
    bcn = LoadAirportStructure("LEBL.txt")
    aircrafts = LoadArrivals("Arrivals.txt")

    # Si el aeropuerto se cargó bien, empezamos el proceso de asignación
    if bcn != -1:
        i = 0
        assigned = 0
        # Vamos avión por avión intentando buscarle sitio en Barcelona
        while i < len(aircrafts):
            if AssignGate(bcn, aircrafts[i]) == 0:
                assigned = assigned + 1  # Sumamos 1 si se pudo aparcar con éxito
            i = i + 1

        # Imprimimos los resultados finales en la consola
        print("Puertas asignadas:", assigned)
        print("Total puertas:", len(GateOccupancy(bcn)))

        ManejarRadarTiempo(segundos_espera=5)
