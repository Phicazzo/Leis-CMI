from pathlib import Path
import requests
import os
from bs4 import BeautifulSoup

Lista=[] 
Pastas=[]


def Pg_Matriz(): #Página inicial do catalogo de Docs a serem baixados 
    Url =  requests.get('http://cpdoc.camaraitaguai.rj.gov.br/images/leis/') #Página inicial do catalogo de Docs a serem baixados 
    EndUrl = 'http://cpdoc.camaraitaguai.rj.gov.br/images/leis/' #Url Final a ser buscado as informações
    Busca(Url,EndUrl)

def Busca(Url,EndUrl): #Função de busca alteravél
    soup = BeautifulSoup(Url.text,'html.parser')#Página a Buscar as informações
    for i in soup.find_all('a'): #para cada a no codigo Html da pagina acima 
        if '.pdf' in i.get('href'):#se o item tiver .pdf (destinar para baixar)
           Item={}#cria dic com as descrições do arquivo
           Item["Raiz"]=str(EndUrl[43:])#Url Raiz
           Item["Nome"]=str(i.get('href'))#Nome do Arquivo 
           Item['Url']=str(EndUrl+str(i.get('href')))#Url do Download
           Lista.append(Item)#adiciona o item a lista de downlodas
        elif '.xls' in i.get('href'):#se for uma tabela de Excel
            Item = {}
            Item["Raiz"] = str(EndUrl[43:])
            Item["Nome"] = str(i.get('href'))
            Item['Url'] = str(EndUrl + str(i.get('href')))
            Lista.append(Item)
        elif '/' in i.get('href'):#se for uma pasta
            if 'images' in i.get('href'):#se for a pasta imagens ignora
                continue
            else:#Caso contrario adiciona a pastas a serem buscadas 
                Pastas.append(str(i.get('href')))

def Download(Raiz,Nome,Endereco):#fução de Download com base no nome. url raiz e endereço 
    #print(Nome, '<<<<')
    if Raiz == 'leis':
        if Nome in os.listdir(os.getcwd() + str(Raiz)):
            print(Nome,"Ja encontrado")
        else:
            Arquivo = Path(os.getcwd() + str(Raiz + Nome))
            Baixar = requests.get(Endereco)
            Arquivo.write_bytes(Baixar.content)
            print(Nome, Endereco, Raiz + '\n' "Baixado.")
    else:
        if Nome in os.listdir(os.getcwd() + str(Raiz[5:])):
            print(Nome,"Ja encontrado")
        else:
            print(Nome, Endereco, Raiz+'\n' "Baixado.")
            Arquivo = Path(os.getcwd() + str(Raiz[5:] + Nome))
            Baixar = requests.get(Endereco)
            Arquivo.write_bytes(Baixar.content)


Pg_Matriz()

for i in Pastas:
    if i[:-1] in os.listdir(os.getcwd()):
        continue
    else:
        print('Criando pasta para Downloads ',i[:-1],"(Ano)")
        os.mkdir(i)

print("Buscando arquivos...")
for i in Pastas:
    Url = requests.get('http://cpdoc.camaraitaguai.rj.gov.br/images/leis/'+str(i))
    EndUrl='http://cpdoc.camaraitaguai.rj.gov.br/images/leis/'+str(i)
    Busca(Url,EndUrl)




for i in Lista:
    print(len(Lista),'de',Lista.index(i))
    print(int((Lista.index(i)*11)/len(Lista)),'Porcento')
    Download(i['Raiz'],i['Nome'],i['Url'])

