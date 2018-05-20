#!/usr/bin/python3
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Museo, Usuario, Comentario
from lxml import etree

# Create your views here.

def extraer_elemento(dic, elemento):
	try:
		elemento = dic[elemento]
	
	except KeyError:
		elemento = ""

	return elemento

def guardar_datos(dic):
	dicc_datos = {}
	lista_aux = ['ID_ENTIDAD', 'NOMBRE', 'DESCRIPCION_ENTIDAD', 'HORARIO', 'TRANSPORTE', 'ACCESIBILIDAD', 'CONTENT_URL', 'NOMBRE_VIA', 'CLASE_VIAL', 'TIPO_NUM', 'NUM', 'LOCALIDAD', 'CODIGO_POSTAL','PLANTA', 'BARRIO', 'DISTRITO', 'COORDENADA_X', 'COORDENADA_Y', 'LATITUD', 'LONGITUD', 'TELEFONO', 'FAX', 'EMAIL', 'EQUIPAMIENTO']
	
	for elemento in lista_aux:
		dicc_datos[elemento] = extraer_elemento(dic, elemento)

	g = Museo(ID_ENTIDAD = dicc_datos['ID_ENTIDAD'], NOMBRE = dicc_datos['NOMBRE'], DESCRIPCION_ENTIDAD = dicc_datos['DESCRIPCION_ENTIDAD'], HORARIO = dicc_datos['HORARIO'], TRANSPORTE = dicc_datos['TRANSPORTE'], ACCESIBILIDAD = dicc_datos['ACCESIBILIDAD'], CONTENT_URL = dicc_datos['CONTENT_URL'], NOMBRE_VIA = dicc_datos['NOMBRE_VIA'], CLASE_VIAL = dicc_datos['CLASE_VIAL'], TIPO_NUM = dicc_datos['TIPO_NUM'], NUM = dicc_datos['NUM'], LOCALIDAD = dicc_datos['LOCALIDAD'], CODIGO_POSTAL = dicc_datos['CODIGO_POSTAL'], PLANTA = dicc_datos['PLANTA'], BARRIO = dicc_datos['BARRIO'], DISTRITO = dicc_datos['DISTRITO'], COORDENADA_X = dicc_datos['COORDENADA_X'], COORDENADA_Y = dicc_datos['COORDENADA_Y'], LATITUD = dicc_datos['LATITUD'], LONGITUD = dicc_datos['LONGITUD'], TELEFONO = dicc_datos['TELEFONO'], FAX = dicc_datos['FAX'], EMAIL = dicc_datos['EMAIL'], EQUIPAMIENTO = dicc_datos['EQUIPAMIENTO'], NUMERO_COMENTARIOS = 0)
	
	g.save()
		
	return None

def parsear(doc):

	contenidos = doc.getroot()
	
	for k in range(1, len(contenidos)):
		contenido = contenidos[k]
		atributo = contenido[1]			
		dic = {}
		
		for i in range(0, len(atributo)-1):
			nombre = atributo[i].attrib.get("nombre") 
			if nombre == "LOCALIZACION":
				for j in range(0, len(atributo[i])):				
					nombre = atributo[i][j].attrib.get("nombre")
					val = nombre.find("-")
					if val != -1:
						nombre = nombre.replace("-", "_")

					dic[nombre] = atributo[i][j].text
	 		
			elif nombre == "DATOSCONTACTOS":
				for j in range(0, len(atributo[i])):
					nombre = atributo[i][j].attrib.get("nombre")
					val = nombre.find("-")
					if val != -1:
						nombre = nombre.replace("-", "_")

					dic[nombre] = atributo[i][j].text
			else:
				val = nombre.find("-")
				if val != -1:
					nombre = nombre.replace("-", "_")

				dic[nombre] = atributo[i].text

		guardar_datos(dic) 
		
	return None

def crear_database():	
	doc = etree.parse('museos/201132-0-museos.xml')
	parsear(doc)

	return None
		
	
@csrf_exempt
def mostrar_principal(request):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'	
	
	lista_museos = Museo.objects.exclude(NUMERO_COMENTARIOS__in="0").order_by('-NUMERO_COMENTARIOS')
	if len(lista_museos) < 5:
		lista_museos = lista_museos[0:len(lista_museos)]
		
	else:
		lista_museos = lista_museos[0:5]

	cuatro = False
	tres = False
	dos = False
	uno = False
	cero = False
	#Un tricky para cuadrar dimensiones de la interfaz
	if len(lista_museos) == 0:
		cero = True
	elif len(lista_museos) == 1:
		uno = True
	elif len(lista_museos) == 2:
		dos = True
	elif len(lista_museos) == 3:
		tres = True
	elif len(lista_museos) == 4:
		cuatro = True

	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Accesibles' in request.POST:
			respuesta = HttpResponseRedirect('/accesibles')
		elif 'Next' in request.POST: 
			respuesta = HttpResponseRedirect('/1')
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta


@csrf_exempt
def mostrar_principal_next(request, numero):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'	
	
	lista_museos = Museo.objects.exclude(NUMERO_COMENTARIOS__in="0").order_by('-NUMERO_COMENTARIOS')
	volver = False
	if len(lista_museos) <= 5:
		lista_museos = lista_museos[0:len(lista_museos)]	
	elif len(lista_museos) - int(numero)*5 < 5:
		lista_museos = lista_museos[int(numero)*5:len(lista_museos)]
		volver = True
	else:
		lista_museos = lista_museos[int(numero)*5:(int(numero)*5+5)]
	
	cuatro = False
	tres = False
	dos = False
	uno = False
	cero = False
	#Un tricky para cuadrar dimensiones de la interfaz
	if len(lista_museos) == 0:
		cero = True
	elif len(lista_museos) == 1:
		uno = True
	elif len(lista_museos) == 2:
		dos = True
	elif len(lista_museos) == 3:
		tres = True
	elif len(lista_museos) == 4:
		cuatro = True
	
	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Accesibles' in request.POST:
			respuesta = HttpResponseRedirect('/accesibles')
		elif 'Next' in request.POST:
			if volver:
				respuesta = HttpResponseRedirect('/')
			else: 
				respuesta = HttpResponseRedirect('/' + str(int(numero)+1))
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta

@csrf_exempt
def mostrar_principal_accesibles(request):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'		

	lista_museos = Museo.objects.exclude(NUMERO_COMENTARIOS__in="0").filter(ACCESIBILIDAD = '1').order_by('-NUMERO_COMENTARIOS')
	if len(lista_museos) < 5:
		lista_museos = lista_museos[0:len(lista_museos)]
		
	else:
		lista_museos = lista_museos[0:5] 
	
	cuatro = False
	tres = False
	dos = False
	uno = False
	cero = False
	#Un tricky para cuadrar dimensiones de la interfaz
	if len(lista_museos) == 0:
		cero = True
	elif len(lista_museos) == 1:
		uno = True
	elif len(lista_museos) == 2:
		dos = True
	elif len(lista_museos) == 3:
		tres = True
	elif len(lista_museos) == 4:
		cuatro = True
	
	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Accesibles' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'Next' in request.POST: 
			respuesta = HttpResponseRedirect('/accesibles/1')
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta


@csrf_exempt
def mostrar_principal_accesibles_next(request, numero):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'		

	lista_museos = Museo.objects.exclude(NUMERO_COMENTARIOS__in="0").filter(ACCESIBILIDAD = '1').order_by('-NUMERO_COMENTARIOS')
	volver = False
	if len(lista_museos) <= 5:
		lista_museos = lista_museos[0:len(lista_museos)]	
	elif len(lista_museos) - int(numero)*5 < 5:
		lista_museos = lista_museos[int(numero)*5:len(lista_museos)]
		volver = True
	else:
		lista_museos = lista_museos[int(numero)*5:(int(numero)*5+5)]

	cuatro = False
	tres = False
	dos = False
	uno = False
	cero = False
	#Un tricky para cuadrar dimensiones de la interfaz
	if len(lista_museos) == 0:
		cero = True
	elif len(lista_museos) == 1:
		uno = True
	elif len(lista_museos) == 2:
		dos = True
	elif len(lista_museos) == 3:
		tres = True
	elif len(lista_museos) == 4:
		cuatro = True
	
	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Accesibles' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'Next' in request.POST:
			if volver:
				respuesta = HttpResponseRedirect('/accesibles')
			else: 
				respuesta = HttpResponseRedirect('/accesibles/' + str(int(numero)+1))
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')
	
	return respuesta

@csrf_exempt
def mostrar_museos(request):

	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
	
	if request.method == "GET":
		lista_museos = Museo.objects.all()
		respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link})
	elif request.method == "POST":
		distrito = request.POST['Distrito'].upper()
		lista_museos = Museo.objects.filter(DISTRITO=distrito)
		respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link})

	return respuesta


@csrf_exempt
def mostrar_app_museo(request, identificador):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
		mostrar_selec = True
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
		mostrar_selec = False
		
	museo = Museo.objects.get(id=int(identificador))
	comentarios = Comentario.objects.filter(museo=museo)
	lista_vacia = False
	print(len(comentarios))	
	if len(comentarios) == 0:
		lista_vacia  = True
 		
	if request.method == "GET":
		respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })
	
	elif request.method == "POST":
		if 'About' in request.POST:
   			respuesta = HttpResponse('agregar ayuda')
		elif 'Añadir a lista' in request.POST:
			museos_usuario = Usuario.objects.filter(nombre=request.user.username)
			if len(museos_usuario.filter(museo=museo)) == 0:
				g = Usuario(nombre = request.user.username, comentario = "", museo = museo)	
				g.save()
			respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })

		elif 'Enviar' in request.POST:
			coment = request.POST['Comentario']
			if coment != "":
				g = Comentario(text = request.POST['Comentario'], museo = museo)	
				g.save()
				comentarios = Comentario.objects.filter(museo=museo) 
				museo.NUMERO_COMENTARIOS = museo.NUMERO_COMENTARIOS + 1
				museo.save()		
			respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })	
	return respuesta
 
@csrf_exempt
def mostrar_usuario(request, usuario):
	
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
		mostrar_selec = True
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
		mostrar_selec = False
	
	museos_usuario = Usuario.objects.filter(nombre=usuario)
	if len(museos_usuario) < 5:
		museos_usuario = museos_usuario[0:len(museos_usuario)]
		
	else:
		museos_usuario = museos_usuario[0:5]

	if request.method == "GET":
		respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link}) 
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Next' in request.POST: 
			respuesta = HttpResponseRedirect('/' + usuario +'/1')
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta



@csrf_exempt
def mostrar_usuario_next(request, usuario, numero):
	
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
		mostrar_selec = True
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
		mostrar_selec = False
	
	museos_usuario = Usuario.objects.filter(nombre=usuario)
	volver = False
	if len(museos_usuario) <= 5:
		museos_usuario = museos_usuario[0:len(museos_usuario)]
		volver = True	
	elif len(museos_usuario) - int(numero)*5 < 5:
		museos_usuario = museos_usuario[int(numero)*5:len(museos_usuario)]
		volver = True
	else:
		museos_usuario = museos_usuario[int(numero)*5:(int(numero)*5+5)]

	if request.method == "GET":
		respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link}) 
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Next' in request.POST:
			if volver:
				respuesta = HttpResponseRedirect('/' + usuario)
			else: 
				respuesta = HttpResponseRedirect('/' + usuario + '/' + str(int(numero)+1))
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta

def mostrar_ayuda(request):
	respuesta = HttpResponse('Aqui mostramos la ayuda')
	return respuesta


