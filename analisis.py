import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import igraph as ig
import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import networkx as nx
# PARA AGREGAR CENTRALIDADES A LA RED GRANDE
'''
de = nx.degree_centrality(G)
g.nodes['greg.couch']['degree'] == de['greg.couch']
g.nodes['jozef.lieskovsky']['degree'] == de['jozef.lieskovsky']
g.number_of_nodes()
nx.set_node_attributes(g, de, 'degree')

bb = pd.read_csv('closeness-grande.csv')
bbdict = bb.set_index('nodo')['degree'].to_dict()
nx.set_node_attributes(g, bbdict, 'closeness')
g.nodes['greg.couch']['closeness'] == bbdict['greg.couch']
g.nodes['jozef.lieskovsky']['closeness'] == bbdict['jozef.lieskovsky']

ei = pd.read_csv('eigenvalue-grande.csv')
eidict = ei.set_index('nodo')['degree'].to_dict()
nx.set_node_attributes(g, eidict, 'eigen')

for nodo in g.nodes():
    if not g.nodes[nodo]['closeness'] == bbdict[nodo]:
        print(nodo)
    if not g.nodes[nodo]['degree'] == de[nodo]:
        print(nodo)
    if not g.nodes[nodo]['eigen'] == eidict[nodo]:
        print(nodo)
    if not g.nodes[nodo]['closeness'] == bbdict[nodo]:
        print(nodo)

for nombre in archsemes:
    Gdir = nx.read_gml('porsemestre/' + nombre)
    nx.write_gml(Gdir.to_undirected(),
                 'porsemestre-undirected/undirected' + nombre)

# %%
G = nx.read_gml('enron-grande-limpia.gml')
g = nx.read_gml('10000.gml')
'''
# def limpiar(G,admin,misc):
#     nodos = G.nodes()
#     for string in admin:
#         nodos_a_remover = list(filter(lambda x: string in x, nodos))
#         G.remove_nodes_from(nodos_a_remover)

#     G.remove_nodes_from(admin)
#     aislados = list(nx.isolates(G))
#     G.remove_nodes_from(aislados)
#     G.remove_edges_from(nx.selfloop_edges(G))
# admin = ['email','e-mail','<','"','enron','security','communications','everyone','helpdesk','help','houston','omaha','portland',
#         'ect','support','management','parking','team','outlook','corp','office','admin','reception','system','desk','information'
#         ,'services','mailing']

# misc = ['body.shop', 'bodyshop', 'transportation.parking', 'parking.transportation'
#     '4b98e0e8-e7271b97-862566a9-4fb484', '9.ews', 'all-hou.dl-bus',
#     '2.ews', '3e', '40ees','afdeblasio1-503-291-1556ol.com','???????.??????',
#     '3.ews','4.ews','40ect','40newpower',
#     'globalflash.recipients','task.force','postmaster','zipper']
# limpiar(G,admin,misc)
# %%


def ordenar(diccionario, key=1, reverse=True):
    medida = {k: v for k, v in sorted(
        diccionario.items(), key=itemgetter(key), reverse=reverse)}
    return medida


def subgrafocomunidad(persona, graph, clusters):
    '''Devuelve el subgrafo con la comunidad que contiene a persona'''
    # if not clusters:
    #     clusters = graph.community_walktrap(
    #         weights=graph.es['peso']).as_clustering()
    if clusters.graph is not graph:
        raise NameError('los clusters pasados no corresponden al grafo')
    indice = graph.vs['label'].index(persona)
    return clusters.subgraph(clusters.membership[indice])


def participacion(graph, clusters):
    ''' Calcula el P_i, z_i y de un grafo.
    Primero se caminan los clusters y se llena el diccionario grado_clus con
    {numero de cluster: lista de grados de los nodos}, y el diccionario
    pertenencia con {nodo: cluster al que pertenece}.

    Luego se camina el diccionario de pertenencia y para cada nodo se guardan
    los vecinos.  El kis para usar en p_i es un contador, cuenta cuantos
    vecinos tiene el nodo en cada comnidad.  El ki es el kis correspondiente al
    cluster del nodo, lo mismo con listagrados.  Despues se populan las listas
    que van a ser los resultados con las formulas correspondientes.

    Parametros:
        graph (ig.Graph): grafo a estudiar.
        clusters (ig.clustering.VertexClustering): cluster correspondiente a graph.
    Returns:
        p (list): participacion de nodos.
        pertenencia (list): comunidad a la que pertenecen los nodos
        z (list): z de los nodos
    Ejemplo:
        $ g.vs['p'], g.vs['pert'], g.vs['zi'] = participacion(g, clusters=g.community_infomap())
        $ g.vs['zi'][1]
        > -0.7071067811865478
        '''
    if clusters.graph is not graph:
        raise NameError('los clusters pasados no corresponden al grafo')
    pertenencia, p, z, grado_clus = {}, {}, {}, {}
    for i, cluster in enumerate(clusters):
        grado_clus[i] = []
        for nodo in cluster:
            pertenencia[nodo] = i
            grado_clus[i].append(graph.vs[nodo].degree())
    for nodo, i in pertenencia.items():
        vecinos = graph.neighbors(graph.vs[nodo], mode='ALL')
        kis = Counter([pertenencia[nodo] for nodo in vecinos])
        ki = kis[i]
        listagrados = grado_clus[i]
        ksi = np.mean(listagrados)
        sigma = np.std(listagrados)
        k = len(vecinos)
        p[nodo] = 1 - sum([(i/k)**2 for i in kis.values()])
        if sigma == 0:
            z[nodo] = np.nan
            continue
        z[nodo] = (ki - ksi)/(sigma)
    resulados = []
    for x in [p, pertenencia, z]:
        x = ordenar(x, key=0, reverse=False)
        resulados.append(list(x.values()))
    return resulados


# chica = ig.read('red-150bien.gml')
# redclus = g
# # g = ig.read('red-150bien.gml').simplify(multiple=False)
# grande = ig.read('enron-grande-limpia.gml')
# diezmil = ig.read('10000_undirected.gml')

funciones = {
    'betweeness': lambda x: ig.Graph.betweenness(x, weights=x.es['peso']),
    'closeness': lambda x: ig.Graph.closeness(x, weights=x.es['peso']),
    'eigenvalue': lambda x: ig.Graph.evcent(x, weights=x.es['peso']),
    'degree':     ig.Graph.degree,
}


def calc_centr(dic):
    ''' Calcula las funciones de centralidad de una red y las imprime en tabla'''
    tabla = {}
    for nombre, red in dic:
        print(nombre)
        g = red['g']
        for nom_func, funcion in funciones.items():
            medida = funcion(g)
            resultado = {p: m for p, m in zip(g.vs['label'], medida)}
            final = list(ordenar(resultado).items())
            tabla[nom_func] = final
            print(nom_func)
            for f in final:
                print(f)


def agregar_centr(redes):
    for nom_func, funcion in funciones.items():
        agregar_prop(redes, nom_func, funcion)


def carga_redes(direccion, nivel=0):
    ''' Carga redes desde archivo o carpeta y devuelve un diccionario con el
    archivo como key, y un diccionario como value que contiene el objeto red.
        Parametros:
            direccion (str): puede ser una carpeta o el nombre de un archivo.
            nivel (0): devuelve el dict solo con la red cargada.
                  (1): ademas devuelve el dict con la red y su particion segun infomap.
                  (2): ademas le asigna los nodos el resultado de correr participacion con esa particion.
        Ejemplo:
            $ redes = cargaredes('porano/', nivel=3)
            $ r
            > {'1998_red': {'g': <igraph.Graph at 0x7fedf96a5750>,
               'clusters': <igraph.clustering.VertexClustering at 0x7fedf3437490>},
              '1999_red': {'g': <igraph.Graph at 0x7fedf5926550>,
               'clusters': <igraph.clustering.VertexClustering at 0x7fedf358b310>}}
            $ redes['1999_red']['g'].vs['pert'][1]
            > 0.85
    '''
    try:
        archivos = [os.path.abspath(os.path.join(direccion, x))
                    for x in sorted(os.listdir(direccion))]
    except NotADirectoryError:
        archivos = [direccion]
    redes = {}
    for archivo in archivos:
        nombre = os.path.splitext(os.path.basename(archivo))[0]
        print('cargando ' + nombre)
        g = ig.read(archivo)
        redes[nombre] = {'g': g}
        if nivel >= 1:
            redes[nombre]['clusters'] = g.community_infomap(
                edge_weights=g.es['peso'])
        if nivel >= 2:
            g.vs['p'], g.vs['pert'], g.vs['zi'] = participacion(
                g, clusters=redes[nombre]['clusters'])
    return redes


def agregar_prop(redes, props, funcion):
    ''' Agrega la propiedad `prop` a todas las redes de un dict de redes,
    usando la funcion `funcion`.
    Parametros: 
        redes (dict): diccionario de redes como devuelve `cargaredes`.
        prop (str o list): propiedad(es) a cargar, va a ser el key con el
            que van a estar identificadas en la red.
        funcion (function): funcion a usar.  
    Ejemplo: 
        $ agregar_prop(redesaño,'betweenness',lambda x: ig.Graph.betweenness(x, weights=x.es['peso']))
        $ redesaño['2002_red']['g'].vs['betweenness'][1]
        > 6180.605216905224'''
    for nombre, redclus in redes.items():
        g = redclus['g']
        print(f'agregando {props} a {nombre}')
        try:
            # la funcion solo acepta g
            resultado = funcion(g)
            g.vs[props] = resultado
        except TypeError:
            # la funcion acepta g y cluster
            if 'clusters' not in redclus:
                redclus['clusters'] = g.community_infomap(
                    edge_weights=g.es['peso'])
            resultado = funcion(g, clusters=redclus['clusters'])
            if isinstance(props, list):
                for i, prop in enumerate(props):
                    g.vs[prop] = resultado[i]
            if isinstance(props, str):
                g.vs[props] = resultado
            else:
                raise TypeError(
                    'Esta funcion solo agrega propiedades de una lista o de un str.')


def agregar_comunes(redes):
    ''' Funcion de conveniencia para agregar propiedades comunes a las redes de dic.
    Parametros:
        redes (dict): diccionario de redes como devuelve `cargaredes`.
    '''
    agregar_prop(redes, ['p', 'pert', 'zi'], participacion)


# ALTAS PARTICIPACION REDES EN TIEMPO
def part_alta(redes, corte=0.85):
    print(f'participacion mas alta que {corte}')
    for nombre, redclus in redes.items():
        print(f'\ngrafo {nombre}--------------------------')
        cantnodos = len(redclus['g'].vs)
        for i, nodos in enumerate(redclus['clusters']):
            cantclusters = len(redclus['clusters'])
            if len(nodos) <= 30:
                continue
            tienenodos = False
            altos = []
            for nodo in nodos:
                p = redclus['g'].vs[nodo]['p']
                if p > corte:
                    altos.append(f'{redclus["g"].vs[nodo]["label"]}\t{p:0.2f}')
                    tienenodos = True
            if tienenodos:
                print(
                    f'\ncluster {i}/{cantclusters}, {len(nodos)} nodos, {len(nodos)/cantnodos:0.3f} fraccion')
                for alto in altos:
                    print(alto)

    # break


# # tabla de personas con alta participacion
# clusters = grande.community_infomap(edge_weights=grande.es['peso'])
# # clusters1000 = diezmil.community_infomap(edge_weights=diezmil.es['peso'])
# clusters1000 = diezmil.to_undirected
# clusters1000 = diezmil.community_multilevel(weights=diezmil.es['peso'])
# # clusters = grande.community_walktrap(weights=grande.es['peso']).as_clustering()
# # clusters = grande.community_multilevel(weights=grande.es['peso'])
# grande.vs['p'], grande.vs['pert'] = participacion(grande, clusters=clusters)
# diezmil.vs['p'], diezmil.vs['pert'] = participacion(
#     diezmil, clusters=clusters1000)

# CLUSTER NOMBRES IMPORTANTES MUCHAS REDES
# TODO PARA EL INFORME
# pintar los nodos culpables
# ver algun patron de comunicacion entre ellos

# print(f'persona,semestre,numcomunidades,comunidad,tamaño,fraccion,participacion,zi,grado')


def cluster_personas(redes):
    tabla = []
    for nombre, redclus in redes.items():
        for persona in nombres_importantes:
            tamañored = len(redclus['g'].vs)
            renglon = []
            atributos = redclus['g'].vs.attributes()[2:]
            try:
                nodo = redclus["g"].vs.find(label=persona)
                clusjeff = nodo['pert']
                tamaño = len(redclus["clusters"][clusjeff])
                renglon += [persona, nombre.lstrip('_red'), len(redclus["clusters"]), clusjeff,
                            tamaño, tamaño/tamañored]
                for atributo in atributos:
                    renglon += nodo[atributo]
            except ValueError:
                renglon.append([persona, nombre, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                                np.nan])
    df = pd.DataFrame(tabla, columns=['persona', 'semestre', 'numcomunidades', 'comunidad',
                                      'tamaño', 'fraccion', *atributos]).sort_values(['persona', 'semestre'])
    df.reset_index(drop=True, inplace=True)
    return df


def plotpzi(redes, ejes):
    for nombre, redclus in redes.items():
        g = redclus['g']
        clusters = redclus['clusters']
        data = {}
        atributos = g.vs.attributes()
        for i, eje in enumerate(ejes):
            if eje not in atributos:
                raise RuntimeError(
                    f'ese eje no esta en los atributos de la red {nombre}')
            data[i] = g.vs[eje]
        plt.title(
            fr'$P_{{i}}\ vs\ z_{{i}}\ en\ el\ año\ {nombre.rstrip("_red")}$')
        plt.xlabel(ejes[0])
        plt.ylabel(ejes[1])
        plt.scatter(data[0], data[1], c=list(
            g.vs['pert']), cmap=plt.cm.tab20c)
        plt.show()
        # break


# for nombre, redclus in anosr.items():
#     g = redclus['g']
#     print(g.vs['p'])
# sacar los top de participacion
# k = grande.vs['p']
# for no in sorted(grande.vs, key=lambda x: k[x.index], reverse=True)[:10]:
#     print(no['label'], no['p'], no.degree())


# ig.plot(g, 'enron-chica-color-participacion.svg',
#         layout=g.layout('lgl'), **vis)
# c = {'betweenness': g.community_edge_betweenness(weights=g.es['peso']).as_clustering(),
#      # # 0.337
#      # g.community_fastgreedy(weights=g.es['peso']).as_clustering().q
#      # # no anda para dirigidos
#      'infomap': g.community_infomap(edge_weights=g.es['peso']),
#      # # 0.561
#      # g.community_label_propagation(weights=g.es['peso']).q
#      # # 0.554
#      # 'eigen':g.community_leading_eigenvector(weights=g.es['peso']),
#      # # 0.488
#      # g.community_optimal_modularity(weights=g.es['peso']).as_clustering().q
#      # # lento
#      'spinglass': g.community_spinglass(weights=g.es['peso']),
#      # 0.608
# 'walktrap': g.community_walktrap(weights=g.es['peso']).as_clustering()}
# 0.604 instant
nombres_importantes = ['jeff.skilling', 'sherri.sera',
                       'kenneth.lay', 'rosalee.fleming',
                       'sally.beck', 'jeff.dasovich',
                       'david.forster', 'john.lavorato', 'shelley.corman', 'rick.buy', 'louise.kitchen']

vis = {'vertex_size': 10,
       # 'vertex_label': ' ',
       # 'vertex_label': [c if c in nombres_importantes else ' ' for c in g.vs['label']],
       'vertex_label_size': 22,
       'vertex_label_color': '#0719e6',
       'autocurve': False,
       # 'vertex_color': [plt.cm.viridis(c) for c in g.vs['pert']],
       'edge_width': 1, 'bbox': (1200, 1200), 'edge_arrow_size': 0.5, 'edge_width': 1, }

# for n, cluster in c.items():
# n, cluster = 'walktrap', g.community_walktrap(
#     weights=g.es['peso']).as_clustering()

# for nombre, red in redes.items():
#     vis['vertex_label'] = [
#         c if c in nombres_importantes else ' ' for c in red['g'].vs['label']]
#     ig.plot(red['clusters'], f'clus/ano/{nombre}-enron-grande.png', mark_groups=True,
#             layout=red['g'].layout('kk'), **vis)


# g = ig.read('red-152.gml')


# ing = ig.read('enron_red_dirigida.gml')
# walktrap = ing.community_walktrap(weights=ing.es['peso']).as_clustering()
# com_ing = ing.community_infomap(edge_weights='peso')
# ig.plot(atlas, layout=atlas.layout('kk'))
