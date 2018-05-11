# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('BARRIO', models.CharField(max_length=20000)),
                ('DISTRITO', models.CharField(max_length=20000)),
                ('COORDENADA_X', models.CharField(max_length=20000)),
                ('COORDENADA_Y', models.CharField(max_length=20000)),
                ('LATITUD', models.CharField(max_length=20000)),
                ('LONGITUD', models.CharField(max_length=20000)),
                ('TELEFONO', models.CharField(max_length=20000)),
                ('FAX', models.CharField(max_length=20000)),
                ('EMAIL', models.CharField(max_length=20000)),
                ('NUMERO_COMENTARIOS', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=256)),
                ('comentario', models.CharField(max_length=20000)),
                ('fecha', models.DateTimeField()),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
    ]
