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
import time
import csv
import tracemalloc
from DISClib.ADT import map as mp

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.new_data_structs()
    return control


# Funciones para la carga de datos


def load_data(control):
    load_airports(control)
    load_flights(control)
    return None


def load_airports(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    filename = cf.data_dir + 'airports-2022.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'), delimiter=';')
    for airport in input_file:
        model.add_airports(control, airport)
    return None

def load_flights(control):
    filename = cf.data_dir + 'fligths-2022.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'), delimiter=';')
    for flight in input_file:
        model.add_flights(control, flight)
        model.add_vuelos(control, flight)
    
    
    return None
    
        
def cinco_primeros(control):
    comercial, carga, militar, aeropuertos = model.cinco_primeros(control)
    return comercial, carga, militar, aeropuertos       

def componentes(control):
    componentes, numero = model.componentes(control)
    return componentes, numero
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, origen, destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = getTime()
    res, aero_origen, aero_destino, aeropuertos_visitados, distancia_total, tiempo_total, mapa_aeropuertos  = model.req_1(control, origen, destino)
    stop_time = getTime()
    delta_time = deltaTime(start_time, stop_time)
    return delta_time, res, aero_origen, aero_destino, aeropuertos_visitados, distancia_total, tiempo_total, mapa_aeropuertos 


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = getTime()
    llave_primer, distancia_total, trayectos = model.req_3(control)
    stop_time = getTime()
    delta_time = deltaTime(start_time, stop_time)
    return delta_time, llave_primer, distancia_total, trayectos


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = getTime()
    llave_primer, distancia_total, trayectos = model.req_4(control)
    stop_time = getTime()
    delta_time = deltaTime(start_time, stop_time)
    return delta_time, llave_primer, distancia_total, trayectos


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, n_aeropuertos):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = getTime()
    llave_primer, respuesta = model.req_6(control, n_aeropuertos)
    stop_time = getTime()
    delta_time = deltaTime(start_time, stop_time)
    return delta_time, llave_primer, respuesta

def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
