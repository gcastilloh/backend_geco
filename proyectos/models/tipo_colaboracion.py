from django.db import models



class Tipo_colaboracion(models.Model):
    tipo = models.CharField(
        max_length=128, 
        verbose_name='tipo de colaboración',
        unique=True, 
        help_text='tipo de colaboración'
    )

    descripcion = models.CharField(
        max_length=128, 
        verbose_name='descripción',
        help_text='descripción de las actividades de este tipo de colaborador'
    )

    duracionMeses = models.IntegerField(
        verbose_name='tiempo de vigencia en meses',
        null=True,
        help_text='Establece el tiempo en que un colaborador estará activo en número de meses'
    )

    class Meta:
        verbose_name = 'tipo de colaboración del documento'
        verbose_name_plural = 'tipos de colaboración'

    # eliminamos espacios al inicio y al final antes de instertar el dato
    def save(self, *args, **kwargs):
        self.tipo = self.tipo.strip()
        self.descripcion = self.descripcion.strip()
        super().save(*args, **kwargs) 

    def __str__(self) -> str:
        return f'[{self.tipo} -> {self.descripcion} ({self.duracionMeses}) meses'
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------