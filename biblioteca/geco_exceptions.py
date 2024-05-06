import traceback

class gecoException(Exception):
    def __init__(self, mensaje="Geco: Ha ocurrido una excepcion desconocida en Geco"):
        self.mensaje = mensaje
        traceback.print_exc()
        super().__init__(self.mensaje)

class UsuarioSinDerechosdException(Exception):
    def __init__(self, mensaje="Geco: El usuario no tiene derecho de realizar la operacion"):
        self.mensaje = mensaje
        traceback.print_exc()
        super().__init__(self.mensaje)

class ArchivoDocumentoNotFoundException(Exception):
    def __init__(self, mensaje="Geco: No se proporcionó el archivo del documento o es inválido"):
        self.mensaje = mensaje
        traceback.print_exc()
        super().__init__(self.mensaje)

class DocumentoYaExistenteException(Exception):
    def __init__(self, mensaje="Geco: Ya existe el documento en el corpus"):
        self.mensaje = mensaje
        traceback.print_exc()
        super().__init__(self.mensaje)        

class MetadatoObligatorioNotFoundException(Exception):
    def __init__(self, mensaje="Metadato obligatorio no proporcionado"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class CantidadIncorrectaDeArchivosException(Exception):
    def __init__(self, mensaje="No se proporcionó el archivo del documento o es inválido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class RepositorioInexistenteException(Exception):
    def __init__(self, mensaje="El repositorio no existe en el disco de alamcenamiento"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class BorradoDeDirectorioException(Exception):
    def __init__(self, mensaje="Error al eliminar el directorio"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
