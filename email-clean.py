import ipdb
import os
import pandas as pd
from collections import defaultdict

campos_listados = ["To", "X-To", "X-cc", "X-bcc"]
# dir = os.walk('./maildir')
fields = {"Message-ID": "",
          "Date": "",
          "From": "",
          "To": "",
          "Cc": "",
          "Bcc": "",
          "Subject": "",
          "Mime-Version": "",
          "Content-Type": "",
          "Content-Transfer-Encoding": "",
          "X-From": "",
          "X-To": "",
          "X-cc": "",
          "X-bcc": "",
          "X-Folder": "",
          "X-Origin": "",
          "user": "",
          "file": ""}

personas = os.listdir('./maildir')
dataset = []
# dataset = defaultdict(list)
# ipdb.set_trace()
walk = open('walksort')
i = 0
# print(mails)
lines = []
# with open('./maildir/' + mail) as m:
data = fields.copy()
buff = ""
buffkey = ""

# try:
#     m = open('mailprueba', encoding='cp1252')
#     for line in m.read().splitlines():
#         # print(line)
#         if line.startswith('X-FileName:'):
#             break
#         particion = line.partition(': ')
#         # si partition encuentra el separador, y lo que esta a la derecha del
#         # sep no es nulo, lo agrego al campo, y sino agrego esa linea al buffer
#         # si encuentro el separador en una linea que nada que ver, la agrego al
#         # buffer y la imprimo
#         if particion[0].startswith('\t'):
#             buff += particion[0].lstrip('\t')
#         if particion[0] in data.keys():
#             if buffkey and buff:
#                 data[buffkey] = buff
#                 buff = ""
#                 buffkey = ""
#             buffkey = particion[0]
#         if particion[2] != "":
#             buff += particion[2]
#             # print(buff)

#         # if particion[0] in data.keys():
#         #     if buffkey and buff:
#         #         data[buffkey] = buff
#         #         buff = ""
#         #         buffkey = ""
#         #     buffkey = particion[0]
#         #     # print(buffkey)
#         # if particion[2] != "":
#         #     buff += particion[2]
#             # print(buff)

#         # if particion[2] == "":
#         #     if particion[0].split(' ')[0] in data.keys():
#         #         ipdb.set_trace()
#         #         buffkey = particion[0]
#         #         # print('buffkey')
#         #         # print(buffkey)
#         #     else:
#         #         buff.append(particion[0].strip())
#         #         # print('buff')
#         #         # print(buff)
#         #     # print(line)
#         #     # print(buff)
#         #     # breakpoint()
#         # elif particion[0] in data.keys():
#         #     if buffkey:
#         #         data[buffkey] = ''.join(buff[1:])
#         #         # print(buffkey)
#         #         # print(''.join(buff[1:]))
#         #         buffkey = ''
#         #         buff = []
#         #     data[particion[0]] = particion[2]
#         # else:
#         #     # cosas que no son los keys pero se escapan lo mando al buff
#         #     buff.append(line)
#         # print(line)
#     # for campo in campos_listados:
#     #     data[campo] = data[campo].split(',')
#     # persona = mail.split('/')[0]
#     data['user'] = 'allen-p'
#     dataset.append(data)
#     print(data)
#     m.close()
# except UnicodeDecodeError as e:
#     # print(mail)
#     raise e
i = 0
for mail in walk.read().splitlines():
    # print(mails)
    lines = []
    # with open('./maildir/' + mail) as m:
    data = fields.copy()
    buff = ""
    buffkey = ""
    try:
        m = open('./maildir/' + mail, encoding='cp1252')
        for line in m.read().splitlines():
            # print(line)
            if line.startswith('X-FileName:'):
                break
            particion = line.partition(': ')
            # si partition encuentra el separador, y lo que esta a la derecha del
            # sep no es nulo, lo agrego al campo, y sino agrego esa linea al buffer
            # si encuentro el separador en una linea que nada que ver, la agrego al
            # buffer y la imprimo

            if particion[0].startswith('\t'):
                buff += particion[0].lstrip('\t')
            if particion[0] in data.keys():
                if buffkey and buff:
                    data[buffkey] = buff
                    buff = ""
                    buffkey = ""
                buffkey = particion[0]
            if particion[2] != "":
                buff += particion[2]
#             if particion[0] in data.keys():
#                 if buffkey and buff:
#                     data[buffkey] = ''.join(buff)
#                     buff = ""
#                     buffkey = ""
#                 buffkey = particion[0]
#                 # print(buffkey)
#             if particion[2] != "":
#                 buff += particion[2]
#                 # print(buff)
#             # if particion[2] == "":
#             #     if particion[0].split(' ')[0] in data.keys():
#             #         ipdb.set_trace()
#             #         buffkey = particion[0]
#             #         # print('buffkey')
#             #         # print(buffkey)
#             #     else:
#             #         buff.append(particion[0].strip())
#             #         # print('buff')
#             #         # print(buff)
#             #     # print(line)
#             #     # print(buff)
#             #     # breakpoint()
#             # elif particion[0] in data.keys():
#             #     if buffkey:
#             #         data[buffkey] = ''.join(buff[1:])
#             #         # print(buffkey)
#             #         # print(''.join(buff[1:]))
#             #         buffkey = ''
#             #         buff = []
#             #     data[particion[0]] = particion[2]
#             # else:
#             #     # cosas que no son los keys pero se escapan lo mando al buff
#             #     buff.append(line)
#             # print(line)
#         # for campo in campos_listados:
#         #     data[campo] = data[campo].split(',')
        persona = mail.split('/')[0]
        data['user'] = persona
        data['file'] = mail
        dataset.append(data)
        m.close()
    except UnicodeDecodeError as e:
        print(mail)
        raise e
    i += 1
    # if i == 100:
    #     break
walk.close()
df = pd.DataFrame(dataset)
df = dataset.drop(['Mime-Version', 'Content-Type',
                   'Content-Transfer-Encoding'], axis=1)
# Parse datetime
df['Date'] = pd.to_datetime(
    df['Date'], infer_datetime_format=True, errors='coerce')

df[df['Date'] == 'Mon, 12 Mar 2001 00:00:00']
