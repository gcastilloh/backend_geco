
import random
import string
from unidecode import unidecode
import re

#-- Genera una cdena aletoria de letras y digitos


def randomString(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def nombreDeArchivoValido(s):
    s = unidecode(s)
    s = re.sub(r'[^\w\-_. ]', '-', s)
    s = s.strip()
    s = re.sub(r'\-+', '-', s)
    return s