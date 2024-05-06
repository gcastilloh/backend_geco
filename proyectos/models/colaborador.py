#--- inicial


from django.db import models


#--------------

# esta clase permite implementar una relación many to many entre ptoyectos y colaboradores donde los colaboradores tienen permisos 
# ver tambien la declaracion ManyToMany en Proyecto
# ojo para crear una asociacion de un  colaborador con un proyecto:
# super_pep_amount = ToppingAmount.objects.create(pizza=super_pep, topping=pepperoni, amount=ToppingAmount.DOUBLE)
#
# from proyectos.models import *
# from users.models import *
# p = Proyecto.objects.get(pk=1)
# u = UsuarioGeco.objects.get(pk=2)
# c = Tipo_colaboracion.objects.get(pk=1)
# r = Colaborador_proyecto.objects.create(colaborador=u,proyecto=p,fecha_alta="2020-08-19T19:28:20.407Z",activo=True,tipo_colaborador=c,vigencia=0,fecha_fin_vigencia="2040-08-19T19:28:20.407Z",fecha_ultimo_ingreso="2020-08-19T19:28:20.407Z")
# p.colaboradores.all()
# u.proyectos.all()
# c = Colaborador_proyecto.objects.filter(proyecto=p)
# for k in c:
#      print(k.colaborador,k.tipo_colaborador.tipo,k.tipo_colaborador.descripcion)
#
# for cc in p.colaborador_atributos.all():  <--- cc ess un objeto del tipo Colaborador_proyecto y colaborador_atributo viene de related_name
#     print(cc.colaborador.nombre,cc.tipo_colaborador.tipo,cc.tipo_colaborador.descripcion)
#
# #-------------------------------------------------------------------------------------------------------------------


# esta clase es un -custom "through" model- empleado en la realción UsuarioGeco-Proyecto
#ok gch

class Colaborador_proyecto(models.Model):
    '''
    Establece una relación *muchos-a-muchos* entre un **Proyecto** y un **UsuarioGeco**. 
    Se ha definido una *constraint* para que la combinación ``proyecto+colaborador`` sea único
    '''
    # asociacion para la relación muchos a muchos
    proyecto = models.ForeignKey('Proyecto', related_name='colaborador_atributos', on_delete=models.CASCADE, null=True)
    ''' ``(fk)`` **Proyecto** sobre el cual un **colaborador** puede trabajar. '''
    colaborador = models.ForeignKey('UsuarioGeco', related_name='colaborador_atributos', on_delete=models.CASCADE, null=True, blank=True)
    ''' ``(fk)`` **UsuarioGeco** que puede trabajar con el Corpus. '''

    # atributos dentro de esta asociación y que no se pueden colocar en ninguno de los dos participantes
    fecha_alta = models.DateTimeField(auto_now_add=True, editable=False)
    ''' ``dateTime(now)`` fecha en la que se establece la relación. Es el propietario del proyecto quien puede agregar usuarios y establecer su relacion con el proyecto. '''
    activo = models.BooleanField(default=True, help_text='el colaborador está activo en el proyecto')
    ''' ``boolean(True)`` indica si la relación ``colaborador - proyecto`` está activa , cuando se da de baja la relación 
        (el propietario borra al colaborador) únicamente se pone en ``False``. 
    '''
    tipo_colaborador = models.ForeignKey('Tipo_colaboracion', on_delete=models.CASCADE, null=False)
    ''' ``(fk)`` **Tipo_colaboracion** establece el tipo de colaboración de un usuario. 
    Los colaboradores que puedes ser: propietario, colaborador o lector.
    Un propietario tiene control total sobre el proyecto, mientras que los colaboradores pueden consultar, 
    agregar o borrar documentos. Finalmente los lectores solo pueden consultar los documentos
    '''

    vigencia = models.IntegerField(default=False, help_text='vigencia del colaborador dentro del proyecto')
    ''' ``integer`` Número de meses en que el colaborador estará activo. 
    0 indicará que es por tiempo indefinido, *Un colaborador propietario siempre debe estar activo*.
    '''
    fecha_fin_vigencia = models.DateTimeField(auto_now_add=False, editable=False)
    ''' ``dateTime`` Fecha en la que termina la vigencia aprobada por el propietario (sólo se registra la más reciente)
    Al final de ese periodo de vigencia, por medio de un demonio, el colaborador debería ser inhabilitado ``(activo=False)``.
    El propietario del corpus deberá habilitar nuevamente al colaborador.
    El código siempre debe verificar que el colacorador esté activo en el corpus donde es colaborador.'''
    fecha_ultimo_ingreso = models.DateTimeField(auto_now_add=False, editable=False)
    ''' ``dateTime`` Fecha en que el colaborador ingresó al corpus a realizar alguna actividad.'''
 
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["colaborador", "proyecto"], name='unique_colaborador_proyecto'),
        ]

    def __str__(self) -> str:
        return f'{self.colaborador.nombre} colabora en "{self.proyecto.nombre}"'

