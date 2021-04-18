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
from DISClib.Algorithms.Sorting import shellsort as sa
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
    addEventOnMap(analyzer, event['artist_id'], event['id'], 'artists')
    addEventOnMap(analyzer, event['track_id'], event['id'], 'tracks')


def addEventOnMap(catalog, int_input, event, catalog_key):
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

# Funciones para creacion de datos

# Funciones de consulta


def eventsSize(analyzer):
    return lt.size(analyzer['listening_events'])


def artistsSize(analyzer):
    return mp.size(analyzer['artists'])


def tracksSize(analyzer):
    return mp.size(analyzer['tracks'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
