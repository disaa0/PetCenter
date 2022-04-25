import csv

from otros import graba_diccionario

def update_users_file(dic:dict, file:str):
    graba_diccionario(dic, 'username', file)

def lee_diccionario_usuarios(archivo:str)->dict:
    diccionario = {}
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['username']
                diccionario[llave] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario

def crear_lista_emails(usuarios:dict)->list:
    lista = []
    for usuario in usuarios:
        lista.append(usuarios[usuario]['email'])
    return lista
