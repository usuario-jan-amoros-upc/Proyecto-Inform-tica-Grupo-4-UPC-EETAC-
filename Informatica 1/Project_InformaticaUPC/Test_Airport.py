from Airport import *

airport = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport(airport)


print("Cargar aeropuertos y coordenadas ")
lista = LoadAirports("airports.txt")

if len(lista) > 0:
    print(f"Se han cargado {len(lista)} aeropuertos.")
    print(f"Primer aeropuerto: {lista[0].ICAOcode}, Lat: {lista[0].latitude}")
else:
    print("No se ha cargado nada. Revisa si 'airports.txt' existe.")

print("Añadir aeropuerto")
bcn = Airport("LEBL", 41.29, 2.08)
resultado_add = AddAirport(lista, bcn)

if resultado_add == 0:
    print("LEBL añadido correctamente.")
else:
    print("No se pudo añadir, quizás ya existía.")

print("Verificamos duplicado.")
resultado_dup = AddAirport(lista, bcn)
if resultado_dup == -1:
    print("No se permitió añadir el mismo código dos veces.")

print("Quitar aeropuerto ")
resultado_rem = RemoveAirport(lista, "LEBL")

if resultado_rem == 0:
    print("LEBL borrado correctamente.")
else:
    print("No se encontró el código para borrar.")

print("Guardar Schengen ")
if len(lista) > 0:
    lista[0].Schengen = True
    print(f"Marcado {lista[0].ICAOcode} como Schengen.")

resultado_save = SaveSchengenAirports(lista, "schengen_solo.txt")

if resultado_save == 0:
    print("Archivo 'schengen_solo.txt' creado.")
else:
    print("ENo se creó el archivo (lista vacía o sin Schengen).")

print(f"Aeropuertos en la lista: {len(lista)}")
PlotAirports(lista)
MapAirports(lista)
