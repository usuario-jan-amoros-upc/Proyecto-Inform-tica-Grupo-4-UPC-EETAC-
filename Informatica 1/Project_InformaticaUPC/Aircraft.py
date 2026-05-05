import matplotlib.pyplot as plt


class Aircraft:
    def __init__(self, aircraft_id, origin, arrival_time, airline):  # Definimos la clase.
        self.aircraft_id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.arrival_time = arrival_time  # Clase con matricula, nombre aerolinea, origen y tiempo de llegada.


def LoadArrivals(filename):
    aircrafts = []  # Queremos que lea el archivo y lo ponga en lista de elementos.

    try:
        f = open(filename, "r")
        f.readline()
        lineas = f.readline()  # Leemos todas las líneas para recorrerlas por índice

        while lineas != "" :
            parts = lineas.rstrip().split()


            if len(parts) == 4:  # Si no tiene la estructura adecuada salta de linea.
                id_aircraft = parts[0]
                origin = parts[1]
                time = parts[2]
                airline = parts[3]

                nuevo_avion = Aircraft(id_aircraft, origin, time, airline)  # Creamos el objeto Aircraft y lo añadimos en una lista.
                aircrafts.append(nuevo_avion)  # Si el objeto no tiene 4 componentes lo ignora.
            lineas = f.readline()
        f.close()

    except:
        print(f"El archivo {filename} no se pudo abrir.")
        return []  # Si no existe devolvemos la lista vacia.

    return aircrafts  # Si existe devolvemos la lista creada.


def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:  # Comprobación
        print("La lista esta vacia, no hay datos de vuelo.")
        return []  # Devolvemos lista vacia tal como pide el enunciado.

    horas = [0] * 24  # Creamos una lista vacia con las horas demomento con ceros.

    for i in range(len(aircrafts)):  # Miramos avion por avion a que hora llega.
        avion = aircrafts[i]
        partes = avion.arrival_time.split(":")  # Separamos las horas de los minutos.
        hora = int(partes[0])  # Cojemos las horas.

        if 0 <= hora < 24:
            horas[hora] = horas[hora] + 1
            # Sumamos en cada posicion de la lista la hora indicada en su respectiva posicion.

    eje_x = []
    for i in range(24):  # Creamos una lista que vaya del 1 hasta el 23.
        eje_x.append(i)

    plt.bar(eje_x, horas, color='blue')  # Gráfico de barras
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
        f.write("aircraft_id origin arrival_time airline\n") #Definimos cabecera para mantener el formato.

        for i in range(len(aircrafts)):
            avion = aircrafts[i]
            linea = (f"{avion.aircraft_id} {avion.origin} {avion.arrival_time} {avion.airline}\n")
            f.write(linea) #Para que el programa nos escriba la linea.

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

    for i in range(len(aircrafts)):
        avion = aircrafts[i]
        nombre_actual_aerolinea = avion.airline.strip()

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

    plt.figure(figsize=(10,6))
    plt.bar(nombres, cantidades, color='orange')
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=90, fontsize=8)
    plt.xlabel("Aerolínea")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    print(f"Aerolineas encontradas:{nombres}")
    plt.show()


def PlotFlightsType(aircrafts,airports):
    if len(aircrafts) == 0:
        print("La lista esta vacia.")
        return []

    vuelos_schengen = 0
    vuelos_no_schengen = 0

    for i in range(len(aircrafts)):
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

    categoria = ['Vuelos Totales']
    plt.bar(categoria, [vuelos_schengen], color='green', label='Schengen')
    plt.bar(categoria, [vuelos_no_schengen], bottom=[vuelos_schengen], color='red', label='No Schengen')
    plt.title("Vuelos según origen (Schengen vs No Schengen)")
    plt.ylabel("Cantidad de vuelos")
    plt.legend() #Importante para saber qué color es cada uno
    plt.show()

def MapFlights(aircrafts, airports):
    f = open("flights_map.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n') #Escribimos la cabecera.
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Trayectorias de Vuelos</name>\n')
    lat_dest = 41.297445 #Escribimos las coordenadas de Barcelona que es el destino fijo.
    lon_dest = 2.083294

    for i in range(len(aircrafts)):
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

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Archivo flights_map.kml generado con éxito.")


import math



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

    for i in range(len(aircrafts)):
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
    return vuelos_lejanos


if __name__ == "__main__":
    aircrafts = LoadArrivals("arrivals.txt") #Cargamos los vuelos del documento.

    from Airport import LoadAirports, SetSchengen #Marcamos las funciones que ha de cojer de Airport.py.
    airports = LoadAirports("airports.txt")

    for i in range(len(airports)):
        SetSchengen(airports[i])

    MapFlights(aircrafts, airports)


    inspeccion = LongDistanceArrivals(aircrafts, airports) #Verificamos la ultima funcion y mostramos los ultimos 2000km.
    print("Vuelos que requieren inspección especial (>2000km):")
    for i in range(len(inspeccion)):
        print(inspeccion[i].aircraft_id, "desde", inspeccion[i].origin)

    MapFlights(inspeccion, airports) #Llamamos de nuevo la funcion MapFlights.
    print("Archivo KML de LARGA DISTANCIA generado con éxito.")


    SaveFlights(aircrafts, "vuelos_salida.txt")
    print("Archivo 'vuelos_salida.txt' guardado y todas las gráficas generadas.")


    PlotAirlines(aircrafts)

    PlotArrivals(aircrafts)

    PlotFlightsType(aircrafts,airports)































