# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20180318_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(default=1, to='dashboard.Department'),
        ),
    ]
