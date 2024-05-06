"""
pip install textract
pip install pandas
pip install openpyxl

"""
import textract
import pandas as pd
import os
import codecs


def obtener_extension(nombre_documento):
    """
    Extrae la extension del directorio del documento
    """
    root, extension = os.path.splitext(nombre_documento)
    return extension
    
def obtener_nombre(nombre_documento):
    root, extension = os.path.splitext(nombre_documento)
    return root


def convert_to_txt(nombre_documento):
    """ Funcion para extraer texto de documentos .pdf, .odt, .xls, .xlsx, .doc, .docx
        con el uso del paquete textract y pandas de python 
    """
    text = textract.process(nombre_documento)
    texto = str(text, encoding='utf8')
    return texto
    
    

def xlsx_to_txt(nombre_documento):
    
    """Funcion para extraer texto de archivos xlsx"""
    
    doc = pd.read_excel(nombre_documento, engine='openpyxl' , sheet_name= None)  
    texto=" "
    for sheets in doc:
        texto += doc[sheets].to_string()
    texto = texto.replace("NaN", " ")
    return texto

def write_txt(nombre_documento_txt, texto): 
    """ Función para escribir en un txt """
    # elimina los \n de windows, solo mantiene el \r de linux
    archivo = open(nombre_documento_txt, 'w', encoding='utf8')
    texto = texto.replace("\n", "")
    archivo.write(texto)
    archivo.close()
    return



def read_txt(nombre_documento):
    """ Función para leer txt """
    try:
        # empleo errors='replace' para que aquellos caracteres que no son codificados correctamente
        # sean sustitutiod por � como indicador de un problema en la traduccion esto evita que el sistema 
        # falle cuando se envia un documento no UTF-8
        with codecs.open(nombre_documento, 'r', encoding='utf-8-sig', errors='replace') as archivo:
            texto = archivo.read()
            # print(f"{texto}")
        return texto
    except IOError as e:
        print("File not accessible",e)
        return ""

def transforma_txt(documento):  
    """ Funcion para transformar archivos .docx, .xls, .xlsx, .pdf, .odt a archivos de texto plano .txt
    el nombre ya trae el path.
    regresa:
        1. boolean: indica si ha sido o no modificado el archivo
        2. El nombre del nuevo archivo
            (a) el mismo que el anterior pero con extensión .txt si hubo una transformacion
            (b) Si el archivo tiene extension txt regresa el mismo nombre original (no hace ningun cambio)
            (c) Si el archivo no tiene alguna de las extensiones regresa el mismo nombre original (no hace ningun cambio)
    """
    
    if obtener_extension(documento)==".txt":
        # si el archivo ya es txt simplemente regresa el nombre original del archivo
        # ojo no se hace una verificacion de que es texto, sólo se confia en la extensión....
        return False, documento
    #TODO: Dejo diccionario en caso de que se agreguen tipos de archivo que no se encuentren en el paquete textract 
    extensiones = {".txt":convert_to_txt, 
        ".docx":convert_to_txt, 
        ".doc":convert_to_txt,
        ".odt":convert_to_txt, 
        ".pdf":convert_to_txt, 
        ".xls":convert_to_txt, 
        ".xlsx":xlsx_to_txt}
    extension = obtener_extension(documento)
    if extension in extensiones:
        funcion = extensiones.get(extension)
        texto=funcion(documento)
        nuevo_documento = documento.replace(extension, ".txt")
        write_txt(nuevo_documento,texto)
        return True, nuevo_documento
    # si el documento no es del tipo correcto regresa un el documento original (??)
    return False,documento

