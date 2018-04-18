# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20180326_1419'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'permissions': (('view_server', 'Can server info'),)},
        ),
    ]
