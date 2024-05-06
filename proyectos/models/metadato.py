from django.db import models

class Metadato(models.Model):
    ''' Un ``Metadato`` es un etiqueta que se adjunta a un documento(s) cuando es agregado al Proyecto.
    Los metadatos de un proyecto se definen en el momento en que se crea el proyecto.
    Para fines de usabilidad en metadatos personalizados se cambió a unique=False (originalmente True)
    '''
    metadato = models.CharField(max_length=128, unique=False,verbose_name='metadato', help_text='Metadato aplicable a un documento')
    '''
    ``char(128)`` Título del metadato
    '''
    abreviacion = models.CharField(max_length=10, unique=False, null=True, verbose_name='abreviación', help_text='abreviación asociada al metadato')
    '''
    ``char(10)`` Abreviación del metadato
    '''
    explicacion = models.TextField(max_length=256, blank=True, null=True, verbose_name='explicación',help_text='explicación breve de lo que significa el metadato')
    '''
    ``char(256)`` Descripción del significado de el metadato
    '''
    es_general = models.BooleanField(default=False)
    '''``(boolean:False)`` Los metadatos pueden:
        - provenir de una lista incial (``es_general=True``) 
        - creados explicitamente para un Proyecto en particular (``es_general=False``)
    '''    
    es_obligatorio_general = models.BooleanField(default=False)
    '''``(boolean:False)``  Aquellos metadatos que pertenzcan a la lista inicial de metadatos (metadatos generales) diponibles son:
        - obligatorios: todos los proyectos deben poseer ese metado (``es_obligatorio_general=True``)
        - optativos: aquellos que el propietario puede decidir agregar a su Proyecto (``es_obligatorio_general=False``). 

    El sistema automáticamente debe agregar el metadato general que es obligartorio a la relación ``Proyecto_Metadatos``.
    '''
    es_catalogo = models.BooleanField(default=False, help_text='determina si este metadato es un catalogo')
    '''
    ``(boolean:False)`` Estilo del metadato:
        - Texto libre: el colaborador escribe un texto (``es_catalogo=False``).
        - Catálogo: el colaborador elige una opción de varias posibles  (``es_catalogo=True``). 
    '''

    class Meta:
        ordering = ["metadato"]
        verbose_name = 'metadato'
        verbose_name_plural = 'metadatos'

    # eliminamos espacios al inicio y al final antes de instertar el dato
    def save(self, *args, **kwargs):
        self.metadato = self.metadato.strip()
        if self.abreviacion:
            self.abreviacion = self.abreviacion.strip()
        super().save(*args, **kwargs)         

    def __str__(self):
        ''' regresa el nombre, la abreviación y en su caso un identificador en caso de ser catálogo
        '''
        if self.es_catalogo:
#            return f'{self.metadato} [{self.abreviacion}] (catalogo)'
            return '{} [{}] (catalogo)'.format(self.metadato,self.abreviacion)
#        return f'{self.metadato} [{self.abreviacion}]'
        return f'{self.id}[{self.metadato},{self.abreviacion}]'

    def getOpciones(self):
        '''
        Si el metadatos es un catálogo entonces se entrega una lista de las opciones asociadas a él.
        '''
        if self.es_catalogo:
            return [Metadato_opcion.objects.filter(metadato=self.id)]

    
#gch ok
class Metadato_opcion(models.Model):
    '''
    Opciones que un Metadatos tipo catálogo ofrece.
    Se ha definido una *constraint* para que la combinación ``metadato+abreviacion`` sea única
    Se ha definido una *constraint* para que la combinación ``metadato+opcion`` sea única
    '''
    metadato = models.ForeignKey('Metadato', on_delete=models.CASCADE, null=False)
    ''' ``(fk)`` Metadato asociado a esta opción
    '''
    abreviacion = models.CharField(max_length=10, unique=False, verbose_name='abreviación', help_text='abreviación')
    ''' ``char(10)`` abreviación de la opción`` '''
    opcion = models.CharField(max_length=128, unique=False,verbose_name='opción', help_text='opciónes disponibles')
    ''' ``char(128)`` texto de la opción '''
    explicacion = models.TextField(blank=True, verbose_name='explicación',help_text='breve explicación del significado esta opción')
    ''' ``text`` breve explicación del significado de está opción'''

    class Meta:
        ordering = ['metadato', 'id']
        verbose_name = 'opcion del metadato'
        verbose_name_plural = 'opciones del metadato'
        constraints = [
            models.UniqueConstraint(fields=["metadato", "abreviacion"], name='abrevaiacion_unica'),
            models.UniqueConstraint(fields=["metadato", "opcion"], name='opcion_unica'),
        ]

    # eliminamos espacios al inicio y al final antes de instertar el dato
    def save(self, *args, **kwargs):
        self.abreviacion = self.nombre.abreviacion()
        self.opcion = self.opcion.strip()
        super().save(*args, **kwargs) 

    def __str__(self):
        ''' regresa el nombre del metadato y la opción asociada'''
#        return f'{self.metadato} ({self.opcion})'
        return '{} ({})'.format(self.metadato,self.opcion)

