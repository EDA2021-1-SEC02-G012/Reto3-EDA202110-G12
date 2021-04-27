"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 * Jose Luis Tavera Ruiz
 * Juan Diego Yepes
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf


# Construccion de modelos


def newAnalyzer():
    """ Inicializa el analizador

    Retorna el analizador inicializado.
    """
    analyzer = {'listening_events': None,
                'artists': None,
                'tracks': None,
                'instrumentalness': None,
                'acousticness': None,
                'liveness': None,
                'speechiness': None,
                'energy': None,
                'danceability': None,
                'valence': None,
                'tempo': None,
                'created_at': None,
                'hashtags': None,
                'vaders': None
                }

    analyzer['listening_events'] = lt.newList(datastructure='ARRAY_LIST')
    analyzer['artists'] = mp.newMap(maptype='PROBING')
    analyzer['tracks'] = mp.newMap(maptype='PROBING')
    analyzer['instrumentalness'] = om.newMap(omaptype='RBT')
    analyzer['acousticness'] = om.newMap(omaptype='RBT')
    analyzer['liveness'] = om.newMap(omaptype='RBT')
    analyzer['speechiness'] = om.newMap(omaptype='RBT')
    analyzer['energy'] = om.newMap(omaptype='RBT')
    analyzer['danceability'] = om.newMap(omaptype='RBT')
    analyzer['valence'] = om.newMap(omaptype='RBT')
    analyzer['tempo'] = om.newMap(omaptype='RBT')
    analyzer['created_at'] = om.newMap(omaptype='RBT')
    analyzer['hashtags'] = mp.newMap(maptype='PROBING')
    analyzer['vaders'] = mp.newMap(maptype='PROBING')

    return analyzer


# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    '''
    Agrega individualmente el evento al analyzer, en
    cada uno de sus mapas
    '''
    lt.addLast(analyzer['listening_events'], event)
    addEventOnProbingMap(analyzer, event['artist_id'], event['id'], 'artists')
    addEventOnProbingMap(analyzer, event['track_id'], event['id'], 'tracks')
    addEventOnOrderedRBTMap(
        analyzer, float(event['instrumentalness']),
        event,
        'instrumentalness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['acousticness']),
        event, 'acousticness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['liveness']),
        event, 'liveness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['speechiness']),
        event, 'speechiness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['energy']),
        event, 'energy')
    addEventOnOrderedRBTMap(
        analyzer, float(event['danceability']),
        event, 'danceability')
    addEventOnOrderedRBTMap(
        analyzer, float(event['valence']),
        event, 'valence')
    addEventOnOrderedRBTMap(
        analyzer, float(event['tempo']),
        event, 'tempo')
    addTimedEvent(
        analyzer, event['created_at'], event, 'created_at')


def addOnMap(analyzer, event, key, map_name):
    '''
    Agrega los hashtags y los vaders a sus mapas individuales
    '''
    mp.put(analyzer[map_name], key, event)


def addEventOnProbingMap(analyzer, int_input, event, map_key):
    """
    La función de addEventOnProbingMap() adiciona el video al mapa
    tipo PROBING que se ha seleccionado.
    Args:
        analyzer: Analizador de eventos
        int_input: Llave a analizar
        video: Video a añadir
        map_key: Especifica cuál mapa
    """
    selected_map = analyzer[map_key]
    existkey = mp.contains(selected_map, int_input)
    if existkey:
        entry = mp.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, map_key)
        mp.put(selected_map, int_input, value)
    lt.addLast(value['events'], event)


def addEventOnOrderedRBTMap(analyzer, int_input, event, map_key):
    """
    La función de addEventOnOrderedRBTMap() adiciona el video al árbol
    tipo RBT que se ha seleccionado.
    Args:
        analyzer: Analizador de eventos
        int_input: Llave a analizar
        video: Video a añadir
        map_key: Especifica cuál mapa
    """
    selected_map = analyzer[map_key]
    existkey = om.contains(selected_map, int_input)
    if existkey:
        entry = om.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, map_key)
        om.put(selected_map, int_input, value)
    lt.addLast(value['events'], event)


def addTimedEvent(analyzer, int_input, event, map_key):
    '''
    Adiciona un evento a un árbol tipo RBT usando el
    tiempo de creación del evento, con los segundos como
    llave
    '''
    time = int_input.split(" ")
    time = time[1].split(':')
    time = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    addEventOnOrderedRBTMap(
        analyzer, time,
        event, map_key)


def newSeparator(key, classifier):
    """
    La función de newSeparator() crea una nueva estructura
    para modelar los mapas.
    Args:
        key: Llave del mapa
        classifier: Especifica cuál mapa
    """
    separator = {classifier: "", "events": None}
    separator[classifier] = key
    separator['events'] = lt.newList('ARRAY_LIST', None)
    return separator


# Funciones de consulta

def eventsSize(analyzer):
    '''
    Retorna el tamaño de la lista de eventos
    '''
    return lt.size(analyzer['listening_events'])


def artistsSize(analyzer):
    '''
    Retorna el tamaño del mapa de artistas,
    para saber los artistas únicos cargados
    '''
    return mp.size(analyzer['artists'])


def tracksSize(analyzer):
    '''
    Retorna el tamaño del mapa de tracks, para
    saber los tracks únicos cargados
    '''
    return mp.size(analyzer['tracks'])


def getEventsByRange(analyzer, criteria, initial, final):
    '''
    Retorna los varias características de los
    eventos dado un criterio y rango en el mismo,
    buscándolos en un árbol
    Args:
        analyzer: Analizador de eventos
        criteria: Llave del analyzer a analizar
        initial: Inicio del rango
        final: Fin del rango
    '''
    lst = om.values(analyzer[criteria], initial, final)
    events = 0
    artists = mp.newMap(maptype='PROBING')
    tracks = mp.newMap(maptype='PROBING')

    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])
        for soundtrackyourtimeline in lt.iterator(lstevents['events']):
            mp.put(artists, soundtrackyourtimeline['artist_id'], 1)
            mp.put(tracks, soundtrackyourtimeline['track_id'], 1)

    artists_size = mp.size(artists)
    tracks_size = mp.size(tracks)

    return events, artists_size, tracks_size, artists, tracks


def getEventsByRangeTempoReturn(analyzer, criteria, initial, final):
    '''
    Retorna el tempo de los eventos organizados en un arbol RBT
    dado un criterio y rango en el mismo,
    buscándolos en un árbol
    Args:
        analyzer: Analizador de eventos
        criteria: Llave del analyzer a analizar
        initial: Inicio del rango
        final: Fin del rango
    '''
    lst = om.values(analyzer[criteria], initial, final)
    minimap = {'tempo_map': None}
    minimap['tempo_map'] = om.newMap(omaptype='RBT')

    for lstevents in lt.iterator(lst):
        for soundtrackyourtimeline in lt.iterator(lstevents['events']):
            addEventOnOrderedRBTMap(
                minimap,
                float(soundtrackyourtimeline['tempo']),
                soundtrackyourtimeline, 'tempo_map')

    return minimap


def getTotalEventsByRangeGenre(analyzer, criteria, initial, final):
    '''
    Retorna la suma de los eventos dentro de un rango específico
    Args:
        analyzer: Analizador de eventos
        criteria: Llave del analyzer a analizar
        initial: Inicio del rango
        final: Fin del rango
    '''
    lst = om.values(analyzer[criteria], initial, final)
    events = 0

    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])

    return events


def getEventsByRangeGenres(analyzer, criteria, dicc, lista):
    '''
    Retorna un diccionario con llave los géneros y valores lel número de
    eventos individuales de escucha de cada género
    Args:
        analyzer: Analizador de eventos
        criteria: Llave del analyzer a analizar
        dicc: Diccionario con los géneros y los rangos
        lista: Lista de los rangos
    '''
    resultado = {}
    llaves = []
    for llave in dicc:
        llaves.append(llave[0])
    for i in lista:
        for llave in dicc:
            if i in llave:
                lim = dicc[llave]
                lim_inf = lim[0]
                lim_sup = lim[1]
                result = getEventsByRange(analyzer, criteria, lim_inf, lim_sup)
                resultado[llave] = result

    return resultado


def getTrcForTwoCriteria(analyzer, criteria1range, str1, criteria2range, str2):
    '''
    Retorna los varias características de los
    eventos dado dos criterios y rangos en el mismo,
    buscándolos en ambos árboles. El retorno son los eventos
    que cumplen con ambas características
    Args:
        analyzer: Analizador de eventos
        criteria1range: Rango del criterio 1
        str1: Llave del analyzer del criterio 1
        criteria2range: Rango del criterio 2
        str2: Llave del analyzer del criterio 2
    '''
    criteria1 = om.values(analyzer[str1], criteria1range[0], criteria1range[1])
    submap = {'events': None}
    submap[str2] = om.newMap(omaptype='RBT')
    for eventO in lt.iterator(criteria1):
        for event0 in lt.iterator(eventO['events']):
            addEventOnOrderedRBTMap(submap, float(event0[str2]), event0, str2)
    result = om.values(submap[str2], criteria2range[0], criteria2range[1])
    artists = mp.newMap(maptype='PROBING')
    tracks = mp.newMap(maptype='PROBING')
    for event1 in lt.iterator(result):
        for eventi in lt.iterator(event1['events']):
            mp.put(artists, eventi['artist_id'], 1)
            mp.put(
                tracks, eventi['track_id'],
                (eventi[str1], eventi[str2]))
    return (mp.size(artists), mp.size(tracks), tracks)


def getRanges(lista_generos, dicc):
    '''
    Retorna los rangos dados los géneros
    '''
    llaves = []
    lim_inf = 1000
    lim_sup = 0

    for llave in dicc:
        llaves.append(llave[0])
    for i in lista_generos:
        for llave in dicc:
            if i in llave:
                lim = dicc[llave]
                if lim[0] <= lim_inf:
                    lim_inf = lim[0]
                if lim[1] >= lim_sup:
                    lim_sup = lim[1]

    ranges = []
    n = 0
    while n < lim_sup:
        ranges.append(0)
        n += 1

    for x in lista_generos:
        for llave in dicc:
            if x in llave:
                lim = dicc[llave]
                h = lim[0]
                while h < lim[1]:
                    ranges[h] = 1
                    h += 1

    ranges.append(0)
    resultados = []

    for pos in range(0, len(ranges)):
        if ranges[pos] == 1 and ranges[pos-1] == 0:
            inferior = pos
        elif ranges[pos] == 1 and ranges[pos+1] == 0:
            superior = pos + 1
            resultados.append((inferior, superior))

    return resultados


def getTemposByTime(analyzer, tiempo_inicio, tiempo_final):
    '''
    Retorna los eventos dados los tiempos al usar la
    funcion getEventsByRangeTempoReturn()
    '''
    realstarttime = tiempo_inicio.split(':')
    realstarttime = (
        int(realstarttime[0])*3600 + int(realstarttime[1])*60
        + int(realstarttime[2]))
    realfinishtime = tiempo_final.split(':')
    realfinishtime = (
        int(realfinishtime[0])*3600 + int(realfinishtime[1])*60
        + int(realfinishtime[2]))
    return getEventsByRangeTempoReturn(
        analyzer, 'created_at', realstarttime, realfinishtime)


def getBestGenre(minimap, genredicc):
    '''
    Retorna un diccionario con el top de
    los géneros dadas las repeticiones
    '''
    asqueroso_top = {}
    bestgenre = None
    mayor = 0
    for genre in genredicc:
        lim = genredicc[genre]
        events = getTotalEventsByRangeGenre(
            minimap, 'tempo_map', lim[0], lim[1])
        asqueroso_top[genre] = events
        if events > mayor:
            mayor = events
            bestgenre = genre

    return asqueroso_top, bestgenre


def getUniqueIDs(minimap, generos, bestgenre):
    '''
    Retorna los eventos únicos dada la llave concatenada
    '''
    lim = generos[bestgenre]
    lst = om.values(minimap['tempo_map'], lim[0], lim[1])
    tracks = {'data': None}
    tracks['data'] = mp.newMap(maptype='PROBING')
    events = 0

    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])
        for soundtrackyourtimeline in lt.iterator(lstevents['events']):
            unique_id = (
                soundtrackyourtimeline['user_id']
                + soundtrackyourtimeline['track_id']
                + soundtrackyourtimeline['created_at'])
            addEventOnProbingMap(
                tracks, soundtrackyourtimeline['track_id'], unique_id, 'data')

    tracks_size = mp.size(tracks['data'])

    return tracks['data'], tracks_size, events


def getSentimentAnalysis(unique_ids, analyzer):
    '''
    Retorna los eventos que tienen un hashtag
    determinado dada la llave concatenada
    '''
    hashtags = analyzer['hashtags']
    vaders = analyzer['vaders']
    llaves = mp.keySet(unique_ids[0])
    tracks = mp.newMap(maptype="PROBING")
    for llave in lt.iterator(llaves):
        ids = mp.get(unique_ids[0], llave)
        vaderavg = 0
        lista = me.getValue(ids)
        for each_id in lt.iterator(lista['events']):
            hashtag = mp.get(hashtags, each_id)
            hashtag_value = me.getValue(hashtag)
            vader = mp.get(vaders, hashtag_value.lower())
            # Santiago no puso lower :)
            if (vader is not None):
                vader_val = me.getValue(vader)
                if (vader_val is not None) and (vader_val != ''):
                    vaderavg += float(vader_val)

        if vaderavg != 0.0:
            listaX = me.getValue(ids)
            n = lt.size(listaX['events'])
            vaderavg = vaderavg/n
            mp.put(tracks, llave, vaderavg)

    return tracks
