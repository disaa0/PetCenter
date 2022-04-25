import csv
import usuarios

def graba_diccionario(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh:

        lista_campos = obtiene_llaves(diccionario,llave_dict)
        print("lista_campos")
        print(lista_campos)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        rows = []
        for llave, valor_d in diccionario.items():
            print("1")
            print(llave, valor_d)
            d = { 'username':llave}  #aquí va llave_dict
            for key,value in valor_d.items():
                print("2")
                print(key,value)
                d[key] = value
            rows.append(d)
        dw.writerows(rows) 

def obtiene_llaves(diccionario:dict,llave_dicc:str)->list:
    lista = [ llave_dicc ]
    llaves = list(diccionario.keys())
    
    k = llaves[0]
    diccionario_adentro = diccionario[k]

    lista_dentro =  list(diccionario_adentro.keys())
    lista.extend(lista_dentro)
    print(lista)
    return lista

my_dict = usuarios.lee_diccionario_usuarios('db/users.csv')
graba_diccionario(my_dict,'username','db/users.csv')