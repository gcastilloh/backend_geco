import os
import requests


def acortar_cadena(cadena, n):
    if len(cadena) <= n:
        return cadena  # La cadena es igual o más corta que n, no es necesario acortarla ni agregar "..."
    else:
        return cadena[:n] + "... continúa archivo ... "  # Agrega "..." al final de la cadena acortada

def main():
        #obtener token
    os.system('cls' if os.name == 'nt' else 'clear')
        
    url_servidor = 'http://127.0.0.1:8000/'

    url = url_servidor+'apidocs/get-token/'
    


    # Datos de autenticación (nombre de usuario y contraseña)
    data = {
          'username': 'usuario_anonimo',
          'password': '2024anonimo',
      }

    # Datos de autenticación (nombre de usuario y contraseña)
    data = {
          'username': 'gsierram',
          'password': 'test2024',
      }


    # Realiza una solicitud POST para obtener el token
    response = requests.post(url, data=data)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtiene el token del cuerpo de la respuesta
        token = response.json().get('token')
        print(f'Token de acceso: {token}')
    else:
        print('Error en la autenticación. Verifica las credenciales.')
        exit()

    JSONtoken = {'token': token}


    #obtener corpus publicos a partir del token con token
    url = url_servidor+'apidocs/corpus/'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}

    response = requests.get(url, headers=headers )

    JSONdocsCorpus = response.json()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-'*50)
    print(JSONdocsCorpus)
    print('-'*50,'\n'*2)

    # obtiene los corpus en los que el usuario del token tiene acceso porque colabora con él
    url = url_servidor+'apidocs/corpus/colabora'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(JSONdocsCorpus)
    print('-'*50,'\n'*2)


    id = 4
    # # obtiene los metadatos registrados para el corpus
    url = url_servidor+f'apidocs/corpus/{id}/meta'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(JSONdocsCorpus)
    print('-'*50,'\n'*2)

    if response.status_code == 404:
        print(response.json())
        print("La solicitud obtuvo un estado 404 (No encontrado).")


    # obtiene una lista de los documentos que se tienen registrados en el corpus
    id = 4
    url = url_servidor+f'apidocs/corpus/{id}'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(JSONdocsCorpus)
    print('-'*50,'\n'*2)    
    # if response.status_code == 404:
    #     print(response.json())
    #     print("La solicitud obtuvo un estado 404 (No encontrado).")
    # else:
    #     k = 0
    #     for d in JSONdocsCorpus['data']:
    #         k = k+1
    #         print(d['id'],d['archivo'])
    #         if (k==10):
    #             print('Continúan más archivos...')
    #             break
    #     print('-'*50,'\n'*2)   
    # print('-'*50,'\n'*2)

    #obtiene los valores de los metadatos para el documento proporcionado
    id = 4
    doc_id = 857
    url = url_servidor+f'apidocs/corpus/{id}/{doc_id}/meta'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    for d in JSONdocsCorpus['data']:
        print(d['id'],d['valor'])
    print('-'*50,'\n'*2)   


    # #obtiene el contenido del documento cuyo corpus y id se proporciona
    id = 4
    doc_id = 857
    url = url_servidor+f'apidocs/corpus/{id}/{doc_id}'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(JSONdocsCorpus['data'])
    # print(acortar_cadena(JSONdocsCorpus['data'],400))
    print('-'*50,'\n'*2)

    #obtiene el contenido del documento con etiquetado POS cuyo corpus y id se proporciona
    id = 4
    doc_id = 857
    url = url_servidor+f'apidocs/corpus/{id}/{doc_id}/pos'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(acortar_cadena(JSONdocsCorpus['data'],400))
    print('-'*50,'\n'*2)

    #obtiene la lista de ids de documentos adjuntos del documento cuyo corpus y id se proporciona
    id = 4
    doc_id = 857
    url = url_servidor+f'apidocs/corpus/{id}/{doc_id}/adjuntos'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    JSONdocsCorpus = response.json()
    print(acortar_cadena(JSONdocsCorpus['data'],400))
    print('-'*50,'\n'*2)


    #obtiene el contenido del documento adjunto cuyo corpus, documento y id se proporciona
    id = 4
    doc_id = 857
    adj_id = 114
    url = url_servidor+f'apidocs/corpus/{id}/{doc_id}/adjunto/{adj_id}'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}
    response = requests.get(url, headers=headers )
    print(response.status_code)
    JSONdocsCorpus = response.json()
    print(acortar_cadena(JSONdocsCorpus['data'],400))
    print('-'*50,'\n'*2)

if __name__ == '__main__':
   main()


