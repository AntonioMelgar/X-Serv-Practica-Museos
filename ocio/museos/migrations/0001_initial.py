# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ID_ENTIDAD', models.CharField(max_length=256)),
                ('NOMBRE', models.CharField(max_length=256)),
                ('DESCRIPCION_ENTIDAD', models.CharField(max_length=20000)),
                ('HORARIO', models.CharField(max_length=20000)),
                ('TRANSPORTE', models.CharField(max_length=20000)),
                ('ACCESIBILIDAD', models.CharField(max_length=256)),
                ('CONTENT_URL', models.CharField(max_length=20000)),
                ('NOMBRE_VIA', models.CharField(max_length=20000)),
                ('CLASE_VIAL', models.CharField(max_length=20000)),
                ('TIPO_NUM', models.CharField(max_length=20000)),
                ('NUM', models.CharField(max_length=20000)),
                ('LOCALIDAD', models.CharField(max_length=20000)),
                ('CODIGO_POSTAL', models.CharField(max_length=20000)),
                ('PLANTA', models.CharField(max_length=20000)),
                ('BARRIO', models.CharField(max_length=20000)),
                ('DISTRITO', models.CharField(max_length=20000)),
                ('COORDENADA_X', models.CharField(max_length=20000)),
                ('COORDENADA_Y', models.CharField(max_length=20000)),
                ('LATITUD', models.CharField(max_length=20000)),
                ('LONGITUD', models.CharField(max_length=20000)),
                ('TELEFONO', models.CharField(max_length=20000)),
                ('FAX', models.CharField(max_length=20000)),
                ('EMAIL', models.CharField(max_length=20000)),
                ('EQUIPAMIENTO', models.CharField(max_length=20000)),
                ('NUMERO_COMENTARIOS', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pagina_Personal',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nombre_pagina', models.CharField(max_length=256)),
                ('nombre_usuario', models.CharField(max_length=256)),
                ('color_cuerpo', models.CharField(max_length=256)),
                ('color_cabecera', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=256)),
                ('comentario', models.CharField(max_length=20000)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
