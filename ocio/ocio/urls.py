"""ocio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login

urlpatterns = [
	url(r'^(.+)/xml$', 'museos.views.mostrar_xml'), ##
	url(r'^$', 'museos.views.mostrar_principal'),
	url(r'^(\d+)$', 'museos.views.mostrar_principal_next'),
	url(r'^accesibles/(\d+)$', 'museos.views.mostrar_principal_accesibles_next'),
	url(r'^accesibles$', 'museos.views.mostrar_principal_accesibles'),	
	url(r'^museos/(\d+)$', 'museos.views.mostrar_app_museo'),
	url(r'^root/museos/(\d+)$', 'museos.views.mostrar_app_museo'), ###	
	url(r'^museos', 'museos.views.mostrar_museos'),
	url(r'^about', 'museos.views.mostrar_ayuda'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^logout', logout), 
	url(r'^login', login),
	url(r'^(.+)/(\d+)', 'museos.views.mostrar_usuario_next'), ##
	url(r'^(.+)$', 'museos.views.mostrar_usuario') ##
	
]
