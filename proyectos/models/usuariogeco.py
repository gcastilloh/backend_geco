from django.db import models
from django.contrib.auth.models import User



# Nota la clase User posee los siguientes atribuos:
# username          -> Nombre de usuario
# password          -> contraseña
# first_name        -> nombre
# last_name         -> apellidos
# email             -> dirección de correo electrónico
# is_active         -> activo
# is_staff          -> es staff
# is_superuser      -> es superusuario
# groups            -> grupos
# user_permissions  -> permisos de usuario
# last_login        -> ultimo ingreso
# date_joined       -> fecha de creación

class UsuarioGeco(models.Model):
    OPCIONES_GRADO = (('', 'Elegir...'), ('LIC','Licenciatura'), ('ESP','Especialización'), ('MBA','Mestría'), ('DOC','Doctorado'), ('POS','Postdoctorado'), ('NONE','OTRO'),)
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=128, unique=False)
    apellidos = models.CharField(max_length=128, unique=False)
    grado_academico = models.CharField(max_length=128, unique=False, choices=OPCIONES_GRADO)
    institucion = models.CharField(max_length=128, unique=False)
    foto_perfil = models.ImageField(default='fotosPerfil/generic.png',null=True, blank=True, upload_to='fotosPerfil/')
    pais = models.ForeignKey('PaisUsuario', on_delete=models.CASCADE, default=13, null=True)

    class Meta:
        ordering = ["usuario"]
        verbose_name = 'Usuario GeCo'
        verbose_name_plural = 'Usuarios GeCo'
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "apellidos"], name='unique_nombre_and_apellido'),
        ]

        # revisr un poco mas UniqueContraint y CheckConstraint para restringir la insercion de datos

    def getNombreCompleto(self):
#        return f'{self.grado_academico} {self.nombre} {self.apellidos}'
        return '{} {} {}'.format(self.grado_academico,self.nombre,self.apellidos)
    def __str__(self):
#        return f'{self.usuario} ({self.getNombreCompleto()})'
        return '{} ({})'.format(self.usuario,self.getNombreCompleto())

    def getProyectos(self):
        res = []
        for ca in self.colaborador_atributos.all():
            res += [{'tipo_id': ca.tipo_colaborador.id,
                     'tipo_colaboracion': ca.tipo_colaborador.tipo, 'proyecto': ca.proyecto}]
        return res

    def num_proyectos(self):
        '''determina el numero de proyectos en los que participa'''
        return len(list(self.colaborador_atributos.all()))

    def email(self):
        '''correo electrónico de el usuario'''
        return self.usuario.email


class PaisUsuario(models.Model):
    pais = models.CharField(max_length= 128, unique = True, help_text = 'País dónde reside el usuario')
    def __str__(self):
        return '%s' % self.pais        