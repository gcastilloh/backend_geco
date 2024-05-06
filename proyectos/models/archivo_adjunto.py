from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage

class Archivo_adjunto(models.Model):
    '''
    Son documentos adjuntos al documento principal.
    '''
    documento = models.ForeignKey('Documento', related_name='archivo_adjunto_documento', on_delete=models.CASCADE, null=False)
    archivo_original = models.CharField(max_length= 128, unique = False, help_text = 'nombre del archivo')
    archivo = models.CharField(max_length= 128, unique = True, help_text = 'nombre del archivo en el repositorio')
    derechos = models.BooleanField(default=True,help_text='¿El documento tiene derechos de autor?')
    tipo = models.ForeignKey('Proyecto_adjunto', related_name='archivo_adjunto_tipo', on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ['archivo_original']
        verbose_name = 'Archivo adjunto'
        verbose_name_plural = 'Archivos adjuntos'

    # eliminamos espacios al inicio y al final antes de instertar el dato
    def save(self, *args, **kwargs):
        self.archivo_original = self.archivo_original.strip()
        self.archivo = self.archivo.strip()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        dir_repositorio_proyecto = self.documento.proyecto.getPathRepositorio()
        FS = FileSystemStorage(location=dir_repositorio_proyecto,file_permissions_mode=0o664)
        if FS.exists(self.archivo):
            FS.delete(self.archivo)
        super().delete(*args, **kwargs)
        #print(f'archivo adjunto {self.archivo_original} ({self.archivo}) borrado')


    def __str__(self):
        return f"{self.archivo} {self.archivo_original}"

    #regresa el nombre del archivo con todo y ruta física desde /
    def getArchivoConPath(self):
        return f"{self.documento.proyecto.getPathRepositorio()}{self.archivo}"

    #regresa el nombre del archivo con todo y URL tomando como base la MEDIA_URL
    def getArchivoConMediaURL(self):
        return f"{settings.MEDIA_URL}{self.documento.proyecto.repositorio}/{self.archivo}"

    #regresa el nombre del archivo con todo y ruta física desde /
    def getArchivoConPath(self):
        return f"{self.documento.proyecto.getPathRepositorio()}{self.archivo}"

    #regresa el nombre del archivo con todo y URL tomando como base la MEDIA_URL
    def getArchivoConMediaURL(self):
        return f"{settings.MEDIA_URL}{self.documento.proyecto.repositorio}/{self.archivo}"


