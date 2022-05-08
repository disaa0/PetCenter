from datetime import date, datetime
import csv

def graba_diccionario(diccionario:dict,archivo:str):
    with open(archivo,'w') as fh:

        lista_campos = obtiene_llaves(diccionario)
        print(lista_campos)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        d = {}
        for llave, valor_d in diccionario.items():
            d = {}  #aquí va llave_dict
            for key,value in valor_d.items():
                d[key] = value
            rows.append(d)
        #print(rows)
        dw.writerows(rows) 

def obtiene_llaves(diccionario:dict)->list:
    lista = []
    for elemento, valores in diccionario.items():
        lista = valores.keys()
        break
    return lista


def graba_diccionario_de_diccionarios(diccionario:dict,archivo:str):
    with open(archivo,'w') as fh:
        lista_campos = obtiene_llaves_dd(diccionario)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        for el1 in diccionario.keys():
            for el2 in diccionario[el1].keys():
                d = {}
                for el3 in diccionario[el1][el2].keys():
                    #print(diccionario[el1][el2][el3])
                    d[el3] = diccionario[el1][el2][el3]
                rows.append(d)
        dw.writerows(rows)

def obtiene_llaves_dd(diccionario:dict)->list:
    llaves = []
    llaves_internas = []
    llaves_finales = []
    for elemento in diccionario.keys():
        llaves.append(elemento)
        break
    llave1 = llaves[0]
    for elemento in diccionario[llave1]:
        llaves_internas.append(elemento)
        break
    llave2 = llaves_internas[0]
    for elemento in diccionario[llave1][llave2]:
        llaves_finales.append(elemento)
    return llaves_finales

def graba_ddd(diccionario:dict,archivo:str):
    with open(archivo,'w') as fh:
        lista_campos = obtiene_llaves_ddd(diccionario)
        #print(diccionario)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        for el1 in diccionario.keys():
            for el2 in diccionario[el1].keys():
                for el3 in diccionario[el1][el2].keys():
                    d = {}
                    for elf in diccionario[el1][el2][el3].keys():
                        #print(diccionario[el1][el2][el3])
                        d[elf] = diccionario[el1][el2][el3][elf]
                    rows.append(d)
        dw.writerows(rows)

def obtiene_llaves_ddd(diccionario:dict)->list:
    llaves = []
    llaves1 = []
    llaves2 = []
    llaves_finales = []
    for elemento in diccionario.keys():
        llaves.append(elemento)
        break
    llave1 = llaves[0]
    for elemento in diccionario[llave1]:
        llaves1.append(elemento)
        break
    llave2 = llaves1[0]
    for elemento in diccionario[llave1][llave2]:
        llaves2.append(elemento)
    llave3 = llaves2[0]
    for elemento in diccionario[llave1][llave2][llave3]:
        llaves_finales.append(elemento)
    return llaves_finales

def graba_diccionario_de_diccionarios_lista(diccionario:dict,archivo:str):
    with open(archivo,'w') as fh:
        lista_campos = obtiene_llaves_ddl(diccionario)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        for el1 in diccionario.keys():
            for el2 in diccionario[el1].keys():
                for li in diccionario[el1][el2]:
                    d = {}
                    #print(diccionario[el1][el2][el3])
                    for lf,vf in li.items():
                        d[lf] = vf
                    rows.append(d)
        dw.writerows(rows)

def obtiene_llaves_ddl(diccionario:dict)->list:
    llaves_finales = []
    for key in diccionario.keys():
        l1 = key
        break
    for key in diccionario[l1].keys():
        l2 = key
        break
    
    for li in diccionario[l1][l2]:
        for k in li.keys():
            llaves_finales.append(k)
        break
    return llaves_finales

def crea_diccionario_clientes(diccionario_clientes:dict)->dict:
    diccionario_palabras = {}
    for id, usuario in diccionario_clientes.items():
        username = usuario['username']
        name = usuario['name']
        agrega_palabras(diccionario_palabras, username, usuario)
        agrega_palabras(diccionario_palabras, name, usuario)
        agrega_frases(diccionario_palabras, username, usuario)
        agrega_frases(diccionario_palabras, name, usuario)
    return diccionario_palabras

def limpia_texto(texto:str)->str:
    lista_simbolos = [',','.',';',':','/','(',')','-','_','?','¿','¡','!']
    for simbolo in lista_simbolos:
        texto = texto.replace(simbolo,'')
    return texto

def agrega_palabras(diccionario:dict,cadena:str, diccionario_pelicula:dict):
    minusculas = cadena.lower()
    cadena_limpia = limpia_texto(minusculas)
    palabras = cadena_limpia.split(' ')
    palabras.append(cadena_limpia)
    for palabra in palabras:
        if palabra not in diccionario:
            diccionario[palabra] = [diccionario_pelicula]
        else:
            diccionario[palabra].append(diccionario_pelicula)

def agrega_frases(diccionario:dict,frase:str, diccionario_pelicula:dict):
    minusculas = frase.lower()
    frase_limpia = limpia_texto(minusculas)
    palabras = frase_limpia.split(' ')
    lista_frase =[]
    for i, palabra in enumerate(palabras):
        if i+1 < len(palabras):
            dupla = [palabra, palabras[i+1]]
            lista_frase.append(dupla)
        if i+2 < len(palabra):
            triple = [palabra, palabra[i+1],palabra[i+2]]
            lista_frase.append(triple)
    for elemento in lista_frase:
        frase_compuesta = ' '.join(elemento)
        if frase_compuesta not in diccionario:
            diccionario[frase_compuesta] = [ diccionario_pelicula]
        else:
            diccionario[frase_compuesta].append(diccionario_pelicula)

def tiene_mascotas(mascotas:dict, usuario:str)->bool:
    ret = False
    if usuario in mascotas:
        for mascota, valores in mascotas[usuario].items():
            if valores['active'] == 'True':
                ret = True
                break
    return ret

def usuario_activo(usuarios:dict, user:str)->bool:
    ret = False
    if user in usuarios:
        if usuarios[user]['active'] == 'True':
            ret = True
    return ret