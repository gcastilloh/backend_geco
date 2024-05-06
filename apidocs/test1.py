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
    print(JSONtoken)


    #obtener corpus publicos a partir del token con token
    url = url_servidor+'apidocs/corpus/'
    headers = {'Authorization': 'Token ' + JSONtoken["token"]}

    response = requests.get(url, headers=headers )

    JSONdocsCorpus = response.json()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-'*50)
    print(JSONdocsCorpus)
    print('-'*50,'\n'*2)

if __name__ == '__main__':
   main()


