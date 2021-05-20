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
 * Jose Luis Tavera Ruiz
 * Juan Diego Yepes
 """

import config as cf
import sys
import controller
import os
import random
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
Para poder ejecutar la carga de datos, debe guardar los
archivos en una carpeta con el mismo nombre del porcen-
taje, ej: subsamples-small como carpeta.
A ello se deben las rutas de archivo a
continuación
"""

analyzer = None

events_analysis_file = 'subsamples-small/context_content_features-small.csv'
sentiment_values = 'subsamples-small/sentiment_values.csv'
hashtag_file = 'subsamples-small/user_track_hashtag_timestamp-small.csv'
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
    print("6- Encontrar música por género(s)")
    print("7- Encontrar género más escuchado dado un rango de horas")
    print("Presione cualquier otra tecla para salir")


def printTopGenres(dicc):
    '''
    Imprime los géneros iterando el diccionario
    '''
    print('\n')
    events = dicc.values()
    events = sorted(events, reverse=True)
    top = 1
    for event in events:
        for genre in dicc:
            if event == dicc[genre]:
                string = genre.split("- ")
                print(
                    'TOP ' + str(top) + ': '
                    + string[1] + ' with '
                    + str(event) + ' repetitions.')
                top += 1


def printfirstandlast5(arraylist):
    '''
    Imprime últimos y primeros 5 eventos cargados
    '''
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


def printRandom5(mapa, str1, str2):
    '''
    Imprime 5 eventos random dentro del mapa
    '''
    lista = mp.keySet(mapa)
    listsize = lt.size(lista)
    sample = random.sample(range(listsize), 5)
    n = 0
    for num in sample:
        n += 1
        element = lt.getElement(lista, num)
        thing = mp.get(mapa, element)
        value = me.getValue(thing)
        print(
            "Track:", n, str(element),
            str1, ':', value[0], str2, ':', value[1])


def printartists(artistsmap):
    '''
    Imprime los artistas en el mapa
    '''
    i = 1
    keys = mp.keySet(artistsmap)
    while i < 11:
        print("Artist no. " + str(i) + " ID: " + str(lt.getElement(keys, i)))
        i += 1


def printgenre(dicc):
    '''
    Imprime para cada género información solicitada
    '''
    for genre in dicc:
        result = dicc[genre]
        print('\n')
        print(genre)
        print('Registro de eventos Cargados: ' + str(result[0]))
        print('Artistas únicos Cargados: ' + str(result[1]))
        printartists(result[4])


def printfortotal(analyzer, ranges):
    '''
    Imprime los eventos únicos totales
    '''
    total_events = 0
    for every_tuple in ranges:
        events = controller.getEventsByRange(
            analyzer, 'tempo', every_tuple[0], every_tuple[1])
        total_events += events[0][0]
    print('\n')
    print("Registro de eventos únicos totales: " + str(total_events))


def printgenresdict(dicc):
    '''
    Imprime el diccionario de géneros
    '''
    for key in dicc.keys():
        print(key, ' Rango de tempo: ', dicc[key])


def printtop10tracks(mapa, bestgenre):
    '''
    Imprime el top 10 del mapa de tracks
    '''
    print('\n')
    bestgenre = bestgenre.split('- ')[1]
    print('Las tracks únicas de', bestgenre, 'son', mp.size(mapa))
    keys = mp.keySet(mapa)
    n = 1
    for key in lt.iterator(keys):
        if n == 11:
            break
        value = mp.get(mapa, key)
        actualvalue = me.getValue(value)
        print(
            'TOP', n, 'track:', key, 'vader:', actualvalue[0], 'hashtags',
            actualvalue[1])
        n += 1


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        analyzer = controller.init()
        print("Cargando información de los archivos...")
        answer = controller.loadData(
            analyzer, events_analysis_file, hashtag_file, sentiment_values)
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
        print(
            "Tiempo [ms]: ",
            f"{answer[0]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{answer[1]:.3f}")
        print('instrumentalness: ', om.height(analyzer['instrumentalness']))
        print('acousticness: ', om.height(analyzer['acousticness']))
        print('liveness: ', om.height(analyzer['liveness']))
        print('speechiness: ', om.height(analyzer['speechiness']))
        print('energy: ', om.height(analyzer['energy']))
        print('danceability: ', om.height(analyzer['danceability']))
        print('valence: ', om.height(analyzer['valence']))
        print('tempo: ', om.height(analyzer['tempo']))
        print('created_at: ', om.height(analyzer['created_at']))

    elif int(inputs[0]) == 2:
        criteria = input("Ingrese el criterio a evaluar: ")
        initial = float(input("Ingrese el límite inferior: "))
        final = float(input("Ingrese el límite superior: "))
        print("Buscando en la base de datos ....")
        result = controller.getEventsByRange(
            analyzer, criteria, initial, final)
        print('Registro de eventos Cargados: ' + str(result[0][0]))
        print('Artistas únicos Cargados: ' + str(result[0][1]))
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")

    elif int(inputs[0]) == 3:
        initialenergy = float(input(
            "Ingrese el límite inferior para la energía: "))
        finalenergy = float(input(
            "Ingrese el límite superior para la energía: "))
        energyrange = (initialenergy, finalenergy)
        initialdanceability = float(input(
            "Ingrese el límite inferior para la bailabilidad: "))
        finaldanceability = float(input(
            "Ingrese el límite superior para la bailabilidad: "))
        danceabilityrange = (initialdanceability, finaldanceability)
        print("Buscando en la base de datos ....")
        result = controller.getMusicToParty(
            analyzer, energyrange, danceabilityrange)
        print('Artistas únicos Cargados:', str(result[0][0]))
        print('Tracks únicas Cargadas:', str(result[0][1]))
        printRandom5(result[0][2], 'energy', 'danceability')
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")

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
        result = controller.getMusicToStudy(
            analyzer, instrumentalnessrange, temporange)
        print('Artistas únicos Cargados:', str(result[0][0]))
        print('Tracks únicas Cargadas:', str(result[0][1]))
        printRandom5(result[0][2], 'instrumentalness', 'tempo')
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")

    elif int(inputs[0]) == 5:
        genero = input("Ingrese el nombre del género musical: ")
        lim_inf = int(input("Ingrese el límite inferior del Tempo: "))
        lim_sup = int(input("Ingrese el límite superior del Tempo: "))
        n = len(genre.keys()) + 1
        llave = str(n) + "- " + str(genero)
        genre[llave] = (lim_inf, lim_sup)
        print("El género " + str(genero) + " ha sido agregado con éxito!")
        print(genre)
        print('Ésta es la base de datos actualizada:')
        printgenresdict(genre)

    elif int(inputs[0]) == 6:
        print('Éstos son los géneros disponibles para consulta:')
        printgenresdict(genre)
        lista_generos = []
        generos = "1"
        print("Ingrese el número de cada uno de los géneros a consultar.")
        print("Para dejar de agregar géneros a la búsqueda, presione enter.")
        while len(generos) > 0:
            generos = input('~')
            if len(generos) != 0:
                lista_generos.append(generos)
        ranges = controller.getRanges(lista_generos, genre)
        dicc = controller.getEventsByRangeGenres(
            analyzer, 'tempo', genre, lista_generos)
        printgenre(dicc[0])
        printfortotal(analyzer, ranges)
        print(
            "Tiempo [ms]: ",
            f"{dicc[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{dicc[2]:.3f}")

    elif int(inputs[0]) == 7:
        print("Ingrese la hora de inicio en formato 24h: (Ej. 12:34:56)")
        tiempo_inicio = input("~")
        print("Ingrese la hora final en formato 24h: (Ej. 12:34:56)")
        tiempo_final = input("~")
        print(
            "Eventos de escucha entre", tiempo_inicio, 'y', tiempo_final,
            ":", controller.getPlaying(
                    analyzer['created_at'],
                    (tiempo_inicio, tiempo_final)))
        result = controller.getTemposByTime(
            analyzer, tiempo_inicio, tiempo_final)
        bestgenre = controller.getBestGenre(result, genre)
        printTopGenres(bestgenre[0])
        uniqueIDs = controller.getUniqueIDs(
            result, genre, bestgenre[1])
        result2 = controller.getSentimentAnalysis(uniqueIDs, analyzer)
        printtop10tracks(result2[0], bestgenre[1])
        print(
            "Tiempo [ms]: ",
            f"{result2[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result2[2]:.3f}")

    else:
        sys.exit(0)
sys.exit(0)
