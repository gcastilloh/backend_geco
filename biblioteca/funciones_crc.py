import hashlib

def get_checksum(name):
    '''
    recibe el nombre de un archivo y genera el check sum de ese archivo
    basado en Blake2 y no en MD5
    BLAKE2: simpler, smaller, fast as MD5 (https://eprint.iacr.org/2013/322.pdf)
    Why Replace SHA-1 with BLAKE2? https://research.kudelskisecurity.com/2017/03/06/why-replace-sha-1-with-blake2/
    '''
    try:
        with open(name, "rb") as f:
            file_hash = hashlib.blake2b()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except:
        return None
