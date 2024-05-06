import requests
import re
import time
# function
ports={'freeling':'7000',
         'treetagger':'8000',
         'spacy':'9000'}

# Nombre estandar : Regex
standar_tags_regex={
  'freeling':{
    'SALTO':'^SALTO',
    'ADJETIVO':'^A',
    'CONJUNCION':'^C',
    'DETERMINADOR':'^D',
    'SUSTANTIVO':'^N',
    'PRONOMBRE':'^P',
    'ADVERBIO':'^R',
    'ADPOSICION':'^S',
    'VERBO':'^V',
    'NUMERO':'^Z',
    'DIA':'^W',
    'INTERSECCION':'^I',
    'PUNTUACION':'^F'
  },
  'treetagger':{
    'SALTO':'^SALTO',
    'ADJETIVO':'^ADJ',
    'CONJUNCION':'^CC|^CQ|^CS',
    'DETERMINADOR':'^ART',
    'SUSTANTIVO':'^NC|^NMEA|^NMON|^NP',
    'PRONOMBRE':'^DM|^INT|^PPO|^PPX|^REL',
    'ADVERBIO':'^ADV',
    'ADPOSICION':'^PREP',
    'VERBO':'^V',
    #'NUMERO':'',
    #'DIA':'W*',
    'INTERSECCION':'^ITJN',
    'PUNTUACION':'^BACKSLASH|^CM|^COLON|^DASH|^DOTS|^LP|^PERCT|^QT|^RP|^SEMICOLON|^SLASH'
  },  
  'spacy':{
    'SALTO':'^SALTO',
    'ADJETIVO':'^ADJ',
    'CONJUNCION':'^CONJ|^SCONJ|^CCONJ',
    'DETERMINADOR':'^DET',
    'SUSTANTIVO':'^NOUN|^PROPN',
    'PRONOMBRE':'^PRON',
    'ADVERBIO':'^ADV',
    'ADPOSICION':'^ADP',
    'VERBO':'^VERB|^AUX',
    'NUMERO':'^NUM',
    #'DIA':'W*',
    'INTERSECCION':'^INTJ',
    'PUNTUACION':'^PUNCT|^SYM'
  },

}

def estandarizar_lemmas(content_tags,title,lemmatizador):
  dict_regex=standar_tags_regex[lemmatizador]
  list_lemmas=content_tags[title]['cuerpo']
  
  if len(list_lemmas)>0:
    list_new_lemmas=[]
    
    for lemma in list_lemmas:
      if type(lemma) is dict:
        for key_lemma in lemma:
          new_lemma = {key_lemma:{
                      'tag': lemma[key_lemma]['tag'],
                      'pos': lemma[key_lemma]['tag'],
                      'lemma': lemma[key_lemma]['lemma'] 
                    }}
          
          for std_val, value in dict_regex.items():
            x = re.search(value, lemma[key_lemma]['tag'])
            if(x != None):
              new_lemma[key_lemma]['tag']=std_val
              break
          
          list_new_lemmas.append(new_lemma)
      else:
        list_new_lemmas.append(lemma)
    
    return {title:{'cuerpo':list_new_lemmas}}

  else:
    return content_tags


def get_lemmas(corpus,lemmatizador="freeling"):
  inicio = time.time()
  port=ports[lemmatizador]
  corpus_tag=[]
  for doc in corpus:
    files = {'file':(doc['titulo'], doc['contenido'])}
    # Enviar peticion
    url = "http://localhost:{}/".format(port)

    result = requests.post(url, files=files)
    result_standar=estandarizar_lemmas(result.json(),doc['titulo'],lemmatizador)
    corpus_tag.append(result_standar)
  fin = time.time()
  tiempo = fin-inicio
  return {"result":corpus_tag,"timeEtiquetado":tiempo}

    