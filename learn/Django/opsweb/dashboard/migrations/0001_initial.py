# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=11)),
                ('title', models.CharField(max_length=32)),
                ('department', models.CharField(max_length=32)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=32)),
                ('ip', models.CharField(unique=True, max_length=15)),
                ('cpu', models.CharField(max_length=50)),
                ('mem', models.CharField(max_length=50)),
                ('disk', models.CharField(max_length=50)),
                ('sn', models.CharField(max_length=50)),
                ('idc', models.CharField(max_length=50)),
                ('ipinfo', models.CharField(max_length=255, verbose_name=b"[{'eth0':1.1.1.1,'mac':''},{'eth0':2.2.2.2,'mac':''}]")),
                ('product', models.CharField(max_length=50)),
                ('remark', models.TextField(default=b'')),
            ],
            options={
                'db_table': 'server',
            },
        ),
    ]
