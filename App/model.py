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
                'tempo': None
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

    return analyzer


# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    lt.addLast(analyzer['listening_events'], event)
    addEventOnProbingMap(analyzer, event['artist_id'], event['id'], 'artists')
    addEventOnProbingMap(analyzer, event['track_id'], event['id'], 'tracks')
    addEventOnOrderedRBTMap(
        analyzer, float(event['instrumentalness']),
        (event['id'], event['artist_id'], event['track_id']),
        'instrumentalness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['acousticness']),
        (event['id'], event['artist_id'], event['track_id']), 'acousticness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['liveness']),
        (event['id'], event['artist_id'], event['track_id']), 'liveness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['speechiness']),
        (event['id'], event['artist_id'], event['track_id']), 'speechiness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['energy']),
        (event['id'], event['artist_id'], event['track_id']), 'energy')
    addEventOnOrderedRBTMap(
        analyzer, float(event['danceability']),
        (event['id'], event['artist_id'], event['track_id']), 'danceability')
    addEventOnOrderedRBTMap(
        analyzer, float(event['valence']),
        (event['id'], event['artist_id'], event['track_id']), 'valence')
    addEventOnOrderedRBTMap(
        analyzer, float(event['tempo']),
        (event['id'], event['artist_id'], event['track_id']), 'tempo')


# Funciones para agregar un evento a un mapa tipo probing

def addEventOnProbingMap(analyzer, int_input, event, map_key):
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
    selected_map = analyzer[map_key]
    existkey = om.contains(selected_map, int_input)
    if existkey:
        entry = om.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, map_key)
        om.put(selected_map, int_input, value)
    lt.addLast(value['events'], event)


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
    return lt.size(analyzer['listening_events'])


def artistsSize(analyzer):
    return mp.size(analyzer['artists'])


def tracksSize(analyzer):
    return mp.size(analyzer['tracks'])


def getEventsByRange(analyzer, criteria, initial, final):
    lst = om.values(analyzer[criteria], initial, final)
    events = 0
    artists = mp.newMap(maptype='PROBING')
    tracks = mp.newMap(maptype='PROBING')

    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])
        for soundtrackyourtimeline in lt.iterator(lstevents['events']):
            mp.put(artists, soundtrackyourtimeline[1], 1)
            mp.put(tracks, soundtrackyourtimeline[2], 1)

    artists_size = mp.size(artists)
    tracks_size = mp.size(tracks)

    return events, artists_size, tracks_size, artists, tracks


def getTrcForTwoCriteria(analyzer, criteria1range, str1, criteria2range, str2):
    listtracks = mp.newMap(maptype='PROBING')
    listartists = mp.newMap(maptype='PROBING')

    criteria1 = getEventsByRange(
        analyzer, str1, criteria1range[0], criteria1range[1])
    criteria1trackslist = mp.keySet(criteria1[4])
    criteria1artistslist = mp.keySet(criteria1[3])

    criteria2 = getEventsByRange(
        analyzer, str2, criteria2range[0], criteria2range[1])
    criteria2trackslist = mp.keySet(criteria2[4])
    criteria2artistslist = mp.keySet(criteria2[3])

    for key in lt.iterator(criteria1trackslist):
        mp.put(listtracks, key, 1)

    for key in lt.iterator(criteria1artistslist):
        mp.put(listartists, key, 1)

    for key in lt.iterator(criteria2trackslist):
        mp.put(listtracks, key, 1)

    for key in lt.iterator(criteria2artistslist):
        mp.put(listartists, key, 1)

    return (mp.size(listtracks), mp.size(listartists))

# Funciones utilizadas para comparar elementos dentro de una lista


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


# Funciones de ordenamiento
