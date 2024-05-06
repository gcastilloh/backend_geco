
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from conf import CONF_USUARIO_ANONIMO
from proyectos.models import Proyecto
from proyectos.models import UsuarioGeco

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def corpus_view(request):
    '''
    Regresa un listado de los proyectos que estan asociados a la autenticacion efectuada
    '''

    proyectos = Proyecto.objects.filter(es_publico=True).order_by('id').values_list('id', 'nombre','es_publico')
    if request.user.username != CONF_USUARIO_ANONIMO:
      usuario = UsuarioGeco.objects.get(usuario=request.user)
      proyectos_priv = Proyecto.objects.filter(es_publico=False, colaboradores=usuario,activo=True).order_by('id').values_list('id', 'nombre', 'es_publico')
      proyectos = proyectos.union(proyectos_priv)
    proyectos = [{'id': id, 'nombre': nombre,'publico': es_publico } for id, nombre, es_publico in proyectos]

    return JsonResponse({'status': 200,
                          'data': {
                                  'usuario' : request.user.username,
                                  'proyectos': proyectos,
                                  },
                          }, safe=False)
