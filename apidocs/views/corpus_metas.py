from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from proyectos.models import UsuarioGeco
from proyectos.models import Proyecto
from proyectos.models import Proyecto_metadato


from decoradores import con_derechos_en_proyecto


# Create your views here.
@api_view(['GET']) 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_meta(request, corpus_id):
    try:
        proyecto= Proyecto.objects.get(id=corpus_id)
        datos = Proyecto_metadato.objects.filter(proyecto=proyecto).order_by('id').values_list('id','metadato__metadato','es_obligatorio')
        data = [{'id':id, 'metadato':metadato,'es_obligatorio':es_obligatorio} for id,metadato,es_obligatorio in datos]
    except Proyecto.DoesNotExist:
        return JsonResponse({'status':404,'data':{"error": f"No se encontró el corpus o no tiene derechos de uso id = {corpus_id}"}}, status=404)
    return JsonResponse({'status':200,'data':data},safe=False, status=200)
