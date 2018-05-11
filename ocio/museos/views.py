#!/usr/bin/python3
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Museo, Usuario
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
	

def parser():
	
	doc = etree.parse('museos/201132-0-museos.xml')
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

	lista_museos = Museo.objects.order_by('-NUMERO_COMENTARIOS')[0:5]
	if request.method == "GET":
		respuesta = render(request, 'museos/index.html', {'lista_museos': lista_museos, 'logged': logged, 'link': link, 'name_link': name_link})
	
	elif request.method == "POST":
		if 'Todos' in request.POST:
   			respuesta = HttpResponseRedirect('/museos')
		elif 'About' in request.POST:
			respuesta = HttpResponseRedirect('/about')		
		elif 'Cargar' in request.POST: ######
			parser()	
			respuesta = HttpResponseRedirect('/')

	return respuesta

@csrf_exempt
def mostrar_museos(request):
	if request.method == "GET":
		lista_museos = Museo.objects.all()
		respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos})
	elif request.method == "POST":
		distrito = request.POST['Distrito']
		lista_museos = Museo.objects.filter(DISTRITO=distrito)
		respuesta = render(request, 'museos/museos.html', {'lista_museos': lista_museos})

	return respuesta 

def mostrar_ayuda(request):
	respuesta = HttpResponse('Aqui mostramos la ayuda')
	return respuesta


