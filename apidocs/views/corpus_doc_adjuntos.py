from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from proyectos.models import UsuarioGeco
from proyectos.models import Proyecto
from proyectos.models import Documento
from proyectos.models import Archivo_adjunto

from decoradores import con_derechos_en_proyecto


    #obtiene una lista de los archivos adjuntos al documento cuyo corpus y id se proporciona
    #path('corpus/<int:corpus_id>/<int:document_id>/adjuntos', views.corpus_doc_adjuntos, name='corpus_doc_meta'),


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_doc_adjuntos(request, corpus_id, document_id):
    proyecto= Proyecto.objects.get(id=corpus_id) 
    try:
        documento = Documento.objects.get(id=document_id,proyecto=proyecto)
    except Documento.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": "No se encontró el documento o no tiene derechos de uso"+str(document_id)+"."}}, status=404)
    if request.method == 'GET':
        adjuntos = Archivo_adjunto.objects.filter(documento=documento).values_list('id','archivo_original')
        data = [{'id':id, 'archivo':archivo_original} for id, archivo_original in adjuntos ]
        response_data = {'status':200,'data': data}
        return JsonResponse(response_data, safe=False)    
    # elif request.method == 'POST':
    #     objetoUsuarioGeco = UsuarioGeco.objects.get(usuario = request.user)


    
