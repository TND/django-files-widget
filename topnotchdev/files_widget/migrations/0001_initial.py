# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topnotchdev.files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extension', models.CharField(max_length=100, null=True, blank=True)),
                ('image', topnotchdev.files_widget.fields.ImageField(max_length=200)),
                ('display_text_overlay', models.BooleanField(default=True)),
                ('overlay_text', models.CharField(help_text=b'Leave blank to display file extension', max_length=7, null=True, blank=True)),
                ('base_color', models.CharField(max_length=12, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IconSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('css_path', models.CharField(help_text=b'Optional css file for icon styling', max_length=200, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('priority', models.IntegerField(default=1)),
                ('default_icon', models.ForeignKey(blank=True, to='files_widget.FileIcon', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fileicon',
            name='icon_set',
            field=models.ForeignKey(to='files_widget.IconSet'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.permission',),
        ),
    ]
