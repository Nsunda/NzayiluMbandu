# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Solicitacoes'
        db.create_table(u'mct_solicitacoes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('termopt', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('conceitopt', self.gf('django.db.models.fields.CharField')(max_length=1800)),
            ('sugeretermokk', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sugereconceitokk', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('solicitante', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('data_solicita', self.gf('django.db.models.fields.DateTimeField')()),
            ('respondente', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('data_inicio_analise', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_fim_analise', self.gf('django.db.models.fields.DateTimeField')()),
            ('status_certificado', self.gf('django.db.models.fields.CharField')(max_length=17)),
        ))
        db.send_create_signal(u'mct', ['Solicitacoes'])

        # Adding model 'Termos'
        db.create_table(u'mct_termos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solicitacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mct.Solicitacoes'])),
            ('termokk', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('conceitokk', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('data_criakk', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 13, 0, 0))),
            ('status_certificado', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('observacao_certificado', self.gf('django.db.models.fields.CharField')(max_length=800)),
            ('responsavel_observacao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'mct', ['Termos'])

        # Adding model 'Certificacao'
        db.create_table(u'mct_certificacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('termokk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mct.Termos'])),
            ('certificador', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('certificado', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('data_cert', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'mct', ['Certificacao'])


    def backwards(self, orm):
        # Deleting model 'Solicitacoes'
        db.delete_table(u'mct_solicitacoes')

        # Deleting model 'Termos'
        db.delete_table(u'mct_termos')

        # Deleting model 'Certificacao'
        db.delete_table(u'mct_certificacao')


    models = {
        u'mct.certificacao': {
            'Meta': {'object_name': 'Certificacao'},
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'certificador': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'data_cert': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'termokk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mct.Termos']"})
        },
        u'mct.solicitacoes': {
            'Meta': {'object_name': 'Solicitacoes'},
            'conceitopt': ('django.db.models.fields.CharField', [], {'max_length': '1800'}),
            'data_fim_analise': ('django.db.models.fields.DateTimeField', [], {}),
            'data_inicio_analise': ('django.db.models.fields.DateTimeField', [], {}),
            'data_solicita': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'respondente': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'solicitante': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status_certificado': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'sugereconceitokk': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'sugeretermokk': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'termopt': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'mct.termos': {
            'Meta': {'object_name': 'Termos'},
            'conceitokk': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'data_criakk': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 13, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacao_certificado': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'responsavel_observacao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'solicitacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mct.Solicitacoes']"}),
            'status_certificado': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'termokk': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mct']