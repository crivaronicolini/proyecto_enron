import pytest
import numpy as np
import igraph as ig
from ..analisis import *


@pytest.fixture
def red_ejemplo():
    ''' Hago una red con dos comunidades para testear '''
    g = ig.Graph()
    g.add_vertices(7)
    g.add_edges([(0, 1), (0, 2), (2, 1), (0, 3),
                 (3, 4), (4, 5), (5, 3), (6, 5)])
    clusters = g.community_infomap()
    ''' pi esta definido como
            1 - sum_comunidades_s( (enlaces(i, nodos_comunidad_s) / grado_nodo_i)**2 )
        entonces puedo hacer esa cuenta para cada nodo a mano. '''
    p = [
        1 - (2/3)**2 - (1/3)**2,
        1 - (2/2)**2 - (0/2)**2,
        1 - (2/2)**2 - (0/2)**2,
        1 - (1/3)**2 - (2/3)**2,
        1 - (0/2)**2 - (2/2)**2,
        1 - (0/3)**2 - (3/3)**2,
        1 - (0/1)**2 - (1/1)**2,
    ]
    ''' zi esta definido como
            ( enlaces(i, nodos_comunidad_s_i) - promedio_grados_en_s_i ) / desviacion_grado_s_i
        entonces puedo hacer esa cuenta para cada nodo a mano. '''
    grados1, grados2 = [3, 2, 2], [3, 2, 3, 1]
    desviacion_comm1, desviacion_comm2 = np.std(grados1), np.std(grados2)
    promedio_comm1, promedio_comm2 = np.mean(grados1), np.mean(grados2)
    zi = [
        (2 - promedio_comm1) / desviacion_comm1,
        (2 - promedio_comm1) / desviacion_comm1,
        (2 - promedio_comm1) / desviacion_comm1,
        (2 - promedio_comm2) / desviacion_comm2,
        (2 - promedio_comm2) / desviacion_comm2,
        (3 - promedio_comm2) / desviacion_comm2,
        (1 - promedio_comm2) / desviacion_comm2,
    ]
    # part = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0}
    part = [1, 1, 1, 0, 0, 0, 0]
    g.vs['p'], g.vs['part'], g.vs['zi'] = p, part, zi
    red = {'g': g, 'clusters': clusters}
    return g, clusters


def test_analisis_participacionzi(red_ejemplo):
    g, clusters = red_ejemplo
    # ptest, parttest, zitest = test_participacionzi(g, clusters)
    ptest, parttest, zitest = participacion(g, clusters)
    np.testing.assert_allclose(ptest, g.vs['p'])
    np.testing.assert_allclose(parttest, g.vs['part'])
    np.testing.assert_allclose(zitest, g.vs['zi'])
