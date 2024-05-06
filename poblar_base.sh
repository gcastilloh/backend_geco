echo "sudo -u postgres pg_dump -d geco4 -t auth_permission --data-only > tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t auth_permission --data-only > tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t auth_user --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t auth_user --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t authtoken_token --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t authtoken_token --data-only >> tmp/respaldo.sql

echo "sudo -u postgres pg_dump -d geco4 -t proyectos_paisusuario --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_paisusuario --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_aplicacion --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_aplicacion --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_tipo_colaboracion --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_tipo_colaboracion --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_metadato_opcion --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_metadato_opcion --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_metadato --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_metadato --data-only >> tmp/respaldo.sql

echo "sudo -u postgres pg_dump -d geco4 -t proyectos_usuariogeco --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_usuariogeco --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto_aplicacion --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto_aplicacion --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto_metadato --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_proyecto_metadato --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_colaborador_proyecto --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_colaborador_proyecto --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_documento --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_documento --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_documento_metadato --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_documento_metadato --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_archivo_adjunto --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_archivo_adjunto --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_bitacora --data-only >> tmp/respaldo.sql"
echo "sudo -u postgres pg_dump -d geco4 -t escritorio_mensaje --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t escritorio_mensaje --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t proyectos_bitacora --data-only >> tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t proyectos_bitacora --data-only >> tmp/respaldo.sql
echo "sudo -u postgres pg_dump -d geco4 -t authtoken_token > tmp/respaldo.sql"
sudo -u postgres pg_dump -d geco4 -t authtoken_token --data-only >> tmp/respaldo.sql

echo "limpiando dato"
python tmp/adapt.py tmp/respaldo.sql tmp/datos.sql

echo "borrando bas"
rm db.sqlite3
echo "creando la base"
python manage.py migrate
sqlite3 db.sqlite3 < tmp/token.sql

echo "poblando la base"
sqlite3 db.sqlite3 < tmp/datos.sql

echo "Creando superusaurio"
python manage.py createsuperuser --username nuevoadmin  --email super@gmail.com 