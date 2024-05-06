## pip install djangorestframework
# Modelos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from proyectos.models import UsuarioGeco
from biblioteca import  read_txt
from proyectos.models import Proyecto
from proyectos.models import Documento
from proyectos.models import Archivo_adjunto
from decoradores import con_derechos_en_proyecto

    # obtiene una lista de los archivos adjuntos al documento cuyo corpus y id se proporciona
    # path('corpus/<int:corpus_id>/<int:document_id>/adjunto/<int:adjunto_id>', views.corpus_recupera_adjunto, name='corpus_doc_meta'),


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_recupera_adjunto(request, corpus_id, document_id, adjunto_id):
    
    proyecto= Proyecto.objects.get(id=corpus_id)    
    try:
        documento = Documento.objects.get(proyecto = proyecto,id=document_id)
        documento = Archivo_adjunto.objects.get(id=adjunto_id,documento=documento)
    except Documento.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": f"No se encontró el documento solicitado id={document_id}."}}, status=404)
    except  Archivo_adjunto.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": f"No se encontró el archivo solicitado id={adjunto_id}."}}, status=404)

    data = {'status':404,'data': read_txt(documento.getArchivoConPath())}

    return JsonResponse(data, safe=False)