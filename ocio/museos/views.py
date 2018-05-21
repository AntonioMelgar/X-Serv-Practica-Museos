#!/usr/bin/python3
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Museo, Usuario, Comentario, Pagina_Personal
from lxml import etree
from django.template.loader import get_template
from django.template import Context

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
	
	list_mus = Museo.objects.all()
	if len(list_mus) != 0:
		mostrar_cargar = False
	else:
		mostrar_cargar = True
 
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
	
	paginas_usuarios = Pagina_Personal.objects.all()

	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro, 'paginas_usuarios': paginas_usuarios, 'mostrar_cargar': mostrar_cargar})
	
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
	
	list_mus = Museo.objects.all()
	if len(list_mus) != 0:
		mostrar_cargar = False
	else:
		mostrar_cargar = True	

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
	
	paginas_usuarios = Pagina_Personal.objects.all()

	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro, 'mostrar_cargar': mostrar_cargar, 'paginas_usuarios': paginas_usuarios})
	
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
		
	list_mus = Museo.objects.all()
	if len(list_mus) != 0:
		mostrar_cargar = False
	else:
		mostrar_cargar = True

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

	paginas_usuarios = Pagina_Personal.objects.all()	

	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro, 'mostrar_cargar': mostrar_cargar, 'paginas_usuarios': paginas_usuarios})
	
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

	list_mus = Museo.objects.all()
	if len(list_mus) != 0:
		mostrar_cargar = False
	else:
		mostrar_cargar = True

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
	
	paginas_usuarios = Pagina_Personal.objects.all()	

	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'cero': cero, 'uno': uno, 'dos': dos, 'tres': tres, 'cuatro': cuatro, 'mostrar_cargar': mostrar_cargar, 'paginas_usuarios': paginas_usuarios})
	
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

	mostrar = True	
	if request.method == "GET":
		lista_museos = Museo.objects.all()
		respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar': mostrar})
	elif request.method == "POST":
		if 'Enviar' in request.POST:
			distrito = request.POST['Distrito'].upper()
			lista_museos = Museo.objects.filter(DISTRITO=distrito)
			mostrar = False	
			respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar': mostrar})
		elif 'Inicio' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
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

	if len(comentarios) == 0:
		lista_vacia  = True
 		
	if request.method == "GET":
		respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })
	
	elif request.method == "POST":
		if 'About' in request.POST:
   			respuesta = HttpResponseRedirect('/about')
		elif 'Añadir a lista' in request.POST:
			museos_usuario = Usuario.objects.filter(nombre=request.user.username)
			try:
				nombre_pagina = Pagina_Personal.objects.get(nombre_usuario=request.user.username).nombre_pagina
			except Pagina_Personal.DoesNotExist:
				nombre_pagina = "Página de " + request.user.username
				color_cuerpo = "#FFFFFF"
				color_cabecera = "#9E4528" 
				pagina_personal = Pagina_Personal(nombre_pagina = nombre_pagina, nombre_usuario = request.user.username, color_cuerpo = color_cuerpo, color_cabecera = color_cabecera)	 ##
				pagina_personal.save()
			if len(museos_usuario.filter(museo=museo)) == 0:
				g = Usuario(nombre = request.user.username, comentario = "", museo = museo)	
				g.save()
			respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })

		elif 'Inicio' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'Todos' in request.POST:
			respuesta = HttpResponseRedirect('/museos')
		elif 'Enviar' in request.POST:
			coment = request.POST['Comentario']
			if coment != "":
				g = Comentario(text = request.POST['Comentario'], museo = museo)	
				g.save()
				comentarios = Comentario.objects.filter(museo=museo) 
				museo.NUMERO_COMENTARIOS = museo.NUMERO_COMENTARIOS + 1
				museo.save()
				lista_vacia = False		
			respuesta = render(request, 'museos/museos_app.html', {'museo': museo, 'logged': logged, 'link': link, 'name_link': name_link, 'mostrar_selec': mostrar_selec, 'comentarios': comentarios, 'lista_vacia' : lista_vacia })	
	return respuesta
 
@csrf_exempt
def mostrar_usuario(request, usuario):

	mostrar_selec = False
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
		if request.user.username == usuario:			
			mostrar_selec = True
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
		
	try:
		nombre_pagina = Pagina_Personal.objects.get(nombre_usuario=usuario).nombre_pagina
		color_cuerpo =  Pagina_Personal.objects.get(nombre_usuario=usuario).color_cuerpo ##
		color_cabecera =  Pagina_Personal.objects.get(nombre_usuario=usuario).color_cabecera ##
	except Pagina_Personal.DoesNotExist:
		return HttpResponse('Página no encontrada') 

	museos_usuario = Usuario.objects.filter(nombre=usuario)
	if len(museos_usuario) < 5:
		museos_usuario = museos_usuario[0:len(museos_usuario)]
		
	else:
		museos_usuario = museos_usuario[0:5]

	if request.method == "GET":
		respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera}) ##
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Inicio' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'Modificar' in request.POST:
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			pagina_personal.nombre_pagina = request.POST['Pagina']
			pagina_personal.save()
			nombre_pagina = Pagina_Personal.objects.get(nombre_usuario=usuario).nombre_pagina
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})
		
		elif 'color_cuerpo_boton' in request.POST: ##
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			color_cuerpo = request.POST['color_cuerpo_texto']
			color_cuerpo = color_cuerpo.upper()
			if color_cuerpo == "MORADO":
				color_cuerpo = "#BD8ACF"		
			elif color_cuerpo == "AZUL":
				color_cuerpo = "#706DC9"
			elif color_cuerpo == "VERDE":
				color_cuerpo = "#4CE656"
			elif color_cuerpo == "NARANJA":
				color_cuerpo = "#E38914"
			elif color_cuerpo == "AMARILLO":
				color_cuerpo = "#DBDB3B"
			elif color_cuerpo == "ROJO":
				color_cuerpo = "#ED2828"
			elif color_cuerpo == "ROSA":
				color_cuerpo = "#E089BC"
			elif color_cuerpo == "GRIS":
				color_cuerpo = "#9C9599"
			elif color_cuerpo == "MARRON":
				color_cuerpo = "#D18D6B"
			elif color_cuerpo == "BLANCO":
				color_cuerpo = "#FFFFFF"
			else:
				color_cuerpo = pagina_personal.color_cuerpo 

			pagina_personal.color_cuerpo = color_cuerpo
			pagina_personal.save()
			color_cuerpo = Pagina_Personal.objects.get(nombre_usuario=usuario).color_cuerpo
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})

		elif 'color_cabecera_boton' in request.POST: ## 
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			color_cabecera = request.POST['color_cabecera_texto']
			color_cabecera = color_cabecera.upper()
			if color_cabecera == "MORADO":
				color_cabecera = "#BD8ACF"		
			elif color_cabecera == "AZUL":
				color_cabecera = "#706DC9"
			elif color_cabecera == "VERDE":
				color_cabecera = "#4CE656"
			elif color_cabecera == "NARANJA":
				color_cabecera = "#E38914"
			elif color_cabecera == "AMARILLO":
				color_cabecera = "#DBDB3B"
			elif color_cabecera == "ROJO":
				color_cabecera = "#ED2828"
			elif color_cabecera == "ROSA":
				color_cabecera = "#E089BC"
			elif color_cabecera == "GRIS":
				color_cabecera = "#9C9599"
			elif color_cabecera == "MARRON":
				color_cabecera = "#D18D6B"
			elif color_cabecera == "BLANCO":
				color_cabecera = "#FFFFFF"
			else:
				color_cabecera = pagina_personal.color_cabecera 

			pagina_personal.color_cabecera = color_cabecera
			pagina_personal.save()
			color_cabecera = Pagina_Personal.objects.get(nombre_usuario=usuario).color_cabecera
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})


		elif 'Next' in request.POST: 
			respuesta = HttpResponseRedirect('/' + usuario +'/1')
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta



@csrf_exempt
def mostrar_usuario_next(request, usuario, numero):
	
	mostrar_selec = False
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
		if request.user.username == usuario:			
			mostrar_selec = True
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'
		
	try:
		nombre_pagina = Pagina_Personal.objects.get(nombre_usuario=usuario).nombre_pagina
		color_cuerpo =  Pagina_Personal.objects.get(nombre_usuario=usuario).color_cuerpo ##
		color_cabecera =  Pagina_Personal.objects.get(nombre_usuario=usuario).color_cabecera ##
	except Pagina_Personal.DoesNotExist:
		nombre_pagina = "Página de " + usuario
		color_cuerpo = "#FFFFFF"
		color_cabecera = "#9E4528" 
		pagina_personal = Pagina_Personal(nombre_pagina = nombre_pagina, nombre_usuario = usuario, color_cuerpo = "#FFFFFF", color_cabecera = "#9E4528")	 ##
		pagina_personal.save()

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
		respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera}) 
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')
		elif 'Inicio' in request.POST:
			respuesta = HttpResponseRedirect('/')
		elif 'Modificar' in request.POST:
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			pagina_personal.nombre_pagina = request.POST['Pagina']
			pagina_personal.save()
			nombre_pagina = Pagina_Personal.objects.get(nombre_usuario=usuario).nombre_pagina
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})


		elif 'color_cuerpo_boton' in request.POST: ##
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			color_cuerpo = request.POST['color_cuerpo_texto']
			color_cuerpo = color_cuerpo.upper()
			if color_cuerpo == "MORADO":
				color_cuerpo = "#BD8ACF"		
			elif color_cuerpo == "AZUL":
				color_cuerpo = "#706DC9"
			elif color_cuerpo == "VERDE":
				color_cuerpo = "#4CE656"
			elif color_cuerpo == "NARANJA":
				color_cuerpo = "#E38914"
			elif color_cuerpo == "AMARILLO":
				color_cuerpo = "#DBDB3B"
			elif color_cuerpo == "ROJO":
				color_cuerpo = "#ED2828"
			elif color_cuerpo == "ROSA":
				color_cuerpo = "#E089BC"
			elif color_cuerpo == "GRIS":
				color_cuerpo = "#9C9599"
			elif color_cuerpo == "MARRON":
				color_cuerpo = "#D18D6B"
			elif color_cuerpo == "BLANCO":
				color_cuerpo = "#FFFFFF"
			else:
				color_cuerpo = pagina_personal.color_cuerpo 

			pagina_personal.color_cuerpo = color_cuerpo
			pagina_personal.save()
			color_cuerpo = Pagina_Personal.objects.get(nombre_usuario=usuario).color_cuerpo
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})

		elif 'color_cabecera_boton' in request.POST: ## 
			pagina_personal = Pagina_Personal.objects.get(nombre_usuario=usuario)
			color_cabecera = request.POST['color_cabecera_texto']
			color_cabecera = color_cabecera.upper()
			if color_cabecera == "MORADO":
				color_cabecera = "#BD8ACF"		
			elif color_cabecera == "AZUL":
				color_cabecera = "#706DC9"
			elif color_cabecera == "VERDE":
				color_cabecera = "#4CE656"
			elif color_cabecera == "NARANJA":
				color_cabecera = "#E38914"
			elif color_cabecera == "AMARILLO":
				color_cabecera = "#DBDB3B"
			elif color_cabecera == "ROJO":
				color_cabecera = "#ED2828"
			elif color_cabecera == "ROSA":
				color_cabecera = "#E089BC"
			elif color_cabecera == "GRIS":
				color_cabecera = "#9C9599"
			elif color_cabecera == "MARRON":
				color_cabecera = "#D18D6B"
			elif color_cabecera == "BLANCO":
				color_cabecera = "#FFFFFF"
			else:
				color_cabecera = pagina_personal.color_cabecera 

			pagina_personal.color_cabecera = color_cabecera
			pagina_personal.save()
			color_cabecera = Pagina_Personal.objects.get(nombre_usuario=usuario).color_cabecera
			respuesta = render(request, 'museos/usuario.html', {'lista_museos': museos_usuario, 'logged': logged, 'link': link, 'name_link': name_link, 'nombre_pagina': nombre_pagina, 'mostrar_selec': mostrar_selec, 'color_cuerpo': color_cuerpo, 'color_cabecera': color_cabecera})	

 
		elif 'Next' in request.POST:
			if volver:
				respuesta = HttpResponseRedirect('/' + usuario)
			else: 
				respuesta = HttpResponseRedirect('/' + usuario + '/' + str(int(numero)+1))
		elif 'Cargar' in request.POST: ######
			crear_database()	
			respuesta = HttpResponseRedirect('/')

	return respuesta

@csrf_exempt
def mostrar_ayuda(request):
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.'
		name_link = 'Logout'
		link = '/logout'
	else:
		logged = 'Not logged in.'
		name_link = 'Login'
		link = '/login'

	if request.method == "GET":
		respuesta = render(request, 'museos/about.html', {'logged': logged, 'link': link, 'name_link': name_link})

	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'Inicio' in request.POST:
			respuesta = HttpResponseRedirect('/')
	return respuesta

def mostrar_xml(request, usuario):
	museos_usuario = Usuario.objects.filter(nombre=usuario)
	template = get_template('canal.xml')	
	if request.method == "GET":
		return HttpResponse(template.render(Context({'nombre_usuario':usuario, 'lista_museos':museos_usuario})), content_type="text/xml")
	
	


