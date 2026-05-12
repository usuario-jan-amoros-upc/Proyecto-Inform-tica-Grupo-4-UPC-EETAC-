# Importamos la función que nos dice si un aeropuerto pertenece a Schengen.
from Airport import IsSchengenAirport

# Importamos la función que carga los vuelos de llegada desde Arrivals.txt.
from Aircraft import LoadArrivals


# Definimos la clase Gate, que representa una puerta del aeropuerto.
class Gate:
    # Constructor de Gate: recibe el nombre de la puerta.
    def __init__(self, name):
        # Guardamos el nombre de la puerta, por ejemplo T1BAAG1.
        self.name = name
        # Indicamos si la puerta está ocupada; al principio siempre está libre.
        self.occupied = False
        # Guardamos el identificador del avión que ocupa la puerta; al principio está vacío.
        self.aircraft_id = ""


# Definimos la clase BoardingArea, que representa una zona de embarque.
class BoardingArea:
    # Constructor de BoardingArea: recibe el nombre de la zona y su tipo.
    def __init__(self, name, area_type):
        # Guardamos el nombre de la zona, por ejemplo T1BAA.
        self.name = name
        # Guardamos si la zona es Schengen o non-Schengen.
        self.area_type = area_type
        # Creamos la lista de puertas de la zona; cada elemento será de tipo Gate.
        self.gates = []


# Definimos la clase Terminal, que representa una terminal del aeropuerto.
class Terminal:
    # Constructor de Terminal: recibe el nombre de la terminal.
    def __init__(self, name):
        # Guardamos el nombre de la terminal, por ejemplo T1 o T2.
        self.name = name
        # Creamos la lista de zonas de embarque; cada elemento será de tipo BoardingArea.
        self.boardingAreas = []
        # Creamos la lista de aerolíneas que trabajan en esta terminal.
        self.airlines = []


# Definimos la clase BarcelonaAP, que representa el aeropuerto de Barcelona.
class BarcelonaAP:
    # Constructor de BarcelonaAP: recibe el código del aeropuerto.
    def __init__(self, code):
        # Guardamos el código del aeropuerto, por ejemplo LEBL.
        self.code = code
        # Creamos la lista de terminales; cada elemento será de tipo Terminal.
        self.terminals = []


# Esta función crea las puertas de una zona de embarque.
def SetGates(area, init_gate, end_gate, prefix):
    # Si la puerta final no es mayor que la inicial, devolvemos error.
    if end_gate <= init_gate:
        # Código de error.
        return -1

    # Borramos cualquier lista anterior de puertas de esta zona.
    area.gates = []
    # Empezamos a crear puertas desde el número inicial.
    num = init_gate
    # Repetimos hasta llegar al número final de puerta.
    while num <= end_gate:
        # Construimos el nombre de la puerta usando el prefijo y el número.
        gate_name = prefix + str(num)
        # Creamos un objeto Gate con ese nombre.
        gate = Gate(gate_name)
        # Añadimos la puerta a la lista de puertas de la zona.
        area.gates.append(gate)
        # Pasamos al siguiente número de puerta.
        num = num + 1

    # Devolvemos 0 para indicar que ha funcionado correctamente.
    return 0


# Esta función carga las aerolíneas que pertenecen a una terminal.
def LoadAirlines(terminal, t_name):
    # Construimos el nombre del archivo, por ejemplo T1_Airlines.txt.
    filename = t_name + "_Airlines.txt"

    # Intentamos abrir el archivo de aerolíneas.
    try:
        # Abrimos el archivo en modo lectura.
        f = open(filename, "r")
        # Leemos todas las líneas del archivo.
        lineas = f.readlines()
        # Cerramos el archivo.
        f.close()
    # Si hay error al abrir el archivo, entramos aquí.
    except:
        # Mostramos por consola que no se ha podido abrir.
        print("No se ha podido abrir", filename)
        # Devolvemos error.
        return -1

    # Vaciamos la lista de aerolíneas de la terminal.
    terminal.airlines = []

    # Empezamos a recorrer las líneas desde la primera.
    i = 0
    # Recorremos todas las líneas del archivo.
    while i < len(lineas):
        # Separamos la línea por espacios o tabuladores.
        parts = lineas[i].split()
        # Comprobamos que la línea tenga contenido.
        if len(parts) > 0:
            # El código de la aerolínea está en la última posición de la línea.
            codigo = parts[len(parts) - 1]
            # Añadimos el código de la aerolínea a la terminal.
            terminal.airlines.append(codigo)
        # Pasamos a la siguiente línea.
        i = i + 1

    # Devolvemos 0 para indicar que se ha cargado correctamente.
    return 0


# Esta función carga toda la estructura del aeropuerto desde LEBL.txt.
def LoadAirportStructure(filename):
    # Intentamos abrir el archivo con la estructura del aeropuerto.
    try:
        # Abrimos el archivo en modo lectura.
        f = open(filename, "r")
        # Leemos todas las líneas del archivo.
        lineas = f.readlines()
        # Cerramos el archivo.
        f.close()
    # Si hay error al abrir el archivo, entramos aquí.
    except:
        # Mostramos por consola que no se ha podido abrir.
        print("No se ha podido abrir", filename)
        # Devolvemos error.
        return -1

    # Si el archivo está vacío, devolvemos error.
    if len(lineas) == 0:
        # Código de error.
        return -1

    # Separamos la primera línea, donde está el código LEBL.
    primera = lineas[0].split()
    # Creamos el objeto BarcelonaAP con el código de la primera línea.
    bcn = BarcelonaAP(primera[0])
    # Esta variable guardará la terminal que estemos leyendo en cada momento.
    terminal_actual = ""

    # Empezamos en la línea 1 porque la línea 0 ya se ha usado.
    i = 1
    # Recorremos todas las líneas restantes.
    while i < len(lineas):
        # Separamos la línea actual en palabras.
        parts = lineas[i].split()

        # Comprobamos que la línea no esté vacía.
        if len(parts) > 0:
            # Si la línea empieza por Terminal, debemos crear una nueva terminal.
            if parts[0] == "Terminal":
                # Creamos una terminal con el nombre indicado, por ejemplo T1.
                terminal_actual = Terminal(parts[1])
                # Cargamos las aerolíneas de esa terminal desde su archivo .txt.
                LoadAirlines(terminal_actual, parts[1])
                # Añadimos la terminal a la lista de terminales del aeropuerto.
                bcn.terminals.append(terminal_actual)

            # Si la línea empieza por Area, debemos crear una zona de embarque.
            elif parts[0] == "Area" and terminal_actual != "":
                # Guardamos la letra de la zona, por ejemplo A.
                area_letter = parts[1]
                # Guardamos el tipo de zona: Schengen o non-Schengen.
                area_type = parts[2]
                # Guardamos el primer número de puerta.
                init_gate = int(parts[4])
                # Guardamos el último número de puerta.
                end_gate = int(parts[6])

                # Construimos el nombre de la zona, por ejemplo T1BAA.
                area_name = terminal_actual.name + "BA" + area_letter
                # Creamos el objeto BoardingArea.
                area = BoardingArea(area_name, area_type)

                # Creamos el prefijo para las puertas, por ejemplo T1BAAG.
                prefix = area_name + "G"
                # Creamos todas las puertas de esa zona.
                SetGates(area, init_gate, end_gate, prefix)

                # Añadimos la zona de embarque a la terminal actual.
                terminal_actual.boardingAreas.append(area)

        # Pasamos a la siguiente línea del archivo.
        i = i + 1

    # Devolvemos el aeropuerto completo con terminales, zonas, puertas y aerolíneas.
    return bcn


# Esta función devuelve la ocupación de todas las puertas del aeropuerto.
def GateOccupancy(bcn):
    # Creamos una lista donde guardaremos la información de cada puerta.
    occupancy = []

    # Empezamos a recorrer las terminales.
    i = 0
    # Recorremos todas las terminales.
    while i < len(bcn.terminals):
        # Guardamos la terminal actual.
        terminal = bcn.terminals[i]

        # Empezamos a recorrer las zonas de embarque de la terminal.
        j = 0
        # Recorremos todas las zonas de embarque.
        while j < len(terminal.boardingAreas):
            # Guardamos la zona actual.
            area = terminal.boardingAreas[j]

            # Empezamos a recorrer las puertas de la zona.
            k = 0
            # Recorremos todas las puertas.
            while k < len(area.gates):
                # Guardamos la puerta actual.
                gate = area.gates[k]
                # Añadimos a la lista los datos de esta puerta.
                occupancy.append([terminal.name, area.name, gate.name, gate.occupied, gate.aircraft_id])
                # Pasamos a la siguiente puerta.
                k = k + 1

            # Pasamos a la siguiente zona.
            j = j + 1

        # Pasamos a la siguiente terminal.
        i = i + 1

    # Devolvemos la lista completa de ocupación.
    return occupancy


# Esta función comprueba si una aerolínea trabaja en una terminal.
def IsAirlineInTerminal(terminal, name):
    # Si el nombre está vacío, no se puede encontrar.
    if name == "":
        # Devolvemos False porque no hay aerolínea que buscar.
        return False

    # Variable para saber si la aerolínea se ha encontrado.
    found = False
    # Empezamos en la primera posición de la lista de aerolíneas.
    i = 0
    # Recorremos la lista mientras no se haya encontrado.
    while i < len(terminal.airlines) and found == False:
        # Si el código de la lista coincide con el que buscamos, la hemos encontrado.
        if terminal.airlines[i] == name:
            # Marcamos encontrado como True.
            found = True
        # Si no coincide, seguimos buscando.
        else:
            # Pasamos a la siguiente aerolínea.
            i = i + 1

    # Devolvemos True si se ha encontrado y False si no.
    return found


# Esta función busca en qué terminal trabaja una aerolínea.
def SearchTerminal(bcn, name):
    # Variable donde guardaremos el nombre de la terminal encontrada.
    terminal_name = ""

    # Empezamos recorriendo las terminales.
    i = 0
    # Recorremos mientras queden terminales y no hayamos encontrado ninguna.
    while i < len(bcn.terminals) and terminal_name == "":
        # Comprobamos si la aerolínea está en la terminal actual.
        if IsAirlineInTerminal(bcn.terminals[i], name) == True:
            # Guardamos el nombre de la terminal encontrada.
            terminal_name = bcn.terminals[i].name
        # Si no está, seguimos buscando.
        else:
            # Pasamos a la siguiente terminal.
            i = i + 1

    # Devolvemos el nombre de la terminal, o vacío si no se ha encontrado.
    return terminal_name


# Esta función asigna una puerta libre a un avión.
def AssignGate(bcn, aircraft):
    # Buscamos la terminal que corresponde a la aerolínea del avión.
    terminal_name = SearchTerminal(bcn, aircraft.airline)

    # Si no se encuentra terminal para la aerolínea, devolvemos error.
    if terminal_name == "":
        # Código de error.
        return -1

    # Si el aeropuerto de origen es Schengen, necesitamos una zona Schengen.
    if IsSchengenAirport(aircraft.origin) == True:
        # Tipo de zona que necesitamos.
        needed_type = "Schengen"
    # Si el aeropuerto de origen no es Schengen, necesitamos una zona non-Schengen.
    else:
        # Tipo de zona que necesitamos.
        needed_type = "non-Schengen"

    # Empezamos a recorrer las terminales.
    i = 0
    # Recorremos todas las terminales.
    while i < len(bcn.terminals):
        # Guardamos la terminal actual.
        terminal = bcn.terminals[i]

        # Comprobamos si es la terminal que necesita el avión.
        if terminal.name == terminal_name:
            # Empezamos a recorrer sus zonas de embarque.
            j = 0
            # Recorremos todas las zonas de embarque.
            while j < len(terminal.boardingAreas):
                # Guardamos la zona actual.
                area = terminal.boardingAreas[j]

                # Comprobamos si la zona tiene el tipo necesario.
                if area.area_type == needed_type:
                    # Empezamos a recorrer las puertas de esta zona.
                    k = 0
                    # Recorremos todas las puertas.
                    while k < len(area.gates):
                        # Guardamos la puerta actual.
                        gate = area.gates[k]

                        # Si la puerta está libre, podemos asignarla.
                        if gate.occupied == False:
                            # Marcamos la puerta como ocupada.
                            gate.occupied = True
                            # Guardamos el id del avión que ocupa la puerta.
                            gate.aircraft_id = aircraft.aircraft_id
                            # Devolvemos 0 porque la asignación ha ido bien.
                            return 0

                        # Pasamos a la siguiente puerta.
                        k = k + 1

                # Pasamos a la siguiente zona.
                j = j + 1

        # Pasamos a la siguiente terminal.
        i = i + 1

    # Si no se ha encontrado ninguna puerta libre adecuada, devolvemos error.
    return -1


# Esta parte solo se ejecuta si abrimos LEBL.py directamente.
if __name__ == "__main__":
    # Cargamos la estructura del aeropuerto desde LEBL.txt.
    bcn = LoadAirportStructure("LEBL.txt")

    # Comprobamos que se haya cargado correctamente.
    if bcn != -1:
        # Mostramos el código del aeropuerto cargado.
        print("Aeropuerto cargado:", bcn.code)
        # Mostramos cuántas terminales se han cargado.
        print("Terminales:", len(bcn.terminals))

        # Cargamos los vuelos desde Arrivals.txt.
        aircrafts = LoadArrivals("Arrivals.txt")
        # Contador de vuelos con puerta asignada.
        asignados = 0
        # Contador de vuelos sin puerta asignada.
        no_asignados = 0

        # Empezamos a recorrer la lista de vuelos.
        i = 0
        # Recorremos todos los vuelos.
        while i < len(aircrafts):
            # Intentamos asignar puerta al vuelo actual.
            res = AssignGate(bcn, aircrafts[i])
            # Si el resultado es 0, se ha asignado puerta.
            if res == 0:
                # Sumamos uno al contador de asignados.
                asignados = asignados + 1
            # Si no, el vuelo no se ha podido asignar.
            else:
                # Sumamos uno al contador de no asignados.
                no_asignados = no_asignados + 1
            # Pasamos al siguiente vuelo.
            i = i + 1

        # Mostramos cuántos vuelos han sido asignados.
        print("Vuelos asignados:", asignados)
        # Mostramos cuántos vuelos no han sido asignados.
        print("Vuelos no asignados:", no_asignados)

        # Obtenemos la lista de ocupación de puertas.
        ocupacion = GateOccupancy(bcn)
        # Mostramos un título para las primeras puertas.
        print("Primeras puertas:")
        # Empezamos por la primera puerta.
        i = 0
        # Mostramos como máximo las primeras 20 puertas.
        while i < len(ocupacion) and i < 20:
            # Imprimimos la información de la puerta actual.
            print(ocupacion[i])
            # Pasamos a la siguiente puerta.
            i = i + 1
