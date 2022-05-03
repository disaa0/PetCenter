from datetime import date, datetime
import csv

def graba_diccionario(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh:

        lista_campos = obtiene_llaves(diccionario,llave_dict)
        #print("lista_campos")
        #print(lista_campos)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        for llave, valor_d in diccionario.items():
            #print("1")
            #print(llave, valor_d)
            d = { 'username':llave}  #aquí va llave_dict
            for key,value in valor_d.items():
                #print("2")
                #print(key,value)
                d[key] = value
            rows.append(d)
        #print(rows)
        dw.writerows(rows) 

def obtiene_llaves(diccionario:dict,llave_dicc:str)->list:
    lista = [ llave_dicc ]
    llaves = list(diccionario.keys())
    
    k = llaves[0]
    diccionario_adentro = diccionario[k]

    lista_dentro =  list(diccionario_adentro.keys())
    lista.extend(lista_dentro)
    #print(lista)
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