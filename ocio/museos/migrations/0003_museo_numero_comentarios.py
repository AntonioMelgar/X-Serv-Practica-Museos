# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_museo_enlace'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='numero_comentarios',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
