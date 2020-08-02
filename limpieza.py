from collections import defaultdict
import pandas as pd
import igraph as ig

# df5 = pd.read_csv("enron/enron_marco_1_of_6.csv",
#                   converters={'To': lambda x: x.strip("'[]").split("', '"),
#                               'From': lambda x: x.strip("'[]").split("', '")})

# df4 = pd.read_csv("enron/enron_marco_1_of_6.csv",
#                   usecols=['Subject', 'To', 'From'],
#                   converters={'To': lambda x: x. strip("'[]").split("', '"),
#                               'From': lambda x: x.strip("'[]").split("', '")})

df9 = pd.read_csv("enron/enron_marco.csv",
                  usecols=['To', 'From',
                           # 'X-Folder','X-To', 'Subject'
                           'user', 'X-From',
                           ],
                  converters={'To': lambda x: x. strip("'[]").strip('><"'),
                              'From': lambda x: x.strip("'[]").strip('><"'),
                              'X-Origin': lambda x: x.lower(),
                              'X-From': lambda x: x.split('<')[0],
                              },
                  # nrows=500
                  )

# holabb = pd.read_csv('enron/enron_marco.csv',
#                      # usecols=['To', 'From'],
#                      converters={'To': lambda x: x. strip("frozenset{}"),
#                                  'From': lambda x: x.strip("frozenset{}")},
#                      )

# df = pd.read_csv('enron/enron_marco.csv',
#                  usecols=['To', 'From'],
#                  converters={'To': lambda x: x. strip("'[]"),
#                              'From': lambda x: x.strip("'[]")},
#                  )
# network = nx.read_gml('./enron/enron_red_ingrid.gml')
df = pd.read_csv('./enron_final-ingr.csv')

# filtro los autores enron y separo los mails de las casillas
lista_mails = df9[df9['From'].str.contains(
    'enron', regex=False)].drop_duplicates('From')['From']
lista_mails.apply(lambda x: x.split('@'))


# df9[df9['To'].str.contains(', ', regex=False)]['To'].map(
#     lambda x: x.split("', '"))


# filtro los destinatarios que dicen enron
solo_enron = df9[df9['From'].str.endswith('@enron.com')]
# a los que tienen varios destinatarios los hago list
# y abro la lista en filas separadas
# al parecer el explode copia el numero de indice para cada fila
solo_enron['To'] = solo_enron['To'].map(lambda x: x.split("', '"))
solo_enron = solo_enron.explode('To')
# de los destinatarios me quedo con los de enron
# s = solo_enron.reset_index(drop=True)
solo_enron = solo_enron[solo_enron['To'].str.endswith(
    '@enron.com')]
solo_enron.reset_index(drop=True, inplace=True)

# puedo ver cuantos mails mando el From al To
grp = solo_enron.groupby(['From'])['To'].value_counts()


# separo los autores en mail y dominio
spl = df9['From'].apply(lambda x: x.split('@'))
# separo esa lista en columnas
doms = pd.DataFrame(spl.to_list())
# cuento las ocurrencias
doms[1].drop_duplicates().value_counts()

arrobas = doms[1].value_counts().drop_duplicates()
direcciones = doms[0]
# arrobas.to_csv('arrobas.csv')

# df6[df6['To'].str.contains(',')]
df9[df9['Direccion-from'].str.contains('enron')]
# a = df1['To'].apply(lambda x: x.strip("'[]").split("', '"))

# quiero ver la cantidad de direcciones que tienen enron
# en el nombre. Pienso que son direcciones institucionales
# de colgado lo hice con el df9 cuando era con el solo_enron son 36325 mails en total
from_separado = pd.DataFrame(solo_enron['From'].apply(
    lambda x: x.split('@')).to_list())
from_separado2 = pd.DataFrame(solo_enron['To'].apply(
    lambda x: x.split('@')).to_list())
# TODO ver por que esto me tira algunas filas donde no van.
# UPDADTE creo que es por el indice que no se desplegaba en el explode
solo_enron.insert(2, 'direccion-from', from_separado[0])
solo_enron.insert(4, 'direccion-to', from_separado2[0])

solo_enron.insert(3, 'dominio-from', from_separado[1])
# si me quedo solo con los @enron esto no va a funcionar
enron_en_dir2 = solo_enron[solo_enron['Direccion-from'].str.contains('enron')]
enron_en_dir2['From'].value_counts().drop_duplicates()
# technology.enron@enron.com                          21552
# enron.announcements@enron.com                        8893
# announcements.enron@enron.com                        1468
# 40enron@enron.com                                     678
# enron.announcement@enron.com                          569
# enron_update@concureworkplace.com                     523
# enronsportsbook@yahoo.com                             434
# cuttings.enron@enron.com                              329
# enron-owner@lists.qgadc.com                           328
# chairman.enron@enron.com                              285
# administration.enron@enron.com                        148
# enron.chairman@enron.com                              142
# admin.enron@enron.com                                  65
# enron.mailsweeper.admin@enron.com                      51
# enron.expertfinder@enron.com                           48
# enron-admin@fsddatasvc.com                             44
# experience.enron@enron.com                             38
# enron.experience@enron.com                             37
# enronsato@hotmail.com                                  34
# enron.payroll@enron.com                                31
# andrew.gieser.enronxgate@enron.com                     30
# john.shafer.enronxgate@enron.com                       27
# payroll.enron@enron.com                                25
# enron@avenueb2e.com                                    20
# enron.gss@enron.com                                    19
# services.enron@enron.com                               18
# enron@houston.rr.com                                   17
# enron.administration@enron.com                         14
# enron.security@enron.com                               12
# enronsigshop@calltsc.com                               11
# enronanywhere@enron.com                                10
# shieldsenron@aol.com                                    9
# enron@easymatch.com                                     7
# enron.messaging.administration@enron.com                6
# enronforum@enronforum.com                               5
# enronmediacuttings@enron.com                            4
# enron.general.announcements.enronxgate@enron.com        3
# mike.harper.enronxgate@enron.com                        2
# resources.enron@enron.com                               1

# alguien le manda mails a esas direcciones?
# si, hay 333 a esas direcciones
solo_enron[solo_enron['To'].isin(enron_en_dir2['From'])][['From', 'To']]

'''
para tratar de agrupar los mails con los nombres de carpetas
para cada fila
    split el from (me quedo con el apellido) y el user
    fijarse si coinciden los elementos
        si coinciden mandarlos a un df
        si no coinciden mandarlos a otro
'''
dir_spl1 = pd.DataFrame(
    solo_enron['Direccion-from'].apply(lambda x: x.split('.')[1]).to_list())
dir_spl = pd.DataFrame(
    solo_enron['Direccion-from'].apply(lambda x: x.split('.')).to_list())
user_spl = pd.DataFrame(solo_enron['user'].apply(
    lambda x: x.split('-')).to_list())
apellidos = solo_enron['user'].apply(lambda x: x.split('-')[0])
# al user_spl parece bien solo usar la primer columna que son los apellidos
dir_spl[dir_spl.isin(apellidos)]
# avor[avor[1].isin(apellidos)]
matched_dirs = solo_enron[dir_spl[1].isin(apellidos)]
empleados = solo_enron[dir_spl[1].isin(apellidos)]['From'].drop_duplicates()
# ahora falta quedarme con los To que estan en esa lista
# caca = pd.DataFrame([x for x in zip(dir_spl[1], user_spl[0]) if x[0] in x[1]])
# [x for x in zip(dir_spl[1], user_spl[0])]
# diferencia entre user y x-origin, a x-origin tiene menos gente y los que tiene estan mal
# df9[df9['user']!=df9['X-Origin']][['Subject','user','X-Origin','X-Folder']].drop_duplicates().to_csv('comparacion-carpeta-user-subject.csv')


# maybe me puedo fijar el mail mas comun en cada carpeta, y quedarme con
# ese si coincide el apellido
def printx(x):
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 100)
    print(x)
    pd.reset_option('display.max_rows')


# para quedarme con los 152 empleados miro la carpeta donde guardaban sus mails (user)
malos = [
    # 'greg.whalley',
    # 'jeff.dasovich',
    # 'stephanie.panus',
    'sally.beck',
]

grup = solo_enron.groupby('user')
user_mail = {}
for user in grup:
    # grup es una tupla con user en el primer elemento y un dataframe en el segundo, este tiene la info de ese user
    # de los mails que estan en el from, me fijo los mas comunes
    direcciones_comunes = user[1]['direccion-from'].value_counts().index.to_list()
    if not direcciones_comunes:
        print(f'\nUSER NOT IN DIR COMUNES {user[0]}')
    # todos tienen el formato nombre.apellido, lo separo en una lista
    direcciones_comunes_spl = [x.replace('..', '.').split(
        '.') for x in direcciones_comunes if x]
    try:
        # hago lo mismo para el user, que tiene formato apellido-inicial
        apellido, inicial = user[0].split('-')
    except ValueError:
        # hay una usuaria que se llama mims-thurston-p, ignoro el thurston
        apellido, _, inicial = user[0].split('-')
    # voy a matchear direccion-persona viendo que tan parecidos son,
    # si tiene el mimo apellido le doy 2 puntos, si tiene la misma inicial 1
    scores = []
    cosa = {}
    for i, d in enumerate(direcciones_comunes_spl):
        score = 0
        try:
            if apellido == d[1]:
                score += 2
            if inicial == d[0][0]:
                score += 1
        except IndexError:
            # la direccion no tiene . para separar, corresponde a no personas
            # print(f'\n\n index error {d}\n\n')
            continue
        # print(d, score)
        # scores[score].append(direcciones_comunes[i])
        scores.append(score)
        cosa[direcciones_comunes[i]] = score
    # el mas probable es la primer direccion que tenga el maximo puntaje
    # en el usuario may-l eso me devuelve el indice anterior
    mail_probable = list(cosa.keys())[scores.index(max(scores))]
    # mail_probable = direcciones_comunes[scores.index(max(scores))]
    user_mail[user[0]] = mail_probable
    if mail_probable in malos:
        # print(f'\n\nMALO {user}\n{mail_probable}\n{cosa}')
        print(
            f'\n\nMALO {user}\n{mail_probable}\n{[(i,j) for i,j in cosa.items() if j>0]}')
    # if user[0] =='may-l':
    #     raise IndexError

mails = user_mail.values()
# hago un dataframe con los mails en los que el from y el to estan en la lista de direcciones de empleados
los150 = solo_enron[solo_enron['direccion-from'].isin(
    mails) & solo_enron['direccion-to'].isin(mails)][['direccion-from', 'direccion-to']]
los150 = los150[~(los150['direccion-from'] == los150['direccion-to'])]
los150 = los150.groupby(los150.columns.tolist()).size(
).reset_index().rename(columns={0: 'peso'})

# import networkx as nx
# los150.to_csv('los150bienbien.csv')
# red = nx.from_pandas_edgelist(los150, source='direccion-from',
#                               target='direccion-to', edge_attr='peso', create_using=nx.DiGraph)
# nx.write_gml(red, 'red-150bien.gml')

'''
duplicados:
 'greg.whalley',
    puede que hayan dos carpetas con distinto nombre que son  de la misma persona
 'stephanie.panus',
    parece que stephanie panus tiene las carpetas phanis-s y panus-s

otros:
   {'robert.benson', 'steven.south'}
    no estan solo en el from
    
'''
# 13:34:26
# 13:36:26
# tardo 2 minutos

'''


Objetivos
Ver con estudios de centralidad cuales fueron los principales empleados involucrados en la empresa.

- Pesos en los enlaces
    Cantidad de mails compartidos?

- Centralidad, como depende de el peso?
    - como depende de si incluimos cc o no?

- Clustering, metodos

- Ver como evoluciona en el tiempo estas medidas


Modificamos el script de brianray en data.world (https://github.com/brianray/data.world-scripts/blob/master/enron_email_script.ipynb) que agrupa los archivos de mail del dataset oficial (http://www.cs.cmu.edu/~enron/).
Con esto obtuvimos un archivo csv donde cada fila es un mail y las columnas indican el destinatario, el sujeto, etc.

'''
