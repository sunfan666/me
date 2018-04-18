# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_profile_cn_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_server', 'Can server info'),)},
        ),
    ]
