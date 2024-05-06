
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from conf import CONF_USUARIO_ANONIMO
from proyectos.models import UsuarioGeco
from proyectos.models import Proyecto

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def corpus_colabora_view(request):
    '''
    Regresa un listado de los proyectos en que el usuario colabora
    '''    
    if request.user.username == CONF_USUARIO_ANONIMO:
      return JsonResponse({'status':200,'proyectos': []}, safe=False)      
    
    usuario = UsuarioGeco.objects.get(usuario=request.user)
    proyectos = Proyecto.objects.filter(colaboradores = usuario, activo = True).order_by('id').values_list('id','nombre','es_publico')  
    proyectos_json = [{'id':id,'nombre':nombre,'publico':es_publico} for id,nombre,es_publico in proyectos]
    data = { 'proyectos': proyectos_json}
    return JsonResponse({'status':200,'data':data}, safe=False)  