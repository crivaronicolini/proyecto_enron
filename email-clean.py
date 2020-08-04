import os
import pandas as pd
from collections import defaultdict
pd.DataFrame.to_csv
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
walk = open('walksort')
lines = []
data = fields.copy()
buff = ""
buffkey = ""
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
            if particion[0].startswith('\t'):
                # si empieza con un tab pertenece al campo anterior
                buff += particion[0].lstrip('\t')
            if particion[0] in data.keys():
                # si empieza con un key y el buffer existe, agrego el buffer
                # y este key lo agrego a un nuevo buffer
                if buffkey and buff:
                    data[buffkey] = buff
                    buff = ""
                    buffkey = ""
                buffkey = particion[0]
            if particion[2] != "":
                buff += particion[2]
        persona = mail.split('/')[0]
        data['user'] = persona
        data['file'] = mail
        dataset.append(data)
        m.close()
    except UnicodeDecodeError as e:
        print(mail)
        raise e
walk.close()
df = pd.DataFrame(dataset)
# pasar a datetime (tarda unos minutos)
df['Date'] = pd.to_datetime(
    df['Date'], infer_datetime_format=True, errors='coerce')
df.to_csv('enron_dataset.csv')
