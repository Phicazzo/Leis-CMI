from pathlib import Path
import requests
import os
from time import sleep
from bs4 import BeautifulSoup

Lista=[]
Pastas=[]


def Pg_Matriz():
    Url =  requests.get('http://cpdoc.camaraitaguai.rj.gov.br/images/leis/')
    EndUrl = 'http://cpdoc.camaraitaguai.rj.gov.br/images/leis/'
    Busca(Url,EndUrl)

def Busca(Url,EndUrl):
    soup = BeautifulSoup(Url.text,'html.parser')
    for i in soup.find_all('a'):
        if '.pdf' in i.get('href'):
           Item={}
           Item["Raiz"]=str(EndUrl[43:])
           Item["Nome"]=str(i.get('href'))
           Item['Url']=str(EndUrl+str(i.get('href')))
           Lista.append(Item)
        elif '.xls' in i.get('href'):
            Item = {}
            Item["Raiz"] = str(EndUrl[43:])
            Item["Nome"] = str(i.get('href'))
            Item['Url'] = str(EndUrl + str(i.get('href')))
            Lista.append(Item)
        elif '/' in i.get('href'):
            if 'images' in i.get('href'):
                continue
            else:
                Pastas.append(str(i.get('href')))

def Download(Raiz,Nome,Endereco):
    #print(Nome, '<<<<')
    if Raiz == 'leis':
        if Nome in os.listdir(os.getcwd() + str(Raiz)):
            print(Nome,"Ja encontrado")
        else:
            print(Nome, Endereco, Raiz,"Baixado.")
            Arquivo = Path(os.getcwd() + str(Raiz + Nome))
            Baixar = requests.get(Endereco)
            Arquivo.write_bytes(Baixar.content)
    else:
        if Nome in os.listdir(os.getcwd() + str(Raiz[5:])):
            print(Nome,"Ja encontrado")
        else:
            print(Nome, Endereco, Raiz,"Baixado.")
            Arquivo = Path(os.getcwd() + str(Raiz[5:] + Nome))
            Baixar = requests.get(Endereco)
            Arquivo.write_bytes(Baixar.content)


Pg_Matriz()

for i in Pastas:
    if i[:-1] in os.listdir(os.getcwd()):
        continue
    else:
        print('criando pasta',i[:-1])
        os.mkdir(i)

for i in Pastas:
    Url = requests.get('http://cpdoc.camaraitaguai.rj.gov.br/images/leis/'+str(i))
    EndUrl='http://cpdoc.camaraitaguai.rj.gov.br/images/leis/'+str(i)
    Busca(Url,EndUrl)



for i in Lista:
    print(len(Lista),'de',Lista.index(i))
    print(int((Lista.index(i)*11)/len(Lista)),'Porcento')
    Download(i['Raiz'],i['Nome'],i['Url'])

