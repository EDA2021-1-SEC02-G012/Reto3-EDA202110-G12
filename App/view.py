"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

analyzer = None
events_analysis_file = 'context_content_features-5pct.csv'


def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información en el catálogo")


def printfirstandlast5(arraylist):
    printlist = arraylist['listening_events']
    i = 1
    listsize = lt.size(printlist)
    while i <= 5:
        print(lt.getElement(printlist, i))
        i += 1
    i = listsize
    while i > (listsize - 5):
        print(lt.getElement(printlist, (listsize - i)))
        i -= 1


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        analysis_file = 'context_content_features-5.csv'
        analyzer = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(analyzer, events_analysis_file)
        print('Registro de eventos Cargados: ' + str(controller.eventsSize(
            analyzer)))
        print('Artistas únicos Cargados: ' + str(controller.artistsSize(
            analyzer)))
        print('Pistas únicas Cargados: ' + str(controller.tracksSize(
            analyzer)))
        printfirstandlast5(analyzer)

    elif int(inputs[0]) == 3:
        pass

    else:
        sys.exit(0)
sys.exit(0)
