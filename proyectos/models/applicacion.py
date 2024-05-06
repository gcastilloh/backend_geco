from django.db import models


class Aplicacion(models.Model):

    SOLO_COPRUS_PARALELO = 1
    SOLO_CORPUS_NO_PARALELO = 2
    AMBOS_TIPOS_CORPUS = 3
    TIPO_APLICACION = (
        (SOLO_COPRUS_PARALELO, 'corpus paralelos'),
        (SOLO_CORPUS_NO_PARALELO, 'corpus no paralelos'),
        (AMBOS_TIPOS_CORPUS, 'ambos tipos de corpus'),
    )

    tipo_aplicacion = models.IntegerField(
        choices=TIPO_APLICACION, default=SOLO_CORPUS_NO_PARALELO, help_text='¿Esta aplicacion funciona en qué tipo de corpus?')
    nombre = models.CharField(
        max_length=128, verbose_name='nombre', help_text='nombre de la aplicación')
    icono = models.ImageField(
        upload_to='iconos_aplicaciones', null=True, blank=True)
    explicacion = models.TextField(verbose_name='explicación', max_length=1024,
                                   blank=False, help_text='breve explicación de la aplicación')

    def __str__(self) -> str:
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = 'aplicación'
        verbose_name_plural = 'aplicaciones'