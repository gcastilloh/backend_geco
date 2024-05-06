from django.db import models
from django.conf import settings

from biblioteca import DocumentoYaExistenteException
from .proyecto import *
from .metadato import *
from .archivo_adjunto import *

class Documento(models.Model):
    '''
    Un documento es un texto que se incorpora al proyecto, el texto original y el etiquetado (*tagged text*) se 
    almacenan en archivos diferentes dentro del ``repositorio`` del proyecto. 
    Se ha agregado un ``check_sum`` del archivo a fin de verificar que el documento almacenado 
    en el ``repositorio`` no sea modificado de maneraa externa al sistema, por ejemplo por un usuario con acceso al 
    servidor y al directorio del respositorio.

    Nota para el desarrollador: el constraint unique en el título se ha cambiado a false, para que se puedan subir
    varios documentos con el mismo nombre en diferentes proyectos.
    '''    
    proyecto = models.ForeignKey('Proyecto', on_delete = models.CASCADE,null=False)
    
    # archivo corresponde a la url a partir de /repos/...
    archivo = models.CharField(max_length = 1024, help_text = 'archivo estandarizado donde se encuentra el documento en el repositorio')
    archivo_original = models.CharField(max_length = 1024, help_text = 'nombre original del archivo con el que se subió a GECO (el del usuario)')
    derechos = models.BooleanField(default=True,help_text='¿El documento tiene derechos de autor?')
    agrupamiento = models.IntegerField(default=0)
    responsable_creacion = models.ForeignKey('UsuarioGeco',related_name='responsable_creacion',on_delete=models.SET_NULL,null=True)
    fecha_creacion = models.DateTimeField(verbose_name='fecha de creacion')
    responsable_modificacion = models.ForeignKey('UsuarioGeco',related_name='responsable_modificacion',on_delete=models.SET_NULL,null=True)
    fecha_modificacion = models.DateTimeField(verbose_name='fecha de modificacion',null=True,blank=True)
    check_sum = models.IntegerField(verbose_name='código verificador',default=0,editable=False)

    metadatos = models.ManyToManyField('Proyecto_metadato',through='Documento_metadato',related_name='documentos')
    
    class Meta:
        ordering = ["proyecto","archivo_original"]
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        constraints = [models.UniqueConstraint(fields=["archivo_original", "proyecto"], name='unique_file')]
        indexes = [
            models.Index(fields=['proyecto','archivo_original']),
        ]
        # UniqueConstraint(fields=["directorio","nombre"], name='unique_directoy_and_name')     
        #revisr un poco mas UniqueContraint y CheckConstraint para restringir la insercion de datos

    # eliminamos espacios al inicio y al final antes de instertar el dato
    # crea automáticamente el archivo etiquetado del documento agregado
    def save(self, *args, **kwargs):
        self.archivo_original = self.archivo_original.strip()
        # if Documento.objects.filter(proyecto=self.proyecto, archivo_original=self.archivo_original).exists():
        #     raise DocumentoYaExistenteException(f'El documento {self.archivo_original} ya existe en el corpus')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        dir_repositorio_proyecto = self.proyecto.getPathRepositorio()
        FS = FileSystemStorage(location=dir_repositorio_proyecto, file_permissions_mode=0o664)

        # gch 2023 tuve que implementar el borrado de los archivos adjuntos aquí porque aunque está habilitado el cascade y eperaba que se llamara
        # al método delete de Archivo_adjunto automáticamente ESO NO SUCEDE, si se borra la entrada de la base pero SIN LLAMAR 
        # al delete de Archivo_adjunto, (supongo que por razones de eficiencia se emplean la facilidades del manejador de bd)

        # Elimina archivos adjuntos
        for a in Archivo_adjunto.objects.filter(documento=self):
            a.delete()

        # Elimina el archivo principal
        archivo_repo = self.archivo
        if FS.exists(archivo_repo):
            FS.delete(archivo_repo)

        # Elimina el archivo .tag si existe
        fileNameTagged = archivo_repo + ".tag"
        if FS.exists(fileNameTagged):
            FS.delete(fileNameTagged)

        # Finalmente, elimina el objeto actual
        super().delete(*args, **kwargs)
        #print(f'Documento {self.archivo_original} ({self.archivo}) borrado')



    def __str__(self):
        return f"{self.proyecto} {self.archivo_original}"

    #regresa el nombre del archivo con todo y ruta física desde /
    def getArchivoConPath(self):
        return f"{self.proyecto.getPathRepositorio()}{self.archivo}"

    #regresa el nombre del archivo etiquetado (terminacion .tag SIEMPRE) con todo y ruta física desde /
    def getArchivoEtiquetadoConPath(self):
        return f"{self.getArchivoConPath()}.tag"

    #regresa el nombre del archivo con todo y URL tomando como base la MEDIA_URL
    def getArchivoConMediaURL(self):
        return f"{settings.MEDIA_URL}{self.proyecto.repositorio}/{self.archivo}"

    #regresa el nombre del archivo_etiquetado (terminacion .tag SIEMPRE) con todo y URL tomando como base la MEDIA_URL
    def getArchivoEtiquetadoConMediaURL(self):
        return f"{self.getArchivoConMediaURL()}.tag"
    

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------

   
    def getRenglonMetadatos(self,no_disponible='valor desconocido'):
        # obtiene la lista de metadatos del proyecto ordenada con base en el tipo de metadato

        metas = list(self.proyecto.metadatos.all().order_by('id'))
        dic = {}

        for x in self.documento_metadatos.all():
            dic[x.proyecto_metadato.metadato] = {'valor':x.valor,'proyecto_metadato_id':x.proyecto_metadato.id}

        ren = []
        for m in metas:
            dc = {}
            if m in dic.keys():
                dc['proyecto_metadato_id'] = dic[m]['proyecto_metadato_id']
                dc['valor'] = dic[m]['valor']
            else:
                dc['proyecto_metadato_id'] = Proyecto_metadato.objects.get(metadato=m, proyecto=self.proyecto).id
                dc['valor'] = no_disponible
            ren.append(dc)
        return ren


    def getDocInfoRemasterizado(self):
        '''obtiene los archivos asociados a un documento'''

        datosMetadatos = self.getRenglonMetadatos()
        diccionarioMetadatos = {
            #"titulo": 'aqui debe ir el metadato titulo???', pero titulo es un metadato
            "archivo_original": self.archivo_original,
            "archivosAsociadosTXT": [],
            "archivosAsociadosAudio": [],
            "datosMetadatos": datosMetadatos,
            "link": self.getArchivoConMediaURL(),
            "idDoc": self.id,
            "idCorpus": self.proyecto.pk
        }

        

        return diccionarioMetadatos

    def getDocInfo(self):


        res = []
        for m in self.documento_metadatos.all().order_by('proyecto_metadato__id'):
            res.append({'proyecto_metadato_id': m.proyecto_metadato.id, 'valor' : m.valor})

        return res

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #--------------------------------------------------------------






    # obtiene los metadatos del documento a actualizar
    # 
    def getActualizar(self):
        '''
        Para el documento en cuestion se:
             'meta' : lista de los valores de metadatos (sin sus nombres)
             'archivo': el titulo....
        '''

        # recupera el diccionario de ids de metadatos para ese proyecto
        metadatosProyecto = Proyecto_metadato.objects.filter(proyecto=self.proyecto).order_by("metadato_id")
        res = []
        for m in metadatosProyecto:
            v =  list(Documento_metadato.objects.filter(documento=self,proyecto_metadato=m).values_list("valor",flat='True'))
            if len(v) == 0:
                # por alguna razon no existe una entrada para ese metadato en la tabla de Documento_metadatos
                # por ejemplo se agregaron nuevos metadados???
                # agraga la entrada a la tabla Documento_metadatos asignado como valor  ""
                # todo: ojo falta preparar para cuando se pueda usar un catalogo (indice)
                y = [m,self,0,""]
                Documento_metadato.objects.create(
                    proyecto_metadato = m,
                    documento = self,
                    indice = 0,
                    valor = "",
                )
                res.append("")
            else:
                res.append(v[0])

                


        # for dms in self.documento_metadatos.all().order_by('proyecto_metadato_id'):
        #     if dms.valor == '0':
        #         consulta = Metadato_opcion.objects.get(id=dms.indice)
        #         res.append(consulta.opcion)
        #     else:
        #         res.append(dms.valor)

        dic = {
            "meta": res,
            #"archivo": self.titulo
            "archivo": "no estoy seguro que va aqui"
        }

        '''

        md	
            <Documento_metadato: Documento_metadato object (501)>
        res	
            ['Español',
            'Anécdota Hadita FC Cintura           ',
            'Cesar ',
            '2021',
            'Foros ',
            'SexoMéxico ',
            'http://boards1.melodysoft.com/SEXOMEXICO/anecdota-haditas-fc-cintura-157378.html',
            'Comportamiento '
            ]
        self	
            <Documento: Corpus de las Sexualidades de México Anecdota_Hadita_FC_Cintura.txt>

        dic	
            {'archivo': 'Anecdota_Hadita_FC_Cintura.txt',
            'meta': ['Español',
                    'Anécdota Hadita FC Cintura           ',
                    'Cesar ',
                    '2021',
                    'Foros ',
                    'SexoMéxico ',
                    'http://boards1.melodysoft.com/SEXOMEXICO/anecdota-haditas-fc-cintura-157378.html',
                    'Comportamiento ']
            }
            
                        
        '''
        return dic

class Documento_metadato(models.Model):

    proyecto_metadato = models.ForeignKey(
        'Proyecto_metadato', related_name='documento_metadatos', on_delete=models.CASCADE, null=True, blank=True)
    documento = models.ForeignKey(
        'Documento', related_name='documento_metadatos', on_delete=models.CASCADE, null=True)

    indice = models.IntegerField(blank=True, verbose_name='indice',
                            help_text='indice de la opción correspondiente al metadato asociado para el documento')
    valor = models.CharField(max_length=256, blank=True, verbose_name='valor',default='',
                            help_text='Valor asignado al metadato para el documento')

    class Meta:
        verbose_name = 'metadato del documento'
        verbose_name_plural = 'metadatos del documento'


    # eliminamos espacios al inicio y al final antes de instertar el dato
    # crea automáticamente el archivo etiquetado del documento agregado
    def save(self, *args, **kwargs):
        if isinstance(self.valor, str):
            self.valor = self.valor.strip()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'[{self.proyecto_metadato}] {self.documento}: "{self.valor}" '


    def getInfo(self):
        return {'proyecto_metadato_id': self.proyecto_metadato.id, 'valor' : self.valor}

# sm = Documento_metadato.objects.filter(proyecto_metadato__proyecto=4)
# d = sm[0]
# doc = d.documento
# metas = doc.metadatos_documentos.all()
# metas = doc.metadatos_documentos.all().order_by('proyecto_metadato__id')
# metas[0]
# <Documento_metadato: Documento_metadato object (128)>
# >>> for m in metas:
# ...    m.getInfo()
# ... 


