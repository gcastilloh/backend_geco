from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.files.uploadedfile import UploadedFile
from conf import CONF_USUARIO_ANONIMO
from biblioteca.geco_exceptions import UsuarioSinDerechosdException

from proyectos.models import UsuarioGeco
from proyectos.models import Proyecto
from proyectos.models import Documento
from proyectos.biblioteca import creaDocumentoTexto
from biblioteca import ArchivoDocumentoNotFoundException, DocumentoYaExistenteException, CantidadIncorrectaDeArchivosException
from decoradores import con_derechos_en_proyecto
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication

from rest_framework import status
import json, base64


# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@con_derechos_en_proyecto
def corpus_docs(request, corpus_id):
    proyecto= Proyecto.objects.get(id=corpus_id)
    if request.method == 'GET':
        documentos = Documento.objects.filter(proyecto = proyecto).order_by('archivo_original').values_list('id','archivo_original')
        data = [{'id':id, 'archivo':archivo} for id, archivo in documentos ]
        response_data = {'status':status.HTTP_200_OK,'data':data}
        return JsonResponse(response_data, safe=False)
    elif request.method == 'POST':
        try:
            if request.user.username == CONF_USUARIO_ANONIMO:
              raise UsuarioSinDerechosdException
            objetoUsuarioGeco = UsuarioGeco.objects.get(usuario=request.user)
            proyecto = Proyecto.objects.get(colaboradores=objetoUsuarioGeco, activo=True, id=corpus_id)
            # determina cuantos archivo se han enviado....
            numero_de_archivos = sum(1 for campo in request.FILES.values() if isinstance(campo, UploadedFile))
            if numero_de_archivos != 1:
                raise CantidadIncorrectaDeArchivosException(f'se proporcionó una cantidad incorrecta de archivos ({numero_de_archivos})')
            metadatos = json.loads(request.POST.get('metadatos'))
            
            documento = request.FILES.get('archivo')
            doc = creaDocumentoTexto(objetoUsuarioGeco, proyecto, documento, True, metadatos)
            data = {'archivo':documento.name, 'metadatos':metadatos}
        except ArchivoDocumentoNotFoundException as e:
            return JsonResponse({'status': status.HTTP_409_CONFLICT,'data':{"error": f"{e}"}}, status=status.HTTP_409_CONFLICT)
        except  DocumentoYaExistenteException as e:
            return JsonResponse({'status': status.HTTP_409_CONFLICT,'data':{"error": f"{e}"}}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST,'data':{"error": f"No se pudo decodificar la información enviada o está incompleta.({e})"}}, status=status.HTTP_400_BAD_REQUEST)
        response_data = {'status': status.HTTP_201_CREATED, 'data': {"message": "Documento creado con éxito", "documento_id": data}}
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)   