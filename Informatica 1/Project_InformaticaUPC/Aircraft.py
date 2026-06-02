import os
import matplotlib.pyplot as plt
import math


class Aircraft:
    def __init__(self, aircraft_id, airline, origin, arrival_time, destination="", departure_time=""):  # Definimos la clase.
        self.aircraft_id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.arrival_time = arrival_time  # Clase con matricula, nombre aerolinea, origen y tiempo de llegada.
        self.destination = destination
        self.departure_time = departure_time


def LoadArrivals(filename):
    aircrafts = []  # Queremos que lea el archivo y lo ponga en lista de elementos.

    try:
        f = open(filename, "r")
        lineas = f.readlines()  # Leemos todas las líneas para recorrerlas por índice
        f.close()

        i = 1
        while i < len(lineas):
            parts = lineas[i].split()

            if len(parts) == 4:  # Si no tiene la estructura adecuada salta de linea.
                id_aircraft = parts[0]
                origin = parts[1]
                time = parts[2]
                airline = parts[3]

                nuevo_avion = Aircraft(id_aircraft, airline, origin, time)  # Creamos el objeto Aircraft y lo añadimos en una lista.
                aircrafts.append(nuevo_avion)  # Si el objeto no tiene 4 componentes lo ignora.
            i = i + 1

    except:
        print(f"El archivo {filename} no se pudo abrir.")
        return []  # Si no existe devolvemos la lista vacia.

    return aircrafts  # Si existe devolvemos la lista creada.


def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:  # Comprobación
        print("La lista esta vacia, no hay datos de vuelo.")
        return []  # Devolvemos lista vacia tal como pide el enunciado.

    horas = [0] * 24  # Creamos una lista vacia con las horas demomento con ceros.

    i = 0
    while i < len(aircrafts):  # Miramos avion por avion a que hora llega.
        avion = aircrafts[i]
        partes = avion.arrival_time.split(":")  # Separamos las horas de los minutos.
        hora = int(partes[0])  # Cojemos las horas.

        if 0 <= hora < 24:
            horas[hora] = horas[hora] + 1
            # Sumamos en cada posicion de la lista la hora indicada en su respectiva posicion.
        i = i + 1

    eje_x = []
    i = 0
    while i < 24:  # Creamos una lista que vaya del 1 hasta el 23.
        eje_x.append(i)
        i = i + 1

    plt.bar(eje_x, horas, color='#9BB8CD')# Gráfico de barras
    plt.gcf().set_facecolor("#FAF3E0")
    plt.gca().set_facecolor("#FAF3E0")
    plt.title("Llegadas por hora a Barcelona (LEBL)")
    plt.xlabel("Hora del día")
    plt.ylabel("Número de vuelos")
    plt.xticks(eje_x)  # Ponemos las horas debajo.

    plt.show()


def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        return []
    try:
        f = open(filename, "w") #Abrimos y que el programa escriba el documento.
        f.write("aircraft_id airline origin arrival_time") #Definimos cabecera para mantener el formato.

        i = 0
        while i < len(aircrafts):
            avion = aircrafts[i]
            linea = (f"{avion.aircraft_id} {avion.airline} {avion.origin} {avion.arrival_time} \n")
            f.write(linea) #Para que el programa nos escriba la linea.
            i = i + 1

        f.close()
        print(f"Se han guardado {len(aircrafts)} vuelos en {filename}.")

    except:
        print(f"Error, no se ha podido guardar {filename}.")


def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("La lista esta vacia.")
        return []

    nombres = []
    cantidades = []

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]
        nombre_actual_aerolinea = avion.airline

        encontrado = False
        j = 0
        while j < len(nombres) and encontrado == False:
            if nombres[j] == nombre_actual_aerolinea:
                encontrado = True
            else:
                j = j + 1

        if encontrado == True:
            # Si ya existe, sumamos 1 en la posición donde se encontró
            cantidades[j] = cantidades[j] + 1
        else:
            # Si no existe, añadimos el nombre y empezamos la cuenta en 1
            nombres.append(nombre_actual_aerolinea)
            cantidades.append(1)
        i = i + 1

    plt.bar(nombres, cantidades, color='#FFD6BA')
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=45)
    plt.gcf().set_facecolor("#FAF3E0")
    plt.gca().set_facecolor("#FAF3E0")
    plt.show()


def PlotFlightsType(aircrafts, airports):
    if len(aircrafts) == 0:
        print("La lista esta vacia.")
        return []

    vuelos_schengen = 0
    vuelos_no_schengen = 0

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]
        codigo_origen = avion.origin #guardamos en una variable el origen del avion que lo encontramos de la clase.

        encontrado = False
        j = 0
        while j < len(airports) and encontrado == False:
             if airports[j].ICAOcode == codigo_origen:
                 encontrado = True

                 if airports[j].Schengen == True:
                     vuelos_schengen = vuelos_schengen + 1 #Si encontramos el codigo del aeropuerto en la lista de airports entonces le sumamos uno a la variable de aeropuerto schengen.
                 else:
                     vuelos_no_schengen = vuelos_no_schengen + 1
             else:
                 j = j + 1
        i = i + 1

    etiquetas = ['Schengen', 'No Schengen']
    valores = [vuelos_schengen, vuelos_no_schengen]
    plt.bar(etiquetas, valores, color=['#BEE3DB', '#F5B7B1'])
    plt.title("Vuelos según origen (Schengen vs No Schengen)")
    plt.gcf().set_facecolor("#FAF3E0")
    plt.gca().set_facecolor("#FAF3E0")
    plt.show()


def MapFlights(aircrafts, airports):
    f = open("flights_map.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n') #Escribimos la cabecera.
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Trayectorias de Vuelos</name>\n')
    lat_dest = 41.297445 #Escribimos las coordenadas de Barcelona que es el destino fijo.
    lon_dest = 2.083294

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]
        codigo_origen = avion.origin

        encontrado = False
        j = 0
        while j < len(airports) and encontrado == False:
            if airports[j].ICAOcode == codigo_origen:
                encontrado = True
                aero_ref = airports[j]  # Guardamos el objeto aeropuerto.
            else:
                j = j + 1

        if encontrado == True:
            if aero_ref.Schengen == True:
                color = "ff00ff00"  # Verde.
            else:
                color = "ff0000ff"  # Rojo.

            f.write('<Placemark>\n')
            f.write(f'  <name>Vuelo {avion.aircraft_id}</name>\n')
            f.write('  <Style>\n')
            f.write('    <LineStyle>\n')
            f.write(f'      <color>{color}</color>\n')
            f.write('      <width>2</width>\n')
            f.write('    </LineStyle>\n')
            f.write('  </Style>\n')

            f.write('  <LineString>\n')
            f.write('    <coordinates>\n')
            f.write(f'      {aero_ref.longitude},{aero_ref.latitude},0\n')
            f.write(f'      {lon_dest},{lat_dest},0\n')
            f.write('    </coordinates>\n')
            f.write('  </LineString>\n')
            f.write('</Placemark>\n')
        i = i + 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Archivo flights_map.kml generado con éxito.")
    os.startfile("flights_map.kml")


def Haversine(lat1, lon1, lat2, lon2):
    pi = 3.1415926535
    lat1_rad = lat1 * pi / 180
    lon1_rad = lon1 * pi / 180
    lat2_rad = lat2 * pi / 180
    lon2_rad = lon2 * pi / 180
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c


def LongDistanceArrivals(aircrafts, airports):
    vuelos_lejanos = []
    lat_bcn = 41.297445
    lon_bcn = 2.083294

    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]
        origen = avion.origin
        encontrado = False
        j = 0
        while j < len(airports) and encontrado == False:
            if airports[j].ICAOcode == origen:
                encontrado = True
                dist = Haversine(airports[j].latitude, airports[j].longitude, lat_bcn, lon_bcn)
                if dist > 2000:
                    vuelos_lejanos.append(avion)
            else:
                j = j + 1
        i = i + 1
    return vuelos_lejanos

#Leemos el archivo y leemos los datos de los vuelos que despegan
def LoadDepartures(filename):
    aircrafts = []
    try:
        f = open(filename, "r")

        # 1. Leemos la primera línea y no hacemos nada con ella para saltarnos la cabecera
        f.readline()

        # 2. Leemos la primera línea de datos reales
        linea = f.readline()

        # 3. Mientras la línea no esté vacía (significa que no hemos llegado al final del archivo)
        while linea != "":
            parts = linea.split()

            if len(parts) >= 4:
                id_aircraft = parts[0]
                dest = parts[1]
                dep_time = parts[2]
                airline = parts[3]

                if len(dep_time) == 4 and dep_time[1] == ':':
                    dep_time = "0" + dep_time

                # Pasamos los parámetros en orden: id, aerolínea, origen (""), llegada (""), destino, salida
                nuevo_avion = Aircraft(id_aircraft, airline, "", "", dest, dep_time)
                aircrafts.append(nuevo_avion)

            # 4. Avanzamos leyendo la siguiente línea antes de que el bucle vuelva a empezar
            linea = f.readline()

        # Cerramos el archivo al salir del bucle while
        f.close()

    except:
        print(f"El archivo {filename} no se pudo abrir.")
        return []

    return aircrafts


def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 or len(departures) == 0:
        return []

    merged_list = []

    i = 0
    while i < len(arrivals):
        arr = arrivals[i]
        nuevo_ac = Aircraft(arr.aircraft_id, arr.airline, arr.origin, arr.arrival_time)
        merged_list.append(nuevo_ac)
        i = i + 1

    j = 0
    while j < len(departures):
        dep = departures[j]
        encontrado = False

        k = 0
        while k < len(merged_list) and encontrado == False:
            ac = merged_list[k]

            if ac.aircraft_id == dep.aircraft_id and ac.departure_time == "":
                if ac.arrival_time < dep.departure_time:
                    ac.destination = dep.destination
                    ac.departure_time = dep.departure_time
                    encontrado = True
            k = k + 1

        if encontrado == False:
            # Pasamos los parámetros ordenados al constructor para el avión nocturno
            night_ac = Aircraft(dep.aircraft_id, dep.airline, "", "", dep.destination, dep.departure_time)
            merged_list.append(night_ac)
        j = j + 1

    return merged_list


def NightAircraft(aircrafts):
    # Si la lista de entrada está vacía, devolvemos un código de error (por ejemplo, -1)
    if len(aircrafts) == 0:
        return -1

    night_list = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]

        # Comprobamos que NO tiene información de llegada (en blanco) pero SÍ de salida
        if ac.arrival_time == "" and ac.departure_time != "":
            night_list.append(ac)

        i = i + 1

    return night_list


if __name__ == "__main__":
    aircrafts = LoadArrivals("arrivals.txt")  # Cargamos los vuelos del documento.

    PlotArrivals(aircrafts)

    from Airport import LoadAirports, SetSchengen  # Marcamos las funciones que ha de coger de Airport.py.

    airports = LoadAirports("airports.txt")

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    PlotFlightsType(aircrafts, airports)  # Probamos tanto las gráficas de Plot como la del Maps programadas.
    MapFlights(aircrafts, airports)

    inspeccion = LongDistanceArrivals(aircrafts, airports)  # Verificamos la última función y mostramos los últimos 2000km.
    print("Vuelos que requieren inspección especial (>2000km):")

    i = 0
    while i < len(inspeccion):
        print(inspeccion[i].aircraft_id, "desde", inspeccion[i].origin)
        i = i + 1

    MapFlights(inspeccion, airports)  # Llamamos de nuevo la funcion MapFlights y
    print("Archivo KML de LARGA DISTANCIA generado con éxito.")





























