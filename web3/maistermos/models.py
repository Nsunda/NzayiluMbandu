#coding: utf8 
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# LINGUAS SUPORTADAS PELO SISTEMA
LINGUA = (
	('Kikongo', 'Kikongo'),
	('Kibundo', 'Kibundo'),
	('Espanhol', 'Espanhol'),
)

LINGUA_CONCEITO = (
	('Portugues', 'Portugues'),
	('Kikongo', 'Kikongo'),
	('Kibundo', 'Kibundo'),
	('Espanhol', 'Espanhol'),
)

# TERMO EM PORTUGUÊS:
class Termopt(models.Model):
	termo = models.CharField(max_length=200)
	conceito = models.CharField(max_length=1800) 	
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_termopt = models.ForeignKey(User, related_name='usuario_insere_termopt')

	def __unicode__(self):
		return self.termo
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

# SOLICITACAO:
ESTADO_SOLICITACAO = (
		('Nao Atendida', 'Nao Atendida'),		# Quando o termo foi solicitado mas ninguem ainda propôs
		('Em criacao', 'Em criacao'),     		# Quando um ou vários linguistas marcou que esta analisando
		('Atendida', 'Atendida'), # Quando um linguista já fez uma proposta e esta em processo de certificação
)
class Solicitacao(models.Model):
	termoref = models.ForeignKey(Termopt, related_name='termoref_solicitac')
	linguax = models.CharField(max_length=20, choices=LINGUA, default='Kikongo')
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_atendente = models.ForeignKey(User, related_name='usuario_atendente', blank=True, null=True)
	data_inicio_atendimento = models.DateTimeField('data_inicio_atendimento', blank=True, null=True)
	data_fim_atendimento = models.DateTimeField('data_inicio_atendimento', blank=True, null=True)
	estado = models.CharField(max_length=20, choices=ESTADO_SOLICITACAO)	
	usuario_solicitantes = models.ManyToManyField(User, related_name='usuario_solicitantes')
	usuario_em_analise = models.ManyToManyField(User, related_name='usuario_em_analise')

	def __unicode__(self):
		return self.estado
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

# TERMO NA LINGUA "X":
ESTADO_TERMO_LX = (
		('Proposto', 'Proposto'),       # Quando o linguista propõe o termo um ou vários linguistas marcou que esta analisando
		('Em certificacao', 'Em certificacao'),   # Quando alguma agência certificadora esta em processo de certificação
		('Nao certificado', 'Nao certificado'),		# Quando o agente certificador já analisou e rejeitou
		('Certificado', 'Certificado'),		# Quando o agente certificador já analisou e rejeitou
	)

class Termolx(models.Model):
	termo = models.CharField(max_length=200)
	linguax = models.CharField(max_length=20, choices=LINGUA)
	termoref = models.ForeignKey(Termopt)
	solicitacao = models.ForeignKey(Solicitacao) 
	justificativa = models.CharField(max_length=1800)
	nao_certificado = models.CharField(max_length=1800)
	estado =  models.CharField(max_length=20, choices=ESTADO_TERMO_LX)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_termolx = models.ForeignKey(User, related_name='usuario_insere_termolx')
	usuario_aprova_termolx = models.ManyToManyField(User, related_name='usuario_aprova_termolx')
	usuario_rejeita_termolx = models.ManyToManyField(User, related_name='usuario_rejeita_termolx')

	def __unicode__(self):
		return self.termo
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

# CONCEITOS:
class Conceito(models.Model):
	conceito = models.CharField(max_length=3000)
	contexto = models.CharField(max_length=200)
	termoref = models.ForeignKey(Termopt, related_name='termoref_conceito') 
	linguax = models.CharField(max_length=20, choices=LINGUA_CONCEITO, default='Portugues')
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_conceito = models.ForeignKey(User, related_name='usuario_insere_conceito')
	usuario_aprova_conceito = models.ManyToManyField(User, related_name='usuario_aprova_conceito')
	usuario_rejeita_conceito = models.ManyToManyField(User, related_name='usuario_rejeita_conceito')

	def __unicode__(self):
		return self.conceito
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

# SUGESTÃO:
class Sugestao(models.Model):
	solicitacao = models.ForeignKey(Solicitacao)
	termo = models.CharField(max_length=200)
	justificativa = models.CharField(max_length=1800)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_sugestao = models.ForeignKey(User, related_name='usuario_insere_sugetao')
	usuario_aprova_sugestao = models.ManyToManyField(User, related_name='usuario_aprova_sugetao')
	usuario_rejeita_sugestao = models.ManyToManyField(User, related_name='usuario_rejeita_sugetao')

	def __unicode__(self):
		return self.termo
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now

# CERTIFICADO:
LISTA_AGENCIAS = (
		('MESCT', 'MESCT'),       # Quando o linguista propõe o termo um ou vários linguistas marcou que esta analisando
		('MC', 'MC'),   # Quando alguma agência certificadora esta em processo de certificação	# Quando o agente certificador já analisou e rejeitou
	)
class Certificado(models.Model):
	termolx = models.ForeignKey(Termolx)
	agencia_certificadora = models.CharField(max_length=20, choices=LISTA_AGENCIAS,default='MC')
	corpo_certificado = models.CharField(max_length=500)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_certificado = models.ForeignKey(User, related_name='usuario_insere_certificado')

	def __unicode__(self):
		return self.agencia_certificadora
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_cert < now
