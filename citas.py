import csv
from otros import graba_diccionario_de_diccionarios

def update_citas_file(dic:dict, file:str):
    graba_diccionario_de_diccionarios(dic, file)

def lee_diccionario_citas(archivo:str)->dict:
    diccionario = {}
    #mascotas[user] ->user[mascota]
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['username']
                mascota = renglon['start']
                if llave not in diccionario:
                    diccionario[llave] = {}
                    diccionario[llave][mascota] = renglon
                else:
                    diccionario[llave][mascota] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario