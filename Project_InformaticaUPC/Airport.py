class Airport:
    def __init__(self, ICAOcode, latitude, longitude):
        self.ICAOcode = ICAOcode
        self.latitude = latitude
        self.longitude = longitude
        self.Schengen = False

def IsSchengenAirport(ICAOcode):
    if ICAOcode == "":
        return False

    Paises = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
              'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    prefijo = ICAOcode[0:2]
    encontrado = False
    i = 0

    while i < len(Paises) and encontrado == False:
        if Paises[i] == prefijo:
            encontrado = True
        else:
            i = i + 1
    return encontrado


def SetSchengen(airport):
    resultado = IsSchengenAirport(airport.ICAOcode)
    airport.Schengen = resultado

def PrintAirport(airport):
    print(f"Aeropuerto:{airport.ICAOcode}")
    print(f"Latitud:{airport.latitude}")
    print(f"Longitud:{airport.longitude}")
    print(f"Schengen:{airport.Schengen}")

def ConvertCoordinates(coordinates):
    direccion = coordinates[0]
    if len(coordinates) == 7:
        grados = float(coordinates[1:3])
        minutos = float(coordinates[3:5])
        segundos = float(coordinates[5:7])
    else:
        grados = float(coordinates[1:4])
        minutos = float(coordinates[4:6])
        segundos = float(coordinates[6:8])

    decimal = grados + (minutos / 60) + (segundos / 3600)
    if direccion == "W" or direccion == "S":
        decimal = decimal * (-1)
    return decimal


def LoadAirports(filename):
    airports = []
    try:
        f = open(filename, "r")
        f.readline()
        lineas = f.readline()

        while lineas != "":
            datos = lineas.split()
            if len(datos) == 3:
                codigo = datos[0]
                lat_decimal = ConvertCoordinates(datos[1])
                lon_decimal = ConvertCoordinates(datos[2])

                nuevo = Airport(codigo, lat_decimal, lon_decimal)
                SetSchengen(nuevo)
                airports.append(nuevo)
            lineas = f.readline()
        f.close()
    except:
        print("Error al leer el archivo de aeropuertos.")

    return airports


def AddAirport(airports, airport):
    repetido = False
    i = 0
    while i < len(airports) and repetido == False:
        if airports[i].ICAOcode == airport.ICAOcode:
            repetido = True
        else:
            i = i + 1

    if repetido == False:
        airports.append(airport)
        return 0
    else:
        return -1


def RemoveAirport(airports, code):
    i = 0
    encontrado = False
    while i < len(airports) and encontrado == False:
        if airports[i].ICAOcode == code:
            encontrado = True
            j = i
            while j < (len(airports) - 1):
                airports[j] = airports[j + 1]
                j = j + 1
            airports[:] = airports[0:len(airports)-1]
            return 0
        else:
            i = i + 1
    return -1


def SaveSchengenAirports(airports, filename):
    if len(airports) == 0:
        return -1

    f = open(filename, "w")
    f.write("CODE LAT LON \n")
    contador = 0
    for i in range(len(airports)):
        a = airports[i]
        if a.Schengen == True:
            f.write(f"{a.ICAOcode} {a.latitude} {a.longitude} \n")
            contador = contador + 1
    f.close()

    if contador == 0:
        return -1
    else:
        return 0


import matplotlib.pyplot as plt


def PlotAirports(airports):
    es_schengen = 0
    no_schengen = 0

    for i in range(len(airports)):
        if airports[i].Schengen == True:
            es_schengen = es_schengen + 1
        else:
            no_schengen = no_schengen + 1

    etiqueta = ["Aeropuertos"]

    plt.bar(etiqueta, [no_schengen], color="orange", label="Non-Schengen")

    plt.bar(etiqueta, [es_schengen], bottom=[no_schengen], color="blue", label="Schengen")

    plt.title('Distribución de Aeropuertos')
    plt.ylabel('Cantidad')
    plt.legend()
    plt.show()


def MapAirports(airports):
    f = open("airports_map.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Airports Map</name>\n')

    for i in range(len(airports)):
        a = airports[i]

        f.write('<Placemark>\n')
        f.write(f'<name>{a.ICAOcode}</name>\n')

        if a.Schengen == True:
            color = "ff00ff00"  # Verde
            status = "Schengen"
        else:
            color = "ff0000ff"  # Rojo
            status = "Non-Schengen"


        f.write('<Style>\n')
        f.write('<IconStyle>\n')
        f.write(f'<color>{color}</color>\n')
        f.write('</IconStyle>\n')
        f.write('</Style>\n')

        f.write(f'<description>Status: {status}</description>\n')

        f.write('<Point>\n')
        f.write(f'<coordinates>{a.longitude},{a.latitude},0</coordinates>\n')
        f.write('</Point>\n')
        f.write('</Placemark>\n')


    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    print("Archivo generado con éxito.")

