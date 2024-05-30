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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import threading
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = {
        'model': None
    }
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")

# 7.13 -73.2 1.9 -76.1

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    controller.load_data(control)
    tabla_comercial = lt.newList('ARRAY_LIST')
    tabla_carga = lt.newList('ARRAY_LIST')
    tabla_militar = lt.newList('ARRAY_LIST')
    print('TOTAL DE AEROPUERTOS CARGADOS: ')
    print(lt.size(control['airports']))
    print('TOTAL DE VUELOS CARGADOS: ')
    print(lt.size(control['flights']))
    print(gr.adjacents(control['graph_comercial_distancia'], "ZZZ"))
    comercial, carga, militar, aeropuertos = controller.cinco_primeros(control)
    llaves = ['Nombre del aeropuerto', 'ID ICAO', 'Ciudad del aeropuerto', 'Concurrencia']
    for aero in list(comercial.keys()):
        for aeropuerto in lt.iterator(aeropuertos):
            if aero == aeropuerto['ICAO']:
                dic = {
                    llaves[0] : aeropuerto['NOMBRE'],
                    llaves[1] : aeropuerto['ICAO'],
                    llaves[2] : aeropuerto['CIUDAD'],
                    llaves[3] : comercial[aero]
                }
                lt.addLast(tabla_comercial, dic)
    for aero in list(carga.keys()):
        for aeropuerto in lt.iterator(aeropuertos):
            if aero == aeropuerto['ICAO']:
                dic = {
                    llaves[0] : aeropuerto['NOMBRE'],
                    llaves[1] : aeropuerto['ICAO'],
                    llaves[2] : aeropuerto['CIUDAD'],
                    llaves[3] : carga[aero]
                }
                lt.addLast(tabla_carga, dic)
    for aero in list(militar.keys()):
        for aeropuerto in lt.iterator(aeropuertos):
            if aero == aeropuerto['ICAO']:
                dic = {
                    llaves[0] : aeropuerto['NOMBRE'],
                    llaves[1] : aeropuerto['ICAO'],
                    llaves[2] : aeropuerto['CIUDAD'],
                    llaves[3] : militar[aero]
                }
                lt.addLast(tabla_militar, dic)
    print("TABLA VUELOS COMERCIALES: ")
    print(tabulate(lt.iterator(tabla_comercial), headers="keys", tablefmt="grid"))
    print("TABLA VUELOS DE CARGA: ")
    print(tabulate(lt.iterator(tabla_carga), headers="keys", tablefmt="grid"))
    print("TABLA VUELOS MILITARES: ")
    print(tabulate(lt.iterator(tabla_militar), headers="keys", tablefmt="grid"))

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, origen, destino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    delta_time, res, aero_origen, aero_destino, aeropuertos_visitados, distancia_total, tiempo_total, mapa_aeropuertos = controller.req_1(control, origen, destino)
    respuesta = lt.newList('ARRAY_LIST')
    print('Tiempo de ejecucion: ' + str(delta_time) + ' [ms]')
    if res:
        print('La distancia que ha entre el punto de origen y el destino es: ' + str(distancia_total) + 'KM')
        print('En el camino encontrado se visitaron: ' + str(len(aeropuertos_visitados)) + ' aeropuertos.')
        for aero in aeropuertos_visitados:
            llave_aeropuerto = mp.get(mapa_aeropuertos, aero)
            aeropuerto_visitado = me.getValue(llave_aeropuerto) 
            dic = {
                'Codigo ICAO: ' : aeropuerto_visitado['ICAO'],
                'Nombre del aeropuerto: ' : aeropuerto_visitado['NOMBRE'],
                'Ciudad del aeropuerto: ' : aeropuerto_visitado['CIUDAD'],
                'Pais del aeropuerto: ' : aeropuerto_visitado['PAIS']
            }
            lt.addLast(respuesta, dic)
        print('El trayecto que se tomo fue: ')
        print(tabulate(lt.iterator(respuesta), headers="keys", tablefmt="grid"))
        print('El trayecto demora: ' + str(tiempo_total) + ' minutos')    
    elif res == False:
        print('NO EXISTE CAMINO')
        print('El aeropuerto mas cercano al punto de origen es: ' + str(aero_origen))
        print('El aeropuerto mas cercano al punto de destino es: ' + str(aero_destino))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    delta_time, llave_primer, distancia_total, trayectos = controller.req_3(control)
    print('Tiempo de ejecucion: ' + str(delta_time) + ' [ms]')
    nombre_aero = me.getValue(llave_primer)
    tabla_primero = {
        'ICAO' : nombre_aero['ICAO'],
        'Nombre del aeropuerto' : nombre_aero['NOMBRE'],
        'Ciudad del aeropuerto' : nombre_aero['CIUDAD'],
        'Pais del aeropuerto' : nombre_aero["PAIS"],
        'Concurrencia' : control['concurrencia']['COMERCIAL'][nombre_aero['ICAO']]
    }
    imprimir_primero = lt.newList('ARRAY_LIST')
    lt.addLast(imprimir_primero, tabla_primero)
    print('El aeropuerto mas importante es: ')
    print(tabulate(lt.iterator(imprimir_primero), headers="keys", tablefmt="grid"))
    print('La suma de la distancia total fue de: ' + str(distancia_total) + ' Km')
    print('El numero total de trayectos calculados fue: ' + str(lt.size(trayectos)))
    print('Los trayectos calculados fueron: ')
    for trayecto in lt.iterator(trayectos):
        print('Aeropuerto de origen: ')
        tabla_origen = {
        'ICAO' : trayecto['aeropuerto_origen']['ICAO'],
        'Nombre del aeropuerto' : trayecto['aeropuerto_origen']['NOMBRE'],
        'Ciudad del aeropuerto' : trayecto['aeropuerto_origen']['CIUDAD'],
        'Pais del aeropuerto' : trayecto['aeropuerto_origen']["PAIS"]
             }    
        imprimir_origen = lt.newList('ARRAY_LIST')
        lt.addLast(imprimir_origen, tabla_origen)
        print(tabulate(lt.iterator(imprimir_origen), headers="keys", tablefmt="grid"))
        print('Aeropuerto de destino: ')
        tabla_destino = {
        'ICAO' : trayecto['aeropuerto_destino']['ICAO'],
        'Nombre del aeropuerto' : trayecto['aeropuerto_destino']['NOMBRE'],
        'Ciudad del aeropuerto' : trayecto['aeropuerto_destino']['CIUDAD'],
        'Pais del aeropuerto' : trayecto['aeropuerto_destino']["PAIS"]
             }
        imprimir_destino = lt.newList('ARRAY_LIST')
        lt.addLast(imprimir_destino, tabla_destino)
        print(tabulate(lt.iterator(imprimir_destino), headers="keys", tablefmt="grid"))
        print('La distancia recorrida en el trayecto fue: ' + str(trayecto['distancia_trayecto']) + ' Km')
        print('El tiempo que tarda en recorrer el trayecto fue: ' + str(trayecto['tiempo_trayecto']) + 'Min')

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    delta_time, llave_primer, distancia_total, trayectos = controller.req_4(control)
    nombre_aero = me.getValue(llave_primer)
    tabla_primero = {
        'ICAO' : nombre_aero['ICAO'],
        'Nombre del aeropuerto' : nombre_aero['NOMBRE'],
        'Ciudad del aeropuerto' : nombre_aero['CIUDAD'],
        'Pais del aeropuerto' : nombre_aero["PAIS"],
        'Concurrencia' : control['concurrencia']['CARGA'][nombre_aero['ICAO']]
    }
    imprimir_primero = lt.newList('ARRAY_LIST')
    lt.addLast(imprimir_primero, tabla_primero)
    for trayecto in lt.iterator(trayectos):
        print('Aeropuerto de origen: ')
        tabla_origen = {
        'ICAO' : trayecto['aeropuerto_origen']['ICAO'],
        'Nombre del aeropuerto' : trayecto['aeropuerto_origen']['NOMBRE'],
        'Ciudad del aeropuerto' : trayecto['aeropuerto_origen']['CIUDAD'],
        'Pais del aeropuerto' : trayecto['aeropuerto_origen']["PAIS"]
             }    
        imprimir_origen = lt.newList('ARRAY_LIST')
        lt.addLast(imprimir_origen, tabla_origen)
        print(tabulate(lt.iterator(imprimir_origen), headers="keys", tablefmt="grid"))
        print('Aeropuerto de destino: ')
        tabla_destino = {
        'ICAO' : trayecto['aeropuerto_destino']['ICAO'],
        'Nombre del aeropuerto' : trayecto['aeropuerto_destino']['NOMBRE'],
        'Ciudad del aeropuerto' : trayecto['aeropuerto_destino']['CIUDAD'],
        'Pais del aeropuerto' : trayecto['aeropuerto_destino']["PAIS"]
             }
        imprimir_destino = lt.newList('ARRAY_LIST')
        lt.addLast(imprimir_destino, tabla_destino)
        print(tabulate(lt.iterator(imprimir_destino), headers="keys", tablefmt="grid"))
        print('La distancia recorrida en el trayecto fue: ' + str(trayecto['distancia_trayecto']) + ' Km')
        print('El tiempo que tarda en recorrer el trayecto fue: ' + str(trayecto['tiempo_trayecto']) + ' Min')
        print('Los tipos de aeronave del trayecto son: ' + str(trayecto['lista_aviones']))
    print('Estos son los trayectos calculados: ')
    print('El aeropuerto mas importante es: ')
    print(tabulate(lt.iterator(imprimir_primero), headers="keys", tablefmt="grid"))
    print('La suma de la distancia total fue de: ' + str(distancia_total) + ' Km')
    print('El numero total de trayectos calculados fue: ' + str(lt.size(trayectos)))
    print('Tiempo de ejecucion: ' + str(delta_time) + ' [ms]')
    


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control, n_aeropuertos):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    delta_time, llave_primer, respuesta = controller.req_6(control, n_aeropuertos)
    print('Tiempo de ejecucion: ' + str(delta_time) + ' [ms]')
    nombre_aero = me.getValue(llave_primer)
    tabla_primero = {
        'ICAO' : nombre_aero['ICAO'],
        'Nombre del aeropuerto' : nombre_aero['NOMBRE'],
        'Ciudad del aeropuerto' : nombre_aero['CIUDAD'],
        'Pais del aeropuerto' : nombre_aero["PAIS"],
        'Concurrencia' : control['concurrencia']['COMERCIAL'][nombre_aero['ICAO']]
    }
    imprimir_primero = lt.newList('ARRAY_LIST')
    lt.addLast(imprimir_primero, tabla_primero)
    print('El aeropuerto con mayor concurrencia es: ')
    print(tabulate(lt.iterator(imprimir_primero), headers="keys", tablefmt="grid"))
    for trayecto in lt.iterator(respuesta):
        print('EL total de aeropuertos del camino es: ' + str(trayecto['total_aeropuertos']))
        print('Los aeropuertos incluidos en el camino son: ')
        print(tabulate(lt.iterator(trayecto['lista_aeropuertos']), headers="keys", tablefmt="grid"))
        print(tabulate(lt.iterator(trayecto['lista_vuelos']), headers="keys", tablefmt="grid"))
        print('La distancia total del camino es: ' + str(trayecto['distancia_trayecto']) + ' Km')
        
        
def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
def menu_cycle():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            control = new_controller()
            load_data(control)
            
            
            
            
        elif int(inputs) == 2:
            lat_origen = float(input('INGRESE LA LATITUD DE ORIGEN: '))
            long_origen = float(input('INGRESE LA LONGITUD DE ORIGEN: '))
            lat_destino = float(input('INGRESE LA LATITUD DE DESTINO: '))
            long_destino = float(input('INGRESE LA LONGITUD DE DESTINO: '))
            origen = (lat_origen, long_origen)
            destino = (lat_destino, long_destino)
            print_req_1(control, origen, destino)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            n_aeropuertos = int(input('INGRESE LA CANTIDAD N DE AEROPUERTOS MAS IMPORTANTES: '))
            print_req_6(control, n_aeropuertos)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864*2)
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle)
    thread.start()
