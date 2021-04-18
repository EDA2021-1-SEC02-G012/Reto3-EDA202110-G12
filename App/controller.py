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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


'''
def info_chooser(subsample):
    try:
        sentiment_values = 'sentiment_values.csv'  # Always the same

        if subsample == 1:
            sample_folder = 'subsample-5pct'
            events_analysis_file = 'context_content_features-5.csv'
        elif subsample == 2:
            sample_folder = 'subsample-10pct'
            events_analysis_file = 'context_content_features-10.csv'
        elif subsample == 3:
            sample_folder = 'subsample-20pct'
            events_analysis_file = 'context_content_features-20.csv'
        elif subsample == 4:
            sample_folder = 'subsample-30pct'
            events_analysis_file = 'context_content_features-30.csv'
        elif subsample == 5:
            sample_folder = 'subsample-50pct'
            events_analysis_file = 'context_content_features-50.csv'
        elif subsample == 6:
            sample_folder = 'subsample-80pct'
            events_analysis_file = 'context_content_features-80.csv'
        elif subsample == 7:
            sample_folder = 'subsample-large'
            events_analysis_file = 'context_content_features-80.csv'
        elif subsample == 8:
            sample_folder = 'subsample-small'
            events_analysis_file = 'context_content_features-small.csv'

        route = sample_folder + '/' + events_analysis_file

    except:
        print("No se ha seleccionado un directorio válido.")
'''

# Inicialización del Catálogo


def loadData(analyzer, file):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    analysis_file = cf.data_dir + file
    input_file = csv.DictReader(open(analysis_file, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.addEvent(analyzer, event)
    return analyzer

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el analyzer


def eventsSize(analyzer):
    """
    Número de eventos cargados
    """
    return model.eventsSize(analyzer)


def artistsSize(analyzer):
    """
    Número de artistas únicos
    """
    return model.artistsSize(analyzer)


def tracksSize(analyzer):
    """
    Número de pistas únicas
    """
    return model.tracksSize(analyzer)
