import random
import string
import shutil
import os

from chardet.universaldetector import UniversalDetector

UTF8_FILE_CONVERT_OK = 1
UTF8_FILE_CONVERT_ERROR = -1
UTF8_FILE_CONVERT_UNKNOW_ENCODE = -2


def detectar_utf8(filename):
    '''
    Determina si el achivo cuyo nombre se envia está codificado en UTF-8
    regresa:
        True o False : es o no UTF-8
    '''
    detector = UniversalDetector()
    detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return (detector.result['encoding'] == 'utf-8')

def detecta_utf8_detalles(filename):
    '''
    Determina si el achivo cuyo nombre se envia está codificado en UTF-8
    regresa:
        True o False : es o no UTF-8
        diccionario : con la codificción y confianza de la deteccion
    '''
    detector = UniversalDetector()
    detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return {'encoding': detector.result['encoding'], 'confidence':  detector.result['confidence']}

def convertidor(fileName):
    if detectar_utf8(fileName):
        return 2
    analisis = detecta_utf8_detalles(fileName)
    if analisis['confidence'] >= 0.50:
        try:
            lettersAndDigits = string.ascii_letters + string.digits
            outFile = ''.join(random.choice(lettersAndDigits) for _ in range(20))        

            f = open(fileName, 'rb')
            step = 1
            content = str(f.read(), analisis['encoding'])  
            step = 2
            f.close()

            out = open(outFile, 'wb')
            step = 3
            out.write(content.encode('utf-8'))
            step = 4
            out.close()
            setp = 5
            tmp = ''.join(random.choice(lettersAndDigits) for _ in range(5)) 
            filetmp = f"{fileName}.{tmp}"
            os.rename(fileName,filetmp)
            os.rename(outFile,fileName)
            os.remove(filetmp)
            return UTF8_FILE_CONVERT_OK
        except Exception as e:
            print(f"convertidor(): exception in step {step}")
            print(f"Error: {e} ")
            return UTF8_FILE_CONVERT_ERROR
        finally:
            if os.path.exists(outFile):
                os.remove(outFile)
    return UTF8_FILE_CONVERT_UNKNOW_ENCODE

def convertir_en_bloque(archivos):
    for f in archivos:
        r = convertidor(f)
        if r<0:
            detalles = detecta_utf8_detalles(f)
            print(f'{f} >>>> fail {r} {detalles}')
        elif r==1:
            print(f'{f}  >>> ok')
        else:
            print(f'{f} >>> none')
    return
        
def convertir_directorio(dir):
    archivos =os.listdir(dir)
    for f in archivos:
        a = f"{dir}/{f}"
        if os.path.isfile(a):
            r = convertidor(a)
            if r==UTF8_FILE_CONVERT_ERROR:
                detalles = detecta_utf8_detalles(a)
                print(f'{f} >>>> fail {r} {detalles}')
            elif r==UTF8_FILE_CONVERT_OK:
                detalles = detecta_utf8_detalles(a)
                print(f'{f} >>>> ok {r} {detalles}')
            elif r == UTF8_FILE_CONVERT_UNKNOW_ENCODE:
                detalles = detecta_utf8_detalles(a)
                print(f'{f} >>>> unknow encoding {r} {detalles}')
        else:
                print(f"{f} >>> isn't file")
    return

