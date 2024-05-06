from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from biblioteca import obtener_extension,obtener_extension,transforma_txt
from datetime import datetime

from proyectos.models import Archivo_adjunto
from proyectos.models import UsuarioGeco
from proyectos.models import Documento
from proyectos.models import Bitacora
from proyectos.models import Proyecto_metadato
from biblioteca import MetadatoObligatorioNotFoundException, ArchivoDocumentoNotFoundException
from proyectos.models import Documento_metadato


import os, uuid

def creaDocumentoTexto(usuarioActual, proyecto, archivoDocumento, banderaDerechosAutor, archivosAdjuntos, documentoMetadatos):
    """ 
    usuarioActual es el objeto del tipo UsuarioGeco
    Procesamiento para guardar archivo de texto en el repositorio
    archivoDocumento: entrada del tipo UploadedFile (obtenida cia request.FILES)
    banderaDerechosAutor: indica si el archivo está protegido por derechos de autor
    proyecto: corpus al que se agraga el documento
    metadatosDocumento: es un diccionario id_metadato_proyecto:valor. **OJO: EL id correponde a el id de la tabla proyecto_metadato**

    Se almacena el archivo
    Se crea el Documento en la base de datos
    Se crean las entradas en la bitacora
    Entrega el objeto Documento creado
    
    TODO: En esta funcion no se pueden enviar archivos adjuntos
    Esta función realiza las verificaciones pertinentes para validar la informacion recibida antes de salvar un documento

    """

    #verifica que archivo documento no esté vacio
    if not archivoDocumento or not isinstance(archivoDocumento,UploadedFile) or archivoDocumento.name.strip()=='':
        raise ArchivoDocumentoNotFoundException(f'No se proporcionó el documento o es incorrecto')

    # nombre del archivo que el usuario subió
    nombreArchivoOriginal = archivoDocumento.name

    # verifica que los metadatos obligatorios esten completos y los que no son obligatorios y falten sean agregados como espacios vacios
    # no se intenta guardar nada, solo verifica y corrige de ser posible si no levanta una excepcion. El almacenamiento en la BD es posterior
    # la verificacion es necesaria porque la solicitud pudo venir de una api de la cual no se tiene mucho control, si viene de la forma de GECO
    # deberia venir la lista completa de los metadatos y con los metadatos obligatorios completos

    proyectoMetadato = Proyecto_metadato.objects.filter(proyecto_id = proyecto.id).order_by('id')

    print(f'Metadatos: {documentoMetadatos}')
    for proy_meta in proyectoMetadato:
        print(f' {proy_meta.id} ')
        if proy_meta.metadato.metadato == 'Título principal':
            # si es el titulo principal y no está en la forma se asigna por omision el nombre del documento
            # estoes aplicable únicamente a envios de varios archivos, si es un solo archivo
            # forzosamente deberia venir el titulo
            if not proy_meta.id in documentoMetadatos:
                documentoMetadatos[proy_meta.id] = nombreArchivoOriginal
        elif proy_meta.es_obligatorio and not proy_meta.id in documentoMetadatos:
            # levanta una excepcion
            raise MetadatoObligatorioNotFoundException(f"El metadato obligatorio {proy_meta.id}: '{proy_meta.metadato.metadato}' no se encontró en el diccionario")
        elif not proy_meta.es_obligatorio and not proy_meta.id in documentoMetadatos:
            # agrega el metadato no obligatorio que no se proporcinó en la lista
            documentoMetadatos[proy_meta.id] = ''
        
    # FilesSystemStrorage es una clase de Django y su documentacion indica:
    # Saves a new file using the storage system, preferably with the name specified. 
    # ** If there already exists a file with this name name, the storage system may modify the filename as necessary to get a unique name. 
    # The actual name of the stored file will be returned.
    dir_repositorio_proyecto = proyecto.getPathRepositorio()
    FS = FileSystemStorage(location=dir_repositorio_proyecto,file_permissions_mode=0o664)

    # genera un nombre de manera aleatoria, este será el nombre con el que se almacenará
    # se mantiene la extension del archivo original
    # salva el archivo 
    
    nombre_repo = str(uuid.uuid4())+obtener_extension(nombreArchivoOriginal)
    nombre_repo = FS.save(nombre_repo, archivoDocumento)
    
    # ojo si el archivo original no es texto y tampoco es alguno de los que se pueden transformar
    # deja el archivo tal cual, lo que puede suponer errore... por ejemplo tratar de subir un .exe¿?
    # hace falta el manejo mas cudiadoso de este caso
    modificado, archivoRepoFinalConPath = transforma_txt(dir_repositorio_proyecto + nombre_repo)
    if modificado:
        # si se creo un archivo temporal para el documento y su transformacion borra el archivo inicial
        FS.delete(nombre_repo)  #elimina archivo desde el que se generó el .txt
    
    # nombre del archivo (sin path) tal como quedó grabado
    archivoRepoFinalTxt = os.path.split(archivoRepoFinalConPath)[1]

    # registra si el documento tiene derechos de autor
    # Guardando el documento en la BD
    nuevoDocumento = Documento.objects.create(
        archivo = archivoRepoFinalTxt,
        archivo_original = nombreArchivoOriginal,
        responsable_creacion = usuarioActual,
        responsable_modificacion = usuarioActual,
        fecha_creacion = datetime.now(tz=timezone.utc),
        fecha_modificacion = datetime.now(tz=timezone.utc),
        proyecto_id = proyecto.id,
        derechos = banderaDerechosAutor,
    )

    # Guarda los metadatos del documento
    for proy_meta in proyectoMetadato:
        Documento_metadato.objects.create(
            proyecto_metadato = proy_meta,
            documento = nuevoDocumento,
            valor = documentoMetadatos[proy_meta.id],
            indice = 0, # solo aplicará cuando se implementen metadatos lista
        )      

    # Registo en la bitácora: se crea el documento y se agrega el etiquetado

    Bitacora.objects.create(
        fecha = datetime.now(tz=timezone.utc),
        actividad = str("Agregó el documento: " + nombreArchivoOriginal),
        usuario = usuarioActual,
        proyecto_id = proyecto.id
    )

    # crea el archivo etiquetado del documento
    # si no se levanto la excepcion... 
    if not os.path.exists(nuevoDocumento.getArchivoEtiquetadoConPath()):
        etiquetar(nuevoDocumento.getArchivoConPath(), nuevoDocumento.getArchivoEtiquetadoConPath())     


    Bitacora.objects.create(
        fecha = datetime.now(tz=timezone.utc),
        actividad = str(f"Al agregar el documento {nombreArchivoOriginal} se creó automáticamente el documento etiquetado"),
        usuario = usuarioActual,
        proyecto_id = proyecto.id
    )               

    # para cada documento asocia los archivos adjuntos
    for adjunto in archivosAdjuntos:
         print(f'prcesando {adjunto.name}')
         guardar_adjunto(usuarioActual,proyecto,nuevoDocumento,adjunto)

    return nuevoDocumento


def guardar_adjunto(usuarioActual, proyecto, documento, archivo_adjunto):
    #Procesamiento para guardar archivo adjunto en el repositorio
    """ 
    Procesamiento para guardar archivo adjunto a un documento en el repositorio
    archivoDocumento: entrada del tipo UploadedFile (obtenida cia request.FILES)
    banderaDerechosAutor: indica si el archivo está protegido por derechos de autor
    proyecto: corpus al que se agraga el documento

    Se almacena el archivo
    Se crea el Documento en la base de datos
    Se crean las entradas en la bitacora
    Entrega el objeto Documento creado
    """
    
    dir_repositorio_proyecto = proyecto.getPathRepositorio()

    FS = FileSystemStorage(location=dir_repositorio_proyecto,file_permissions_mode=0o664)
    nombre_repo = str(uuid.uuid4())+obtener_extension(archivo_adjunto.name)        
    FS.save(nombre_repo, archivo_adjunto)
    print(f'original: {archivo_adjunto.name} repo: {nombre_repo}')
    adjunto = Archivo_adjunto.objects.create(documento=documento,archivo_original=archivo_adjunto.name, archivo=nombre_repo,derechos=documento.derechos)
    Bitacora.objects.create(
        fecha = datetime.now(tz=timezone.utc),
        actividad = f"Adjuntó al documento {documento.archivo_original} el archivo : {archivo_adjunto.name} ({nombre_repo})" ,
        usuario = usuarioActual,
        proyecto_id = proyecto.id
    )        
    return adjunto