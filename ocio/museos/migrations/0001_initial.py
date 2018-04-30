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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('p_k', models.IntegerField()),
                ('nombre', models.CharField(max_length=256)),
                ('horario', models.CharField(max_length=20000)),
                ('descripcion', models.CharField(max_length=20000)),
                ('direccion', models.CharField(max_length=20000)),
                ('accesibilidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=256)),
                ('comentario', models.CharField(max_length=20000)),
                ('fecha', models.DateTimeField()),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
    ]
