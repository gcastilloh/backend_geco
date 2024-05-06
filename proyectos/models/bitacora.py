from django.db import models

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .proyecto import Proyecto

'''
Usamos una señal que se activa justo antes de que se elimine un objeto Proyecto. 
Esta señal obtiene todas las instancias de Bitacora relacionadas con el proyecto 
que se está eliminando y actualiza su campo.

 En la función actualizar_nombre_proyecto, filtramos todas las entradas de Bitacora 
 que están relacionadas con el proyecto que se va a eliminar y actualizamos 
 el campo nombre_proyecto con el nombre del Proyecto.

 La idea es que cuando se borra un proyecto se elimina el id, lo que haria que 
 la bitacora dejara de recordar el nombre del proyecto (asociado a través de id)
 y llevaria a la bitacora a un estado de inconsistencia, al agregar 
 el campo nombre de proyecto se permitirá que ahi se quede registrado el nombre del
 proyecto, aunque ya no exista el objeto correspondiente en el modelo Proyecto
'''

class Bitacora(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, editable=False)
    actividad = models.CharField(max_length=512, null=False)
    usuario = models.ForeignKey(
        'UsuarioGeco', on_delete=models.CASCADE, null=False)
    proyecto = models.ForeignKey(
        'Proyecto', on_delete=models.SET_NULL, null=True, blank=True)
    nombre_proyecto = models.CharField(max_length=256, null=True, blank=True)    

    def __str__(self):
#        return f'{self.usuario.usuario}({self.proyecto.nombre}): {actividad}'
        if self.proyecto:
          return '{} {}({}): {}'.format(self.fecha,self.usuario.usuario,self.proyecto.nombre,self.actividad)
        else:
          return '{} {}({}): {}'.format(self.fecha,self.usuario.usuario,"?",self.actividad)

'''
Usamos una señal que se activa justo antes de que se elimine un objeto Proyecto. 
Esta señal obtiene todas las instancias de Bitacora relacionadas con el proyecto 
que se está eliminando y actualiza su campo.

 En la función actualizar_nombre_proyecto, filtramos todas las entradas de Bitacora 
 que están relacionadas con el proyecto que se va a eliminar y actualizamos 
 el campo nombre_proyecto con el nombre del Proyecto.

 La idea es que cuando se borra un proyecto se elimina el id, lo que haria que 
 la bitacora dejara de recordar el nombre del proyecto (asociado a través de id)
 y llevaria a la bitacora a un estado de inconsistencia, al agregar 
 el campo nombre de proyecto se permitirá que ahi se quede registrado el nombre del
 proyecto, aunque ya no exista el objeto correspondiente en el modelo Proyecto
'''

from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Proyecto)
def actualizar_nombre_proyecto(sender, instance, **kwargs):
    Bitacora.objects.filter(proyecto=instance).update(nombre_proyecto=instance.nombre)