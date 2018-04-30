# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='enlace',
            field=models.CharField(default=1, max_length=20000),
            preserve_default=False,
        ),
    ]
