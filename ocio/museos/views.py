from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Museo, Usuario
 
# Create your views here.
	
@csrf_exempt
def mostrar_principal(request):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = 'logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = 'login'		

	lista_museos = Museo.objects.order_by('-numero_comentarios')[0:5]
	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')	

	return respuesta

def mostrar_museos(request):
	return HttpResponse('Aqui mostramos todos los museos')

def mostrar_ayuda(request):
	return HttpResponse('Aqui mostramos toda la ayuda posible')	


