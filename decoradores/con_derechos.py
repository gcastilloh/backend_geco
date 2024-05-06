from functools import wraps
from django.http import JsonResponse

from conf import CONF_USUARIO_ANONIMO
from proyectos.models import UsuarioGeco, Proyecto

'''
verifica si un usuario tiene derechos sobre el corpus ya sea anonimo (solo corpus publicos)
o un usuario normal (puede usar corpus publicos o aquellos donde colabora)
'''
def con_derechos_en_proyecto(view_func):
    @wraps(view_func)
    def _wrapped_view(request, corpus_id, *args, **kwargs):
        try:
            proyecto = Proyecto.objects.get(activo=True, id=corpus_id)
            if proyecto.es_publico:
                return view_func(request, corpus_id, *args, **kwargs)
            if request.user.username == CONF_USUARIO_ANONIMO:
              print('usuario anonimo tratando de acceder a un proyecto no publico')
              raise Proyecto.DoesNotExist
            objetoUsuarioGeco = UsuarioGeco.objects.get(usuario=request.user)
            proyecto = Proyecto.objects.get(colaboradores=objetoUsuarioGeco, activo=True, id=corpus_id)
        except Proyecto.DoesNotExist:
            return JsonResponse({'status':404,"error": "No se encontró el corpus o no tiene derechos de uso para el corpus con ID " + str(corpus_id) + "."}, status=404)
        return view_func(request, corpus_id, *args, **kwargs)

    return _wrapped_view