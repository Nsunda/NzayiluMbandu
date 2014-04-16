#coding: utf8 
from datetime import datetime
from django.db import models

# Model SOlicitacoes
class Solicitacoes(models.Model):
	termopt = models.CharField(max_length=200, blank=True)
	conceitopt = models.CharField(max_length=1800, blank=True)
	sugeretermokk = models.CharField(max_length=200, blank=True)
	sugereconceitokk = models.CharField(max_length=2000, blank=True)
	solicitante = models.CharField(max_length=100, blank=True) #mudara para tabela User do auth
	data_solicita = models.DateTimeField('data_solicita', default=datetime.now(), blank=True)
	respondente = models.CharField(max_length=100, blank=True)
	data_inicio_atendim = models.DateTimeField('data_inicio_atendim', default=datetime.now(), blank=True)
	data_fim_atendim = models.DateTimeField('data_fim_atendim', default=datetime.now(), blank=True)
	STATUS_SOLICITACAO = (
		('Nao Atendida', 'Nao Atendida'),
		('Em Atendimento', 'Em Atendimento'),
		('Atendida', 'Atendida'),
	)
	estado = models.CharField(max_length=17, choices=STATUS_SOLICITACAO, blank=True)

	def __unicode__(self):
		return self.termopt
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

#Model Certificacao
class Certificacao(models.Model):
	certificador = models.CharField(max_length=100)
	corpo_certificado = models.CharField(max_length=45, blank=True)
	data_cert = models.DateTimeField('date_published')
	def __unicode__(self):
		return self.certificado
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_cert < now

# Model Termos
class Termos(models.Model):
	solicitacao = models.ForeignKey(Solicitacoes)
	certificado = models.ForeignKey(Certificacao)
	termokk = models.CharField(max_length=200)
	conceitokk = models.CharField(max_length=2000)
	data_propostakk = models.DateTimeField('data_propostakk', default=datetime.now())
	STATUS_TERMO = (
		('Não Analisado', 'Não Analisado'),
		('Em Análise', 'Em Análise'),
		('Rejeitado', 'Rejeitado'),
		('Aprovado', 'Aprovado'),
	)
	status = models.CharField(max_length=17, choices=STATUS_TERMO)
	observacao_analise = models.CharField(max_length=800)
	responsavel_analise = models.CharField(max_length=100)
	def __unicode__(self):
		return self.termopt
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

