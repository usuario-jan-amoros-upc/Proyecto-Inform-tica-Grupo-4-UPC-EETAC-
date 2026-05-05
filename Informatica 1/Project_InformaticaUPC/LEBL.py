class Gate:
    def __init__(self,name):
        self.name=name
        self.occupied=False #Al principo todas libres.
        self.aircraft_id="" #Si esta libre no hay id aun.

class BoardingArea:
    def __init__(self,name,area_type):
        self.name=name
        self.type=area_type  #Schengen o no schengen.
        self.gates=[]  #Guardamos objetod de la clase Gate.

class terminal:
    def __init__(self,name):
        self.name=name
        self.boarding_areas=[] #Lista de BoardingArea
        self.airlines=[] #Lista de aerolineas (codigo ICAO).

class BarcelonaAP:
    def __init__(self,code):
        self.code=code
        self.terminals=[]  #Lista de objetos de terminal.

import os

def SetGates(area,init_gate,end_gate,prefix):  #Vamos a utilizar esta funcion con la intencion de crear y asignar objetos Gate a un objeto BoardingArea.
    if end_gate<init_gate: #Comprobamos error el final no puede ser ni igual ni menos al inicio.
        return -1

    area.gates=[] #Vaciamos la lista

    for i in range(init_gate,end_gate+1):
        nombre_puerta=f"{prefix}{i}"

        nueva_puerta=Gate(nombre_puerta) #Usamos la clase Gate para determinar que tiene la puerta.
        area.gates.append(nueva_puerta) #La guardamos
    return 0

def LoadAirlines(terminal, terminal_name): #Leemos el archivo _Airlines.txt y guarda los codigos ICAO en la lista de las aerolineas de la terminal.
    nombre_archivo=terminal_name+"_Airlines.txt"

    try:
        f=open(nombre_archivo,"r")
        terminal.airlines=[] #Vaciamos la lista
        linea=f.readline()

        while linea != "":
            linea=linea.strip() #Quitamos el espacio y el salto de linea.

            if linea !="":
                trozos=linea.split("\t") #Cortamos la linea por el tabulador
                if len(trozos)==2:
                    codigo=trozos[1] #ICAOcode
                    terminal.airlines.append(codigo)
            linea=f.readline()
        f.close()
        return 0
    except:
        return -1


def LoadAirportsStructure(filename):
    try:
        f=open(filename,"r")
        linea=f.readline()
        partes=linea.split()
        codigo_icao=partes[0]

        bcn=BarcelonaAP(codigo_icao) #Creamos el objeto principal

        linea=f.readline()
        while linea != "":
            linea=linea.strip()
            if linea !="":
                partes=linea.split()

                if partes[0]=="Terminal":
                    nombre_terminal=partes[1]
                    terminal_actual=terminal(nombre_terminal)
                    bcn.terminals.append(terminal_actual)


                    LoadAirlines(terminal_actual,nombre_terminal) #Llamamos a la funcion que ya hicimos para cargar sus aerolineas.
                elif partes[0]=="Area":
                    nombre_area=partes[1]
                    tipo_area=partes[2]
                    inicio=int(partes[4])
                    final=int(partes[6])

                    area_nueva=BoardingArea(nombre_area,tipo_area)

                    prefijo_puertas=terminal_actual.name + nombre_area #Creamos el prefijo para las puertas.
                    SetGates(area_nueva,inicio,final,prefijo_puertas) #Llamamos la funcion para crear puerta
                    terminal_actual.boarding_areas.append(area_nueva) #Guardamos aera en termianla actual

                linea=f.readline()

        f.close()
        return bcn
    except:
        return-1


def GateOccupancy(bcn):
    lista_informe=[]

    t=0
    while t < len(bcn.terminals): #Recorremos todas las terminales
        terminal=bcn.terminals[t]

        a=0
        while a<len(terminal.boarding_areas): #Por cada terminal recorremos sus areas
            area=terminal.boarding_areas[a]

            g=0
            while g<len(area.gates): #Por cada area recorremos sus puertas
                puerta=area.gates[g]

                nombre=puerta.name #Determinamos la informacion de cada puerta
                estado=puerta.occupied #Verdadero o falso
                avion=puerta.aircraft_id #El id del que la esta ocupando

                datos_puerta=[nombre,estado,avion]

                lista_informe.append(datos_puerta)
                g=g+1
            a=a+1
        t=t+1
    return lista_informe














