## pip install djangorestframework
# Modelos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from proyectos.models import UsuarioGeco
from proyectos.models import Proyecto
from proyectos.models import Documento
from proyectos.models import Documento_metadato


from decoradores import con_derechos_en_proyecto


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_doc_meta(request, corpus_id, document_id):
    try:
        proyecto= Proyecto.objects.get(activo = True, id=corpus_id)    
        documento = Documento.objects.get(proyecto = proyecto,id=document_id)
        dm = Documento_metadato.objects.filter(documento=documento).order_by('proyecto_metadato__id').values_list('proyecto_metadato__id','valor')
    except Proyecto.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": f"1No se encontró el corpus o no tiene derechos de uso id = {corpus_id}"}}, status=404)
    except Documento.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": f"2No se encontró el documento solicitado id={document_id}"}}, status=404)
    data = [{'id':id,'valor':valor} for id,valor in dm]
    return JsonResponse({'status':200,'data':data},safe=False,status=200)
  

def make_token(request):
    u = []
    for user in User.objects.all():
        t, created = Token.objects.get_or_create(user=user)
        if not created:
            t.delete()
            Token.objects.create(user=user)  
            u.append(user)
    return JsonResponse({'message': f'TOKENS DONE [{u}]'}, safe=False)
     