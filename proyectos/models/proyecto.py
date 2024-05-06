#--- inicial

# todo: establecer un uuid como id del proyecto
# todo: id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Identificador único del proyecto en todo Geco 4.0')

from django.db import models
from django.conf import settings
from .tipo_colaboracion import Tipo_colaboracion
from .colaborador import Colaborador_proyecto
from django.utils.text import slugify

from biblioteca.funciones_cadenas import randomString

# 
# Proyectos.create()
# u = UsuarioGeco.objects.get(id=33) <--- UsuarioGeco
# u.nombre
# u.usuario
# u.usuario.mail
# p = Proyectos.objects.filter(propietario=u)  <--- QuerySet
# p.query()
# p.filter(es_paralelo=True)   <--- QuerySet
# p.filter(es_publico)         <--- QuerySet

#-------------------------------------------------------------------------------------------------------------------
# ojo para crear una asociacion de un  colaborador con un proyecto:
# super_pep_amount = ToppingAmount.objects.create(pizza=super_pep, topping=pepperoni, amount=ToppingAmount.DOUBLE)
#-------------------------------------------------------------------------------------------------------------------


def ceateRepositorioName():
        return randomString(15)

class Proyecto(models.Model):
    # Definimos la longitud máxima como una constante
    NOMBRE_MAX_LENGTH = 200

    ''' La unidad básica es el ``Proyecto`` por medio de este se representa el Corpus (ya sea paralelo o no). `
    El proyecto tiene asociado un grupo de colaboradores, dado por la relación **proyectos.Colaborador_proyecto**. 

    En términos de uso los proyectos pueden ser ``públicos`` o ``privados``.
    
    Los ``proyectos públicos`` pueden visualizarse sin necesidad de tener algun grado de colaboración mientras que para los
    ``proyectos privados`` es necesario que se tenga algun grado de **grado de colaboración** que determinará qué acciones pueden 
    llevarse a cabo en el Proyecto

    Ordenado originalmente por ``nombre``
    '''
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH, unique=True, verbose_name='nombre del proyecto',help_text='nombre del proyecto para el corpus')
    ''' nombre del proyecto ``char(128)`` ``(u,nn)``
    '''

    nombre_enlace = models.SlugField(max_length=NOMBRE_MAX_LENGTH,unique=True)
    ''' nombre a utilizar en el enlace que hace referenica al proyecto dentr de geco para un contexto deconsula del corpus'''
    ''' la funcion genera_enlaces() que definí para manage.py genera los enlaces para quellos proyectos que no tengan aun un enlace'''

    descripcion = models.TextField(
        verbose_name='descripción', help_text='breve descripción del proyecto')
    ''' ``text`` descripción general de proyecto (**o**)
    '''  
    cita = models.TextField(
        null=True, verbose_name='cita', help_text='Forma de citar el proyecto')
    ''' ``text`` forma de citar el proyecto (**o**)
    '''        
    colaboradores = models.ManyToManyField('UsuarioGeco', through='Colaborador_proyecto', related_name='proyectos',)
    ''' ``ManyToMany(UsuarioGeco,Colaborador_proyecto,proyectos)``
    Establece quién colabora en el proyecto mediante una relación muchos-muchos con atributos propios en la relación 
    **Colaborador_proyecto**. Con esto podremos podemos perguntar cosas como:

    ¿cuáles son los colaboradores de un proyecto?:: 

        proyectox.colaboradores.all()

    Consulte la información sobre las realciones many-to-many `aquí <https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/>`_.
    '''    

    metadatos = models.ManyToManyField('Metadato', through='Proyecto_metadato', related_name='proyectos')
    ''' ``ManyToMany(Metadato,Proyecto_Metadato,proyectos)``
    estableciendo en ``Proyecto_metadato`` qué metadato es obligatorio en el proyecto. 
    
    Con esto podremos podemos perguntar cosas como:

    ¿cuáles son los metadatos del proyecto con pk=1?:: 

        proyectox=Proyecto.objects.get(pk=1)
        proyectox.metadatos.all()
    
    ¿cuáles son los proyectos que contienen el metadato con pk=1?::

        meta = Metadato.objects.get(pk=1)
        meta.proyectos.all()

    Consulte la información sobre las realciones many-to-many `aquí <https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/>`_.
    '''
    aplicaciones = models.ManyToManyField('Aplicacion', through='Proyecto_aplicacion', related_name='proyectos')

    ''' ``ManyToMany(Aplicacion,Proyecto_aplicacion,proyectos)`` 
    estableciendo en ``Proyecto_aplicacion`` qué aplicaciones son aplicables para el proyecto. 
    
    Con esto podremos podemos perguntar cosas como:

    ¿cuáles son las aplicaciones del proyecto con pk=1?:: 

        proyectox=Proyecto.objects.get(pk=1)
        proyectox.aplicaciones.all()
    
    ¿cuáles son los proyectos que pueden ejecutarse con la aplicaion con pk=1?::

        a = Aplicacion.objects.get(pk=1)
        a.proyectos.all()

    Consulte la información sobre las realciones many-to-many `aquí <https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/>`_.
    '''
    repositorio = models.CharField(max_length=256, editable=False, unique=True, default=ceateRepositorioName)
    ''' ``char(256)`` directorio donde se almacenarán los documentos, se autogenera por medio de la funcion ``ceateRepositorioName``
    El nombre del repositorio 8directorio) debe ser único.
    '''
    activo = models.BooleanField(default=True, help_text='habilitar para indicar que el proyecto está activo')
    ''' ``boolean(False)`` bandera que incia si el proyecto está activo. Los proyectos se desactivan cuando 
    el propietario *"borra"* el proyecto, un proyecto desactivado no se muestra al usuario, sólo el administrador del 
    sistema puede ver un proyecto *"Borrado"* y un proceso especial debería borrar fisicamente el proyecto y su repositorio
    '''
    es_publico = models.BooleanField(default=False, help_text='habilitar para indicar que el proyecto es público (privado en caso contrario)')
    ''' ``boolean(False)`` establece si un proceso es público, es decir puede ser consultado (pero no alimentado) por cualquier persona
    '''
    es_paralelo = models.BooleanField(default=False, help_text='habilitar para indicar que será un corpus paralelo')
    ''' ``boolean(False)`` un proyecto puede ser paralelo o no, en el primer caso es necesario proporcionar dos o más documentos 
    por cada entrada a fin de poder comparar dichos documentos. 
    **Los documentos de un corpus paralelo deben tener el mismo número de reglones**
    '''
    es_colaborativo = models.BooleanField(default=False, help_text='habilitar para indicar que será un corpus colaborativo')
    ''' ``boolean(False)`` un proyecto puede ser colaborativo o no, en el primer solo el propietario podrá trabajar en el corpus
    en caso de ser True el propietario pordrá establecer colaboradores que trabajarán en el corpus. 
    '''
    creacion = models.DateTimeField(auto_now_add=True, editable=False)
    ''' ``dateTime(now)`` fecha de cración del proyecto
    '''
    fecha_borrado = models.DateTimeField(auto_now_add=False, editable=False, null=True, blank=True)
    ''' ``dateTime`` fecha en la que el proyecto fue *"borrado"*, (``activo = False``)
    '''

    #    __none_user_id__ = UsuarioGeco.objects.filter(user='__none_user__')

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'
        indexes = [
            models.Index(fields=['nombre']),
        ]

    # eliminamos espacios al inicio y al final antes de instertar el dato
    def save(self, *args, **kwargs):
        # Generar el slug a partir del nombre si no está presente
        if not self.nombre_enlace:
            self.nombre_enlace = slugify(self.nombre)        
        self.nombre = self.nombre.strip()
        super().save(*args, **kwargs)          

    def __str__(self):
        ''' regresa el nombre del proyecto'''
        return self.nombre

    def getColaboradores(self):
        ''' regresa una lista con las tuplas ``(id,colaborador)`` los colaboradores ACTIVOS del proyecto 
        '''
        res = []
        for ca in self.colaborador_atributos.all():
            if ca.activo == 1:
                res += [(ca.tipo_colaborador.id,ca.tipo_colaborador.tipo, ca.colaborador, ca)]
        return res

    def propietario(self):
        tipo_propietario = Tipo_colaboracion.objects.get(tipo='propietario')
        for c in Colaborador_proyecto.objects.filter(proyecto=self):
            if c.tipo_colaborador == tipo_propietario:
                return c.colaborador
        return '¿desconocido?'

    def tiene_derechos_descarga(self,usuario):
        if not usuario:
            if self.es_publico:
                return True
            return False
        colabs = self.getColaboradores()
        for c in colabs:
            if usuario==c[2]:
                return True
        return False

    def getPathRepositorio(self):
        return f"{settings.MEDIA_ROOT}{self.repositorio}/"
    
    def getMetadatos(self):
      '''
      obtiene los nombres metados y su ids asociados al proyecto. 
      NOTA: Los ids son los que corresponden al modelo Proyecto_metadato
      '''
      datos = Proyecto_metadato.objects.filter(proyecto=self).order_by('id').values_list('id','metadato__metadato')
      # con el value_list me ahorre todo este código, observa que metadato__metadato me entrega el atributo metadato del modelo metadato
      # no es lo mismo metadato_id que metadato__id 
      # proyecto_metadatos = Proyecto_metadato.objects.filter(proyecto=self).order_by('id')
      # datos = []
      # for pm in proyecto_metadatos:
      #    datos.append([pm.id, pm.metadato.metadato])
      # return datos
      return datos


   

   
    

class Proyecto_adjunto(models.Model):
    OPCIONES_TIPO = ((0, 'Texto'), (1,'Multimedia'), (2,'Otro (pdf, doc, xls, etc'))

    '''
    Establece una relación *muchos-a-muchos* entre un **Proyecto** y un **archivo adjunto**. 
    Se ha definido una *constraint* para que la combinación ``proyecto`` + ``nombre`` . 
    '''
    proyecto = models.ForeignKey('Proyecto', related_name='adjunto_proyecto', on_delete=models.CASCADE, null=True)
    descriptor = models.CharField(max_length= 128, unique = False, help_text = 'descriptor del archivo adjunto')
    tipo = models.IntegerField(unique=False, choices=OPCIONES_TIPO)

    pass

#-----------------------------------------------------------------------------------------------
# esta clase es un -custom "through" model- empleado en la realción Proyecto-Metadato
# ok gch

class Proyecto_metadato(models.Model):
    '''
    Establece una relación *muchos-a-muchos* entre un **Proyecto** y un **Metadato**. 
    Se ha definido una *constraint* para que la combinación ``proyecto`` + ``metadato`` sea único y sea el orden original empleado. 
    '''
    proyecto = models.ForeignKey('Proyecto', related_name='metas_proyecto', on_delete=models.CASCADE, null=True)
    ''' ``(fk)`` **Proyecto** sobre el cual un **Metadato** es válido. '''
    metadato = models.ForeignKey('Metadato', related_name='metas', on_delete=models.CASCADE, null=True, blank=True)
    ''' ``(fk)`` **Metadato** que es valido para un **Proyecto**. '''
    es_obligatorio = models.BooleanField(default=False)
    ''' ``boolean(False)`` establece si el **Metadato** es obligatorio para cualquier documento dado de alta en el **Proyecto**.
    Todo metadato con los atributos  ``es_general=True`` y ``es_obligatorio_general=True`` simultáneamente **obligatoriamente** debe 
    tener ``es_obligatorio=True`` (es decir no es una opción del usuario). En cualquier otro caso el *propietario* determinará cuál
    metadato es obligatorio (``es_obligatorio=True``) y cuál no en su proyecto (``es_obligatorio=True``) .
    '''
    

    class Meta:
        ordering = ['proyecto', 'metadato']
        verbose_name = 'Metadatos del proyecto'
        verbose_name_plural = 'Metadatos de los proyectos'
        constraints = [
            models.UniqueConstraint(fields=["proyecto","metadato"], name='unique_proyecto_metadato'),
        ]


    def __str__(self):
        ''' regresa el nombre del proyecto el metadato y opcionalmente 
        un letrero que indica si ese metadato es obligatorio para el proyecto
        '''
        if self.es_obligatorio:
#            return f'{self.proyecto.nombre} {self.metadato.metadato} (obligatorio)'
            return '{} {} (obligatorio)'.format(self.proyecto.nombre,self.metadato.metadato)

#        return f'{self.proyecto.nombre} {self.metadato.metadato}'
        return '{} {}'.format(self.proyecto.nombre,self.metadato.metadato)

# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------



class Proyecto_aplicacion(models.Model):
    proyecto = models.ForeignKey(
        'Proyecto', related_name='proyecto_aplicaciones', on_delete=models.CASCADE, null=True)
    aplicacion = models.ForeignKey(
        'Aplicacion', related_name='proyecto_aplicaciones', on_delete=models.CASCADE, null=True, blank=True)
