import csv
from queue import Empty

from otros import graba_diccionario, graba_diccionario_de_diccionarios, crea_diccionario_clientes

def update_users_file(dic:dict, file:str):
    graba_diccionario(dic, file)

def update_pets_file(dic:dict, file:str):
    graba_diccionario_de_diccionarios(dic, file)

def lee_diccionario_usuarios (archivo:str)->dict:
    diccionario = {}
    #users[username]->{campo:cosa}
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['username']
                if llave not in diccionario:
                    diccionario[llave] = {}
                diccionario[llave] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario
def lee_lista_mascotas(archivo:str)->dict:
    diccionario = {}
    #mascotas[user] ->user[mascota]
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['username']
                mascota = renglon['pet_name']
                if llave not in diccionario:
                    diccionario[llave] = {}
                    diccionario[llave][mascota] = renglon
                else:
                    diccionario[llave][mascota] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario

def crear_lista_emails(usuarios:dict)->list:
    lista = []
    for usuario in usuarios:
        lista.append(usuarios[usuario]['email'])
    return lista

def crear_lista_mascotas(file:str)->list:
    lista = []
    try:
        with open(file,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                lista.append(renglon['tipo'])
    except IOError:
        print(f"No se pudo abrir el archivo {file}")
    return lista