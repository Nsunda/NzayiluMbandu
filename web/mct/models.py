from datetime import datetime
from django.db import models

# Create your models here.

class Solicitacoes(models.Model):
	termopt = models.CharField(max_length=200)
	conceitopt = models.CharField(max_length=1800)
	sugeretermokk = models.CharField(max_length=200)
	sugereconceitokk = models.CharField(max_length=2000)
	solicitante = models.CharField(max_length=100)
	data_solicita = models.DateTimeField('data_solicita')
	respondente = models.CharField(max_length=100)
	data_inicio_analise = models.DateTimeField('data_inicio_analise')
	data_fim_analise = models.DateTimeField('data_inicio_analise')
	STATUS_SOLICITACAO = (
		('N_A', 'Nao Atendido'),
		('E_A', 'Em analise'),
		('T_P', 'Atendida'),
	)
	status_certificado = models.CharField(max_length=17, choices=STATUS_SOLICITACAO)

	def __unicode__(self):
		return self.termopt
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now


class Termos(models.Model):
	solicitacao = models.ForeignKey(Solicitacoes)
	termokk = models.CharField(max_length=200)
	conceitokk = models.CharField(max_length=2000)
	data_criakk = models.DateTimeField('date_published', default=datetime.now())
	STATUS_CERTFICADO = (
		('T_A', 'Nao Analisado'),
		('T_A', 'Em Analise'),
		('T_R', 'Aceita'),
		('T_R', 'Rejeitado'),
	)
	status_certificado = models.CharField(max_length=17, choices=STATUS_CERTFICADO)
	observacao_certificado = models.CharField(max_length=800)
	responsavel_observacao = models.CharField(max_length=100)
	def __unicode__(self):
		return self.termopt
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now


class Certificacao(models.Model):
	termokk = models.ForeignKey(Termos)
	certificador = models.CharField(max_length=100)
	certificado = models.CharField(max_length=45, blank=True)
	data_cert = models.DateTimeField('date_published')
	def __unicode__(self):
		return self.certificado
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_cert < now