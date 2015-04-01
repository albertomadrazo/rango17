# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_auto_20150219_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='first_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 31, 10, 30, 19, 439995, tzinfo=utc), verbose_name=b'first visit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 31, 10, 30, 19, 439995, tzinfo=utc), verbose_name=b'last visit'),
            preserve_default=True,
        ),
    ]
