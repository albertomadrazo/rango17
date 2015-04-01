# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_auto_20150219_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='username',
            new_name='user',
        ),
    ]
