from Airport import IsSchengenAirport


class Gate:
    def __init__(self, name):
        self.name = name  # Nombre de la puerta (ej: T1AG01)
        self.occupied = False  # Al empezar, la puerta siempre está libre (False)
        self.aircraft_id = ""  # Matrícula del avión que aparque aquí


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

    # 2. Comprobamos si el avión viene de un aeropuerto Schengen (control de pasaportes)
    is_schengen = IsSchengenAirport(aircraft.origin)
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
    # Tres bucles anidados para resetear todo el aeropuerto y dejarlo vacío (a cero)
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
