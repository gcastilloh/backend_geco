from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
  path('get-token/', CustomAuthToken.as_view()),
    # Rutas API

    #obtiene la lista de corpus públicos
    path('corpus/', corpus_view, name='corpus_publicos'),

    #obtiene los nombres de los corpus en que colabora el usuario cuyo token se ha proporcionado
    path('corpus/colabora', corpus_colabora_view, name='corpus_colabora'),

    # obtiene los nombres de los metadatos asociados al corpus cuyo id se ha proporcionado
    path('corpus/<int:corpus_id>/meta', corpus_meta, name='corpus_meta'),
    
    # get: obtiene todos los documentos del corpus cuyo id se ha proporcionado
    # post: envia los dato de un documento para que se agregue al corpus
    path('corpus/<int:corpus_id>', corpus_docs, name='corpus_docs'),

    #obtiene los datos del documento cuyo corpus y id se ha proporcionado
    path('corpus/<int:corpus_id>/<int:document_id>', corpus_recupera_doc, name='corpus_doc'),

    #obtiene los valores de los metadatos del documento cuyo corpus y id se ha proporcionado
    path('corpus/<int:corpus_id>/<int:document_id>/meta', corpus_doc_meta, name='corpus_doc_meta'),

    #obtiene el etiquetado Part Of Speech (POS) del documento cuyo corpus y id se ha proporcionado
    path('corpus/<int:corpus_id>/<int:document_id>/pos', corpus_doc_pos, name='corpus_doc_pos'),

    # get: obtiene una lista de los archivos adjuntos al documento cuyo corpus y id se proporciona
    # post: almacena el documento adjunto que se envia asociandolo al document_id proporcionado
    path('corpus/<int:corpus_id>/<int:document_id>/adjuntos', corpus_doc_adjuntos, name='corpus_doc_meta'),

    #obtiene una lista de los archivos adjuntos al documento cuyo corpus y id se proporciona
    path('corpus/<int:corpus_id>/<int:document_id>/adjunto/<int:adjunto_id>', corpus_recupera_adjunto, name='corpus_doc_meta'),

]
