Instrucciones:

Para la base de dato:

Instalar postgres, y crear el usuario y la base de datos

create user backend_user with password "test2024";
create database backend_geco with owner "test2024"

hacer la migracion de los modelos en django
python manage.py migrate

importar los datos de prueba a la base de postgres:

en powershell (consola de vscode):
$env:PYTHONIOENCODING="utf-8"; python manage.py loaddata datos.json



Nota: Los datos de prueba presentan problemas con la codificación, es debido a que los fuente se migraron de linux a windows, 
pero ya en produccion este detalle no se tendrá