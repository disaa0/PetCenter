import csv
from otros import graba_ddd, graba_diccionario_de_diccionarios

def update_atencion_file(dic:dict, file:str):
    graba_ddd(dic, file)

def lee_diccionario_atencion(archivo:str)->dict:
    diccionario = {}
    #atencion[user] ->user[pet] -> pet[fecha]
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave1 = renglon['username']
                llave2 = renglon['pet_name']
                llave3 = renglon['date']
                if llave1 not in diccionario:
                    diccionario[llave1] = {}
                if llave2 not in diccionario[llave1]:
                    diccionario[llave1][llave2] = {}
                diccionario[llave1][llave2][llave3] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario

