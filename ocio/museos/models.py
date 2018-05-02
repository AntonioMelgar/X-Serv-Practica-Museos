from django.db import models

# Create your models here.
class Museo(models.Model):
	p_k = models.IntegerField()	
	nombre = models.CharField(max_length=256)
	horario = models.CharField(max_length=20000)
	descripcion = models.CharField(max_length=20000)
	direccion = models.CharField(max_length=20000)
	distrito = models.CharField(max_length=256)
	accesibilidad = models.IntegerField()
	enlace = models.CharField(max_length=20000)
	numero_comentarios = models.IntegerField()
	def __str__(self):
		return self.nombre	

class Usuario(models.Model):
	nombre = models.CharField(max_length=256)
	comentario = models.CharField(max_length=20000)
	fecha = models.DateTimeField() 
	museo = models.ForeignKey(Museo)
	def __str__(self):
		return self.museo.nombre + ', ' + self.comentario	


