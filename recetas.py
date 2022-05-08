import csv
from otros import graba_diccionario_de_diccionarios_lista, obtiene_llaves_ddl, graba_diccionario

def update_prescriptions_file(dic:dict, file:str):
    graba_diccionario_de_diccionarios_lista(dic, file)

def lee_diccionario_recetas(archivo:str)->dict:
    diccionario = {}
    #recetas[user] ->user[id_receta]->[wqdqd,dqdqdqd]
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave1 = renglon['username']
                llave2 = renglon['prescription_id']
                if llave1 not in diccionario:
                    diccionario[llave1] = {}
                    diccionario[llave1][llave2] = []
                if llave2 not in diccionario[llave1]:
                    diccionario[llave1][llave2] = []
                diccionario[llave1][llave2].append(renglon)
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario

def update_drugs_file(dic:dict, file:str):
    graba_diccionario(dic, file)

def lee_diccionario_medicinas (archivo:str)->dict:
    diccionario = {}
    #medicinas[id]->{campo:cosa}
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['code']
                if llave not in diccionario:
                    diccionario[llave] = {}
                diccionario[llave] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario

def crear_lista_medidas(file:str)->list:
    lista = []
    try:
        with open(file,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                lista.append(renglon['medida'])
    except IOError:
        print(f"No se pudo abrir el archivo {file}")
    return lista

#diccionario_recetas = lee_diccionario_recetas('db/prescriptions.csv')
#print(diccionario_recetas)
