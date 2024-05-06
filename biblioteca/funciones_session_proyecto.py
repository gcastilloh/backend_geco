from django.shortcuts import redirect
from django.views import generic


def setSessionProyectoActual(request,context,pk=0):
    context['proyecto_actual'] = pk
    request.session['proyecto_actual'] = pk

def getSessionProyectoActual(request):
    return request.session.get('proyecto_actual',0)