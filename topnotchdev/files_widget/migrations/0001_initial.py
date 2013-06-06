# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IconSet'
        db.create_table(u'files_widget_iconset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('css_path', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('default_icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['files_widget.FileIcon'], null=True, blank=True)),
        ))
        db.send_create_signal(u'files_widget', ['IconSet'])

        # Adding model 'FileIcon'
        db.create_table(u'files_widget_fileicon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['files_widget.IconSet'])),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('topnotchdev.files_widget.fields.ImageField')(max_length=200)),
            ('display_text_overlay', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('overlay_text', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('base_color', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'files_widget', ['FileIcon'])


    def backwards(self, orm):
        # Deleting model 'IconSet'
        db.delete_table(u'files_widget_iconset')

        # Deleting model 'FileIcon'
        db.delete_table(u'files_widget_fileicon')


    models = {
        u'files_widget.fileicon': {
            'Meta': {'object_name': 'FileIcon'},
            'base_color': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'display_text_overlay': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'icon_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['files_widget.IconSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('topnotchdev.files_widget.fields.ImageField', [], {'max_length': '200'}),
            'overlay_text': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        },
        u'files_widget.iconset': {
            'Meta': {'object_name': 'IconSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'css_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'default_icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['files_widget.FileIcon']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['files_widget']