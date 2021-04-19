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
from DISClib.Algorithms.Sorting import shellsort as sa  # TODO ask why
import datetime
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
                'valence': None
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
    analyzer['listening_time'] = om.newMap(omaptype='RBT')

    return analyzer


# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    lt.addLast(analyzer['listening_events'], event)
    addEventOnProbingMap(analyzer, event['artist_id'], event['id'], 'artists')
    addEventOnProbingMap(analyzer, event['track_id'], event['id'], 'tracks')
    addEventOnOrderedRBTMap(
        analyzer, event['instrumentalness'], event['id'], 'instrumentalness')


# Funciones para agregar un evento a un mapa tipo probing

def addEventOnProbingMap(catalog, int_input, event, catalog_key):
    selected_map = catalog[catalog_key]
    existkey = mp.contains(selected_map, int_input)
    if existkey:
        entry = mp.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, catalog_key)
        mp.put(selected_map, int_input, value)
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


# Agregar información a un mapa tipo RBT


def addEventOnOrderedRBTMap(catalog, int_input, event, catalog_key):
    selected_map = catalog[catalog_key]
    existkey = om.contains(selected_map, int_input)
    if existkey:
        entry = om.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, catalog_key)
        om.put(selected_map, int_input, value)
    lt.addLast(value['events'], event)

'''
def updateDateIndex(map, event):
    """
    Se toma la fecha del evento y se busca si ya existe en el arbol
    dicha fecha.
    """
    occurreddate = event['created_at']
    eventdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, eventdate.date())
    if entry is None:
        datentry = newDataEntry(event)
        om.put(map, eventdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, event)
    return map


def newDataEntry(event):  # TODO Cambiar nombres de índices
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = mp.newMap(
        numelements=30,
        maptype='PROBING',
        comparefunction=compareOffenses)
    entry['lstcrimes'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def addDateIndex(datentry, event):  # TODO Revisar cómo agrupar
    lst = datentry['lstcrimes']
    lt.addLast(lst, event)
    offenseIndex = datentry['offenseIndex']
    offentry = mp.get(offenseIndex, event['OFFENSE_CODE_GROUP'])
    if (offentry is None):
        entry = newOffenseEntry(event['OFFENSE_CODE_GROUP'], event)
        lt.addLast(entry['lstoffenses'], event)
        mp.put(offenseIndex, event['OFFENSE_CODE_GROUP'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], event)
    return datentry


def newOffenseEntry(offensegrp, event):  # TODO Cambiar nombre
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry
'''

# Funciones para creacion de datos


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
    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])
    return events


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


def compareOffenses(offense1, offense2):  # TODO Change name
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

# Funciones de ordenamiento
