from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from proyectos.models import UsuarioGeco
from biblioteca import  read_txt
from proyectos.models import Proyecto
from proyectos.models import Documento
from proyectos.models import Documento_metadato

from decoradores import con_derechos_en_proyecto

# Create your views here.
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_doc_pos(request, corpus_id, document_id):
   try:
      proyecto= Proyecto.objects.get(activo = True, id=corpus_id)    
   except Proyecto.DoesNotExist:
      return JsonResponse({'status':404,"error": f"No se encontró el corpus o no tiene derechos de uso id = {corpus_id}"}, status=404)

   try:
      documento = Documento.objects.get(proyecto = proyecto,id=document_id)
   except Documento.DoesNotExist:
      return JsonResponse({'status':404,"error": f"No se encontró el documento solicitado id={document_id}"}, status=404)

   data = {'status':200,'data': read_txt(documento.getArchivoEtiquetadoConPath())}
   return JsonResponse(data, safe=False)
