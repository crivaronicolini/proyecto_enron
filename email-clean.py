import os
from collections import defaultdict

campos_listados = ["To", "X-To", "X-cc", "X-bcc"]
# dir = os.walk('./maildir')
fields = {"Message-ID": "",
          "Date": "",
          "From": "",
          "To": [],
          "Subject": "",
          "Mime-Version": "",
          "Content-Type": "",
          "Content-Transfer-Encoding": "",
          "X-From": "",
          "X-To": [],
          "X-cc": [],
          "X-bcc": [],
          "X-Folder": "",
          "X-Origin": ""}

personas = os.listdir('./maildir')
dataset = defaultdict(list)

walk = open('walksort')
# walker = os.walk('./maildir/' + persona)
# breakpoint()
# for dire, folders, mails in list(walker):
for mail in walk.read().splitlines():
    # print(mails)
    lines = []
    with open('./maildir/' + mail) as m:
        for line in m.read().splitlines():
            print(line)
            if line.startswith('X-FileName:'):
                break
            lines.append(line)
    data = fields.copy()
    buff = []
    for line in lines:
        particion = line.partition(': ')
        # si partition encuentra el separador, y lo que esta a la derecha del
        # sep no es nulo, lo agrego al campo, y sino agrego esa linea al buffer
        # si encuentro el separador en una linea que nada que ver, la agrego al
        # buffer y la imprimo
        if particion[2] == "":
            buff.append(particion[0])
            # breakpoint()
        elif particion[0] in data.keys():
            data[particion[0]] = particion[2]
            buff = []
        else:
            buff.append(line)
            print(line)
    # for campo in campos_listados:
    #     data[campo] = data[campo].split(',')
    persona = mail.split('/')[0]
    dataset[persona].append(data)
print(dataset)
walk.close()
