"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import os
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
assert cf

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

analyzer = None
events_analysis_file = 'context_content_features-small.csv'
rows, columns = os.popen('stty size', 'r').read().split()
genre = {
    '1- reggae': (60, 90),
    '2- down-tempo': (70, 100),
    '3- chill-out': (90, 120),
    '4- hip-hop': (85, 115),
    '5- jazz and funk': (120, 125),
    '6- pop': (100, 130),
    '7- r&b': (60, 80),
    '8- rock': (110, 140),
    '9- metal': (100, 160)}


def printMenu():
    print("_"*int(columns))
    print("1- Inicializar analizador y cargar datos")
    print(
        "2- Conocer cuántas reproducciones se tienen con una característica " +
        "específica de contenido y un rango determinado")
    print("3- Encontrar música para festejar")
    print("4- Encontrar música para estudiar")
    print("5- Agregar un género a la base de datos")
    print("6 - Encontrar música por género(s)")
    print("7 - Encontrar género más escuchado dado un rango de horas")
    print("Presione cualquier otra tecla para salir")


def printfirstandlast5(arraylist):
    printlist = arraylist['listening_events']
    i = 1
    listsize = lt.size(printlist)
    while i <= 5:
        element = lt.getElement(printlist, i)
        print('\n')
        print(
                'Track ID: ' + str(element.get('track_id')) + ", " +
                'Instrumentalness: ' + str(element.get('instrumentalness'))
                + ", " + 'Liveness: ' + str(element.get('liveness')) + ", " +
                'Speechiness: ' + str(element.get('speechiness')) + ", " +
                'Danceability: ' + str(element.get('danceability')) + ", " +
                'Valence: ' + str(element.get('valence')) + ", " +
                'Loudness: ' + str(element.get('loudness')) + ", " +
                'Tempo: ' + str(element.get('tempo')) + ", " +
                'Acousticness: ' + str(element.get('acousticness')) + ", " +
                'Energy: ' + str(element.get('energy')) + ", " +
                'Mode: ' + str(element.get('mode')) + ", " +
                'key: ' + str(element.get('key')) + ", " +
                'Artist ID: ' + str(element.get('artist_id')) + ", " +
                'Created at: ' + str(element.get('created_at')) + ", " +
                'User ID: ' + str(element.get('user_id')))
        i += 1
    i = listsize
    while i > (listsize - 5):
        element = lt.getElement(printlist, (i))
        print('\n')
        print(
                'Track ID: ' + str(element.get('track_id')) + ", " +
                'Instrumentalness: ' + str(element.get('instrumentalness'))
                + ", " + 'Liveness: ' + str(element.get('liveness')) + ", " +
                'Speechiness: ' + str(element.get('speechiness')) + ", " +
                'Danceability: ' + str(element.get('danceability')) + ", " +
                'Valence: ' + str(element.get('valence')) + ", " +
                'Loudness: ' + str(element.get('loudness')) + ", " +
                'Tempo: ' + str(element.get('tempo')) + ", " +
                'Acousticness: ' + str(element.get('acousticness')) + ", " +
                'Energy: ' + str(element.get('energy')) + ", " +
                'Mode: ' + str(element.get('mode')) + ", " +
                'key: ' + str(element.get('key')) + ", " +
                'Artist ID: ' + str(element.get('artist_id')) + ", " +
                'Created at: ' + str(element.get('created_at')) + ", " +
                'User ID: ' + str(element.get('user_id')))
        i -= 1


def printartists(artistsmap):
    i = 1
    keys = mp.keySet(artistsmap)
    while i < 11:
        print("Artist no. " + str(i) + " ID: " + str(lt.getElement(keys, i)))
        i += 1


def printgenre(dicc):
    for genre in dicc:
        result = dicc[genre]
        print('\n')
        print(genre)
        print('Registro de eventos Cargados: ' + str(result[0]))
        print('Artistas únicos Cargados: ' + str(result[1]))
        printartists(result[4])


def printfortotal(analyzer, ranges):
    total_events = 0
    for every_tuple in ranges:
        events = controller.getEventsByRange(
            analyzer, 'tempo', every_tuple[0], every_tuple[1])
        total_events += events[0]
    print('\n')
    print("Registro de eventos totales: " + str(total_events))


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        analyzer = controller.init()
        print("Cargando información de los archivos ....")
        answer = controller.loadData(analyzer, events_analysis_file)
        print('Registro de eventos Cargados: ' + str(controller.eventsSize(
            analyzer)))
        print('Artistas únicos Cargados: ' + str(controller.artistsSize(
            analyzer)))
        print('Pistas únicas Cargados: ' + str(controller.tracksSize(
            analyzer)))
        print('\n')
        print('Primeros y últimos 5 cargados, respectivamente: ')
        printfirstandlast5(analyzer)
        print('\n')
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    elif int(inputs[0]) == 2:
        criteria = input("Ingrese el criterio a evaluar: ")
        initial = float(input("Ingrese el límite inferior: "))
        final = float(input("Ingrese el límite superior: "))
        print("Buscando en la base de datos ....")
        result = controller.getEventsByRange(
            analyzer, criteria, initial, final)
        print('Registro de eventos Cargados: ' + str(result[0]))
        print('Artistas únicos Cargados: ' + str(result[1]))

    elif int(inputs[0]) == 3:
        initialenergy = float(input(
            "Ingrese el límite inferior para la energía: "))
        finalenergy = float(input(
            "Ingrese el límite superior para la energía: "))
        energyrange = (initialenergy, finalenergy)
        initialdanceability = float(input(
            "Ingrese el límite inferior para la perreabilidad: "))
        finaldanceability = float(input(
            "Ingrese el límite superior para la perreabilidad: "))
        danceabilityrange = (initialdanceability, finaldanceability)
        print("Buscando en la base de datos ....")
        print(controller.getMusicToParty(
            analyzer, energyrange, danceabilityrange))

    elif int(inputs[0]) == 4:
        initialinstrumentalness = float(input(
            "Ingrese el límite inferior para la instrumentalidad: "))
        finalinstrumentalness = float(input(
            "Ingrese el límite superior para la instrumentalidad: "))
        instrumentalnessrange = (
            initialinstrumentalness, finalinstrumentalness)
        initialtempo = float(input(
            "Ingrese el límite inferior para el tempo: "))
        finaltempo = float(input(
            "Ingrese el límite superior para el tempo: "))
        temporange = (initialtempo, finaltempo)
        print("Buscando en la base de datos ....")
        print(controller.getMusicToStudy(
            analyzer, instrumentalnessrange, temporange))

    elif int(inputs[0]) == 5:
        genero = input("Ingrese el nombre del género musical: ")
        lim_inf = int(input("Ingrese el límite inferior del Tempo: "))
        lim_sup = int(input("Ingrese el límite superior del Tempo: "))
        n = len(genre.keys()) + 1
        llave = str(n) + "- " + str(genero)
        genre[llave] = (lim_inf, lim_sup)
        print("El género " + str(genero) + " ha sido agregado con éxito!")
        print(genre)

    elif int(inputs[0]) == 6:
        lista_generos = []
        generos = "1"
        while len(generos) > 0:
            generos = (input(
                "Ingrese el número de cada uno de los géneros a consultar: "))
            if len(generos) != 0:
                lista_generos.append(generos)
        ranges = controller.getRanges(lista_generos, genre)
        dicc = controller.getEventsByRangeGenres(
            analyzer, 'tempo', genre, lista_generos)
        printgenre(dicc)
        printfortotal(analyzer, ranges)

    elif int(inputs[0]) == 7:
        print("Ingrese la hora de inicio en formato 24h: (Ej. 12:34:56)")
        tiempo_inicio = input("~")
        print("Ingrese la hora final en formato 24h: (Ej. 12:34:56)")
        tiempo_final = input("~")
        result = controller.getGenresByTime(
            analyzer, tiempo_inicio, tiempo_final)

    else:
        sys.exit(0)
sys.exit(0)
