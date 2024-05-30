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

import folium
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
import math 
from haversine import haversine
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {
        'airports':None,
        'dic_airports': mp.newMap(numelements=2000,
                                              maptype='PROBING'),
        'flights': None,
        'graph_time':gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_time' : None,  
        'graph_distancia' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_distancia' : None,
        'graph_comercial_time' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_comercial_time' : None,
        'graph_comercial_distancia' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_comercial_distancia' : None,
        'graph_carga_time' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_carga_time' : None,
        'graph_carga_distancia' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_carga_distancia' : None,
        'graph_militar_time' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_militar_time' : None,
        'graph_militar_distancia' : gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2000),
        'caminos_militar_distancia' : None,
        'mapa_conexiones_aeropuertos' : None,
        'coords' : {},
        'concurrencia': {},
        'mapa_aeropuertos': mp.newMap(numelements=2000,
                                     maptype='PROBING')
    }
    data_structs['airports'] = lt.newList('ARRAY_LIST')
    data_structs['flights'] = lt.newList('ARRAY_LIST')
    data_structs['mapa_conexiones_aeropuertos'] = mp.newMap(numelements=2000,
                                              maptype='PROBING')
    
    return data_structs


# Funciones para agregar informacion al modelo
def add_airports(data_structs, data):
    lt.addLast(data_structs['airports'], data)
    mp.put(data_structs['mapa_aeropuertos'], data['ICAO'], data)
    latitud = (data['LATITUD'])
    longitud = (data['LONGITUD'])
    dupla_l = latitud.replace(",", ".")
    dupla_lg = longitud.replace(',', '.')
    data_structs['coords'][data['ICAO']] = (float(dupla_l), float(dupla_lg))
    return None

def add_flights(data_structs, data):
    if not gr.containsVertex(data_structs['graph_time'], data['ORIGEN']):
        gr.insertVertex(data_structs['graph_time'], data['ORIGEN'])
        if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_time'], data['ORIGEN'])
        elif data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_time'], data['ORIGEN'])           
        elif data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_time'], data['ORIGEN'])
    elif gr.containsVertex(data_structs['graph_time'], data['ORIGEN']):
        if not gr.containsVertex(data_structs['graph_comercial_time'], data['ORIGEN']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_time'], data['ORIGEN'])
        elif not gr.containsVertex(data_structs['graph_carga_time'], data['ORIGEN']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_time'], data['ORIGEN'])           
        elif not gr.containsVertex(data_structs['graph_militar_time'], data['ORIGEN']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_time'], data['ORIGEN'])
        
                
    if not gr.containsVertex(data_structs['graph_time'], data['DESTINO']):
        gr.insertVertex(data_structs['graph_time'], data['DESTINO'])
        if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_time'], data['DESTINO'])
            gr.addEdge(data_structs['graph_comercial_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        if data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_time'], data['DESTINO'])           
            gr.addEdge(data_structs['graph_carga_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        if data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_time'], data['DESTINO'])
            gr.addEdge(data_structs['graph_militar_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
    elif gr.containsVertex(data_structs['graph_time'], data['DESTINO']):
        if not gr.containsVertex(data_structs['graph_comercial_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_time'], data['DESTINO'])
            gr.addEdge(data_structs['graph_comercial_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))  
        elif gr.containsVertex(data_structs['graph_comercial_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.addEdge(data_structs['graph_comercial_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        
        if not gr.containsVertex(data_structs['graph_carga_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_time'], data['DESTINO'])           
            gr.addEdge(data_structs['graph_carga_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        elif gr.containsVertex(data_structs['graph_carga_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.addEdge(data_structs['graph_carga_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        
        if not gr.containsVertex(data_structs['graph_militar_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_time'], data['DESTINO'])    
            gr.addEdge(data_structs['graph_militar_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
        elif gr.containsVertex(data_structs['graph_militar_time'], data['DESTINO']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.addEdge(data_structs['graph_militar_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))
               
    gr.addEdge(data_structs['graph_time'], data['ORIGEN'], data['DESTINO'], int(data['TIEMPO_VUELO']))     
           
        

    
    
    if not gr.containsVertex(data_structs['graph_distancia'], data['ORIGEN']):
        gr.insertVertex(data_structs['graph_distancia'], data['ORIGEN'])
        if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_distancia'], data['ORIGEN'])
        if data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_distancia'], data['ORIGEN'])           
        if data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_distancia'], data['ORIGEN'])
    elif gr.containsVertex(data_structs['graph_distancia'], data['ORIGEN']):
        if not gr.containsVertex(data_structs['graph_comercial_distancia'], data['ORIGEN']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_distancia'], data['ORIGEN'])
        if not gr.containsVertex(data_structs['graph_carga_distancia'], data['ORIGEN']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_distancia'], data['ORIGEN'])           
        if not gr.containsVertex(data_structs['graph_militar_distancia'], data['ORIGEN']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_distancia'], data['ORIGEN'])
    
    distancia = haversine((data_structs['coords'][data['ORIGEN']]), (data_structs['coords'][data['DESTINO']]))
    
    if not gr.containsVertex(data_structs['graph_distancia'], data['DESTINO']):
        gr.insertVertex(data_structs['graph_distancia'], data['DESTINO'])
        if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_distancia'], data['DESTINO'])
            gr.addEdge(data_structs['graph_comercial_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        if data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_distancia'], data['DESTINO'])           
            gr.addEdge(data_structs['graph_carga_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        if data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_distancia'], data['DESTINO'])
            gr.addEdge(data_structs['graph_militar_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
    
    elif gr.containsVertex(data_structs['graph_distancia'], data['DESTINO']):
        if not gr.containsVertex(data_structs['graph_comercial_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.insertVertex(data_structs['graph_comercial_distancia'], data['DESTINO'])
            gr.addEdge(data_structs['graph_comercial_distancia'], data['ORIGEN'], data['DESTINO'], distancia)  
        elif gr.containsVertex(data_structs['graph_comercial_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            gr.addEdge(data_structs['graph_comercial_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        
        if not gr.containsVertex(data_structs['graph_carga_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.insertVertex(data_structs['graph_carga_distancia'], data['DESTINO'])           
            gr.addEdge(data_structs['graph_carga_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        elif gr.containsVertex(data_structs['graph_carga_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'AVIACION_CARGA':
            gr.addEdge(data_structs['graph_carga_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        
        if not gr.containsVertex(data_structs['graph_militar_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.insertVertex(data_structs['graph_militar_distancia'], data['DESTINO'])    
            gr.addEdge(data_structs['graph_militar_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
        elif gr.containsVertex(data_structs['graph_militar_distancia'], data['DESTINO']) and data['TIPO_VUELO'] == 'MILITAR':
            gr.addEdge(data_structs['graph_militar_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
               
    
    
    
    
    gr.addEdge(data_structs['graph_distancia'], data['ORIGEN'], data['DESTINO'], distancia)
    
    
    aeropuerto = mp.get(data_structs['mapa_conexiones_aeropuertos'], data['ORIGEN'])
    
    if aeropuerto is None:
        vuelos = lt.newList('ARRAY_LIST')
        lt.addLast(vuelos, data)
        mp.put(data_structs['mapa_conexiones_aeropuertos'], data['ORIGEN'], vuelos)
    elif aeropuerto != None:
        llave_vuelos = mp.get(data_structs['mapa_conexiones_aeropuertos'], data['ORIGEN'])
        vuelos = me.getValue(llave_vuelos)
        lt.addLast(vuelos, data)
        mp.put(data_structs['mapa_conexiones_aeropuertos'], data['ORIGEN'], vuelos)     
    return None
    
def add_vuelos(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['flights'], data)
    return None 

def cinco_primeros(data_structs):
    res = {"COMERCIAL": {},
           'CARGA' : {},
           'MILITAR' : {}}
    vuelos = data_structs['flights']
    for vuelo in lt.iterator(vuelos):
        if vuelo["TIPO_VUELO"] == 'AVIACION_COMERCIAL':
            if vuelo['ORIGEN'] not in list(res['COMERCIAL'].keys()):
                res['COMERCIAL'][vuelo['ORIGEN']] = 1
            elif vuelo['ORIGEN'] in list(res['COMERCIAL']):
                res['COMERCIAL'][vuelo['ORIGEN']] += 1
            if vuelo['DESTINO'] not in list(res['COMERCIAL'].keys()):
                res['COMERCIAL'][vuelo['DESTINO']] = 1
            elif vuelo['DESTINO'] in list(res['COMERCIAL']):
                res['COMERCIAL'][vuelo['DESTINO']] += 1
        if vuelo["TIPO_VUELO"] == 'AVIACION_CARGA':
            if vuelo['ORIGEN'] not in list(res['CARGA'].keys()):
                res['CARGA'][vuelo['ORIGEN']] = 1
            elif vuelo['ORIGEN'] in list(res['CARGA']):
                res['CARGA'][vuelo['ORIGEN']] += 1
            if vuelo['DESTINO'] not in list(res['CARGA'].keys()):
                res['CARGA'][vuelo['DESTINO']] = 1
            elif vuelo['DESTINO'] in list(res['CARGA']):
                res['CARGA'][vuelo['DESTINO']] += 1
        if vuelo["TIPO_VUELO"] == 'MILITAR':
            if vuelo['ORIGEN'] not in list(res['MILITAR'].keys()):
                res['MILITAR'][vuelo['ORIGEN']] = 1
            elif vuelo['ORIGEN'] in list(res['MILITAR']):
                res['MILITAR'][vuelo['ORIGEN']] += 1
            if vuelo['DESTINO'] not in list(res['MILITAR'].keys()):
                res['MILITAR'][vuelo['DESTINO']] = 1
            elif vuelo['DESTINO'] in list(res['MILITAR']):
                res['MILITAR'][vuelo['DESTINO']] += 1
    
    ordenada_comercial = dict(sorted(res['COMERCIAL'].items(), key=lambda x: (-x[1], x[0])))
    ordenada_carga = dict(sorted(res['CARGA'].items(), key=lambda x: (-x[1], x[0])))
    ordenada_militar = dict(sorted(res['MILITAR'].items(), key=lambda x: (-x[1], x[0]))) 
    
    data_structs['concurrencia']['COMERCIAL'] = ordenada_comercial
    data_structs['concurrencia']['CARGA'] = ordenada_carga
    data_structs['concurrencia']['MILITAR'] = ordenada_militar
    
    
    nombres_comercial = {}
    nombres_carga = {}
    nombres_militar = {}
    i = 0
    while len(nombres_comercial) < 5:
        nombres_comercial[list(ordenada_comercial.keys())[i]] = ordenada_comercial[list(ordenada_comercial.keys())[i]]
        nombres_carga[list(ordenada_carga.keys())[i]] = ordenada_carga[list(ordenada_carga.keys())[i]]
        nombres_militar[list(ordenada_militar.keys())[i]] = ordenada_militar[list(ordenada_militar.keys())[i]]
        i += 1
    j = len(ordenada_comercial) - 5
    ca = len(ordenada_carga) - 5
    k = 0
    m = len(ordenada_militar) - 5
    while k < 5:
        nombres_comercial[list(ordenada_comercial.keys())[j]] = ordenada_comercial[list(ordenada_comercial.keys())[j]]
        nombres_carga[list(ordenada_carga.keys())[ca]] = ordenada_carga[list(ordenada_carga.keys())[ca]]
        nombres_militar[list(ordenada_militar.keys())[m]] = ordenada_militar[list(ordenada_militar.keys())[m]]        
        j += 1
        k += 1
        ca += 1
        m += 1
    
    aeropuertos = lt.newList('ARRAY_LIST')
    for aeropuerto in lt.iterator(data_structs['airports']):
        if aeropuerto['ICAO'] in list(nombres_comercial.keys()) or aeropuerto['ICAO'] in list(nombres_carga.keys()) or aeropuerto['ICAO'] in list(nombres_militar.keys()):
            lt.addLast(aeropuertos, aeropuerto)
    
            
    
    return nombres_comercial, nombres_carga, nombres_militar, aeropuertos
                       
def componentes(data_structs):
    componentes = scc.KosarajuSCC(data_structs['graph_distancia'])
    numero = scc.connectedComponents(componentes)
    return componentes, numero

# Funciones para creacion de datos
def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

# Funciones creadas para requerimientos



# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def req_1(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    distancia_total = 0
    aero_origen = None
    aero_destino = None
    for aeropuerto in data_structs['coords']:
        distancia_origen = haversine(origen, data_structs['coords'][aeropuerto])
        distancia_destino = haversine(destino, data_structs['coords'][aeropuerto])
        if distancia_origen <= 30:
            aero_origen = aeropuerto
            
        if distancia_destino <= 30:
            aero_destino = aeropuerto
            
    if aero_destino != None and aero_origen != None:
        data_structs['caminos_comercial_time'] = djk.Dijkstra(data_structs['graph_comercial_time'], aero_origen)
        data_structs['caminos_comercial_distancia'] = djk.Dijkstra(data_structs['graph_comercial_distancia'], aero_origen)
        res = djk.hasPathTo(data_structs['caminos_comercial_distancia'], aero_destino)
        
        camino_tiempo = djk.pathTo(data_structs['caminos_comercial_time'], aero_destino)
        camino_distancia = djk.pathTo(data_structs['caminos_comercial_distancia'], aero_destino)
        
        while not st.isEmpty(camino_distancia):
            parada = st.pop(camino_distancia)
            distancia_total = distancia_total + parada['weight']
        
        tiempo_total = 0
        aeropuertos_visitados = []
        while not st.isEmpty(camino_tiempo):
            parada = st.pop(camino_tiempo)
            tiempo_total = tiempo_total + parada['weight']
            aeropuertos_visitados.append(parada['vertexA'])
        
        aeropuertos_visitados.append(aero_destino)
        mapa_aeropuertos = mp.newMap()
        
        for aero in aeropuertos_visitados:
            for coso in lt.iterator(data_structs['airports']):
                if coso['ICAO'] == aero:
                    mp.put(mapa_aeropuertos, aero, coso) 
        
        distancia_total = distancia_destino + distancia_origen
        return res, aero_origen, aero_destino, aeropuertos_visitados, distancia_total, tiempo_total, mapa_aeropuertos 
    if aero_destino == None or aero_origen == None:
        res = False
        mas_cercano = 999
        mas_cercano_d = 999
        for aeropuerto in data_structs['coords']:
            distancia_o = haversine(origen, data_structs['coords'][aeropuerto])
            if distancia_o < mas_cercano:
                mas_cercano = distancia_o
                aero_origen = aeropuerto
            distancia_d = haversine(destino, data_structs['coords'][aeropuerto])
            if distancia_d < mas_cercano_d:
                mas_cercano_d = distancia_d
                aero_destino = aeropuerto   
        aeropuertos_visitados = None
        distancia_total = None
        tiempo_total = None
        mapa_aeropuertos = None
        return res, aero_origen, aero_destino, aeropuertos_visitados, distancia_total, tiempo_total, mapa_aeropuertos
         
def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass

def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    concurrencia = data_structs['concurrencia']['COMERCIAL']
    primer_aeropuerto = next(iter(concurrencia))
    llave_primer = mp.get(data_structs['mapa_aeropuertos'], primer_aeropuerto)
    data_structs['caminos_comercial_time'] = djk.Dijkstra(data_structs['graph_comercial_time'], primer_aeropuerto)
    data_structs['caminos_comercial_distancia'] = djk.Dijkstra(data_structs['graph_comercial_distancia'], primer_aeropuerto)
    distancia_total = 0
    trayectos = lt.newList('ARRAY_LIST')
    for aeropuerto in data_structs["coords"]:
        if djk.hasPathTo(data_structs['caminos_comercial_distancia'], aeropuerto) == True:
            camino_aeropuerto = djk.pathTo(data_structs['caminos_comercial_distancia'], aeropuerto)
            tiempo_aeropuerto = djk.pathTo(data_structs['caminos_comercial_time'], aeropuerto)
            distancia_trayecto = 0
            
            while not st.isEmpty(camino_aeropuerto):
                aero = st.pop(camino_aeropuerto)
                distancia_trayecto = distancia_trayecto + aero['weight']
                distancia_total = distancia_total + aero['weight']
            tiempo_trayecto = 0
            while not st.isEmpty(tiempo_aeropuerto):
                aero = st.pop(tiempo_aeropuerto)
                tiempo_trayecto = tiempo_trayecto + aero['weight']
            dic = {
                'aeropuerto_origen' : me.getValue(mp.get(data_structs['mapa_aeropuertos'], primer_aeropuerto)),
                'aeropuerto_destino' : me.getValue(mp.get(data_structs['mapa_aeropuertos'], aeropuerto)),
                'tiempo_trayecto' : tiempo_trayecto,
                'distancia_trayecto' : distancia_trayecto
            }
            lt.addLast(trayectos, dic)
    
        
    
    return llave_primer, distancia_total, trayectos

def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    concurrencia = data_structs['concurrencia']['CARGA']
    primer_aeropuerto = next(iter(concurrencia))
    llave_primer = mp.get(data_structs['mapa_aeropuertos'], primer_aeropuerto)
    data_structs['caminos_carga_time'] = djk.Dijkstra(data_structs['graph_carga_time'], primer_aeropuerto)
    data_structs['caminos_carga_distancia'] = djk.Dijkstra(data_structs['graph_carga_distancia'], primer_aeropuerto)
    distancia_total = 0
    trayectos = lt.newList('ARRAY_LIST')
    for aeropuerto in data_structs['coords']:
        existe = djk.hasPathTo(data_structs['caminos_carga_time'], aeropuerto)
        if existe != False:
            camino_aeropuerto = djk.pathTo(data_structs['caminos_carga_distancia'], aeropuerto)
            tiempo_aeropuerto = djk.pathTo(data_structs['caminos_carga_time'], aeropuerto)
            distancia_trayecto = 0
            lista_aviones = []
            while not st.isEmpty(camino_aeropuerto):
                aero = st.pop(camino_aeropuerto)
                distancia_trayecto = distancia_trayecto + aero['weight']
                distancia_total = distancia_total + aero['weight']
                llave_vuelos = mp.get(data_structs['mapa_conexiones_aeropuertos'], aero['vertexA'])
                for vuelo in lt.iterator(me.getValue(llave_vuelos)):
                    if vuelo['DESTINO'] == aero['vertexB']:
                        lista_aviones.append(vuelo['TIPO_AERONAVE'])
                
            tiempo_trayecto = 0
            while not st.isEmpty(tiempo_aeropuerto):
                aero = st.pop(tiempo_aeropuerto)
                tiempo_trayecto = tiempo_trayecto + aero['weight']
            
            dic = {
                'aeropuerto_origen' : me.getValue(mp.get(data_structs['mapa_aeropuertos'], primer_aeropuerto)),
                'aeropuerto_destino' : me.getValue(mp.get(data_structs['mapa_aeropuertos'], aeropuerto)),
                'tiempo_trayecto' : tiempo_trayecto,
                'distancia_trayecto' : distancia_trayecto,
                'lista_aviones' : lista_aviones
            }
            lt.addLast(trayectos, dic)
            
    
    return llave_primer, distancia_total, trayectos

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass

def req_6(data_structs, n_aeropuertos):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    concurrencia = data_structs['concurrencia']['COMERCIAL']
    primer_aeropuerto = next(iter(concurrencia))
    llave_primer = mp.get(data_structs['mapa_aeropuertos'], primer_aeropuerto)
    data_structs['caminos_comercial_distancia'] = djk.Dijkstra(data_structs['graph_comercial_distancia'], primer_aeropuerto)
    i = 1
    nombres_aeropuertos = list(concurrencia.keys())
    nombres_n_aeropuertos = lt.newList('ARRAY_LIST')
    respuesta = lt.newList('ARRAY_LIST')
    while i < n_aeropuertos + 1:
        lt.addLast(nombres_n_aeropuertos, nombres_aeropuertos[i])
        i += 1
    print(nombres_n_aeropuertos)
    for aeropuerto in lt.iterator(nombres_n_aeropuertos):
        existe = djk.hasPathTo(data_structs['caminos_comercial_distancia'], aeropuerto)
        if existe != None:
            camino_aeropuerto = djk.pathTo(data_structs['caminos_comercial_distancia'], aeropuerto)
            vuelos_camino = lt.newList('ARRAY_LIST')
            aeropuertos_camino = lt.newList('ARRAY_LIST')
            lt.addLast(aeropuertos_camino, primer_aeropuerto)
            distancia_trayecto = 0
            while not st.isEmpty(camino_aeropuerto):
                arco = st.pop(camino_aeropuerto)
                distancia_trayecto = distancia_trayecto + arco['weight']
                lt.addLast(aeropuertos_camino, arco['vertexB'])
                llave_vuelos = mp.get(data_structs['mapa_conexiones_aeropuertos'], arco['vertexA'])
                for vuelo in lt.iterator(me.getValue(llave_vuelos)):
                    if vuelo['DESTINO'] == arco['vertexB'] and vuelo['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
                        lt.addLast(vuelos_camino, vuelo)
            datos_aeropuertos = lt.newList('ARRAY_LIST')
            for aeropuerto in lt.iterator(aeropuertos_camino):
                aero = mp.get(data_structs['mapa_aeropuertos'], aeropuerto)
                datos = me.getValue(aero)
                dic = {
                    'ICAO: ' : datos['ICAO'],
                    'Nombre del aeropuerto: ' : datos['NOMBRE'],
                    'Ciudad del aeropuerto: ' : datos['CIUDAD'],
                    "Pais del aeropuerto: " : datos['PAIS']
                }
                lt.addLast(datos_aeropuertos, dic)
            
            res = {
                'total_aeropuertos' : lt.size(aeropuertos_camino),
                'lista_aeropuertos' : datos_aeropuertos,
                'lista_vuelos' : vuelos_camino,
                'distancia_trayecto' : distancia_trayecto
            }
            lt.addLast(respuesta, res)
                
                
                
    
    return llave_primer, respuesta
         

def req_7(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    distancia_total = 0
    tiempo_total = 0
    aero_origen = None
    aero_destino = None
    res = False  
    for aeropuerto in data_structs['coords']:
        distancia_origen = haversine(origen, data_structs['coords'][aeropuerto])
        distancia_destino = haversine(destino, data_structs['coords'][aeropuerto])
        if distancia_origen <= 30:
            aero_origen = aeropuerto
            
        if distancia_destino <= 30:
            aero_destino = aeropuerto
          
    if aero_destino != None and aero_origen != None:
        distancia_total = distancia_total + distancia_origen + distancia_destino
        data_structs['caminos_comercial_time'] = djk.Dijkstra(data_structs['graph_comercial_time'], aero_origen)
        res = djk.hasPathTo(data_structs['caminos_comercial_time'], aero_destino)
        datos_aeropuertos = lt.newList('ARRAY_LIST')
        if res == True:
            camino_tiempo = djk.pathTo(data_structs['caminos_comercial_time'], aero_destino)
            
            aeropuertos_camino = lt.newList('ARRAY_LIST')
            lt.addLast(aeropuertos_camino, aero_origen)
            while not st.isEmpty(camino_tiempo):
                arco = st.pop(camino_tiempo)
                tiempo_total = tiempo_total + arco['weight']
                distancia_entre = haversine(data_structs['coords'][arco['vertexA']], data_structs['coords'][arco['vertexB']])
                distancia_total = distancia_total + distancia_entre
                lt.addLast(aeropuertos_camino, arco['vertexB'])
            
            for aeropuerto in lt.iterator(aeropuertos_camino):
                aero = mp.get(data_structs['mapa_aeropuertos'], aeropuerto)
                datos = me.getValue(aero)
                dic = {
                    'ICAO: ' : datos['ICAO'],
                    'Nombre del aeropuerto: ' : datos['NOMBRE'],
                    'Ciudad del aeropuerto: ' : datos['CIUDAD'],
                    "Pais del aeropuerto: " : datos['PAIS']
                }
                lt.addLast(datos_aeropuertos, dic)
        return res, aero_origen, aero_destino, datos_aeropuertos, tiempo_total, distancia_total 
    if aero_destino == None or aero_origen == None:
        res = False
        mas_cercano = 999
        mas_cercano_d = 999
        for aeropuerto in data_structs['coords']:
            distancia_o = haversine(origen, data_structs['coords'][aeropuerto])
            if distancia_o < mas_cercano:
                mas_cercano = distancia_o
                aero_origen = aeropuerto
            distancia_d = haversine(destino, data_structs['coords'][aeropuerto])
            if distancia_d < mas_cercano_d:
                mas_cercano_d = distancia_d
                aero_destino = aeropuerto   
        
        datos_aeropuertos = None
        tiempo_total = None
        distancia_total = None
        return res, aero_origen, aero_destino, datos_aeropuertos, tiempo_total, distancia_total
    
                
                
    


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

