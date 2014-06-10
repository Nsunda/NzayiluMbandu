#coding: utf8 
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Lista das diferentes linguas suportadas pelo sistema para criação de novos termos
LINGUA = (
	('Portugues', 'Portugues'),
	('Kikongo', 'Kikongo'),
	('Kimbundu', 'Kimbundu'),
	('Umbundu', 'Umbundu'),
	('Nganguela', 'Nganguela'),
	('Cokwe', 'Cokwe'),
)

# MODEL DO TERMO EM PORTUGUÊS:
############################################################################################
# Esse model é o objeto central do modulo. todo o que esta envolvido com a criação
# de um novo termo esta relacionado com esse objeto. Por exemplo, os novos termos
# nas linguas nacionais angolanas estarão sempre referenciados
class Termopt(models.Model):
	termo = models.CharField(max_length=200)
	# Esse é o conceito principal, adicionado pelo dono do sistema
	conceito = models.CharField(max_length=1800) 	
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_termopt = models.ForeignKey(User, related_name='usuario_insere_termopt')

	def __unicode__(self):
		return self.termo
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now
		
############################################################################################

# MODEL DO TERMO NA LINGUA "X":
############################################################################################ 
# Lingua X refere-se a qualquer opção das linguas que o sistema suporta. 
# Mesmo que o escopo do primeiro protótipo seja o Kikongo já ficou pronto o sistema 
# para adicionar termos nas outras linguas nacionais angolanas

# Ao longo do ciclo de vida da criação de um novo termo numa lingua nacional angolana
# em que ainda não existe uma palavra, o termo passa pelas seguintes fases:
ESTADO_TERMO_LX = (
		('Proposto', 'Proposto'),       # Quando o linguista propõe o termo um ou vários linguistas marcou que esta analisando
		('Em analise', 'Em analise'),   # Quando alguma agência certificadora esta em processo de certificação
		('Rejeitado', 'Rejeitado'),		# Quando o agente certificador já analisou e rejeitou
		('Aprovado', 'Aprovado'),		# Quando o agente certificador já analisou e aprovou
	)

class Termolx(models.Model):
	termo = models.CharField(max_length=200)
	linguax = models.CharField(max_length=20, choices=LINGUA)
	termoref = models.ForeignKey(Termopt)
	# Essa é a Tradução literal do Termopt.conceito
	conceito = models.CharField(max_length=1800)
	justificativa = models.CharField(max_length=1800)
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
############################################################################################

# MODELO DE CONCEITOS:
############################################################################################
# Quando o termo é criado em português o usuário cadastra um conceito ou definição, porém,
# outros usuários poderiam querer adicionar novos conceitos ou definições assiadas ao mesmo
# termo. Esses conceitos podem ser avaliados por outros usuários que podem aprovar ou rejeitar
# o conceito (tipo o like do facebook). Assim, quando o termo é consultado aparecerá uma lista
# de conceitos na lingua em que foi filtrada a coluna e listará primeiro os conceitos com mais
# aprovações. 
# Outra razão para criar este model é que um termo pode ter uma tradução do conceito em linguas
# nacionais angolanas mesmo antes de existir o termo, assim os alunos podem entender o conceito
# e aprender de informática
class Conceito(models.Model):
	# Esse é um proposto pelos professores (Materiais de ensino)
	conceito = models.CharField(max_length=1800)
	termoref = models.ForeignKey(Termopt, related_name='termoref_conceito') 
	linguax = models.CharField(max_length=20, choices=LINGUA)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_conceito = models.ForeignKey(User, related_name='usuario_insere_conceito')
	# Outros profesores poderão aprovar o conceito para ganhar pontos e credibilidade
	usuario_aprova_conceito = models.ManyToManyField(User, related_name='usuario_aprova_conceito')
	# Outros profesores poderão rejeitar o conceito para perder pontos e credibilidade
	usuario_rejeita_conceito = models.ManyToManyField(User, related_name='usuario_rejeita_conceito')

	def __unicode__(self):
		return self.conceito
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now
############################################################################################

# MODELO DE SOLICITACAO:
############################################################################################
# Ao longo do ciclo de vida da solicitação ela passa pelos seguintes estados:
ESTADO_SOLICITACAO = (
		('Nao Atendida', 'Nao Atendida'),		# Quando o termo foi solicitado mas ninguem ainda propôs
		('Em criacao', 'Em criacao'),     		# Quando um ou vários linguistas marcou que esta analisando
		('Em certificacao', 'Em certificacao'), # Quando um linguista já fez uma proposta e esta em processo de certificação
		('Rejeitado', 'Rejeitado'),		  		# Quando o agente certificador já analisou e rejeitou
		('Aprovado', 'Aprovado'),		 		# Quando o agente certificador já analisou e aprovou
	)

class Solicitacao(models.Model):
	termoref = models.ForeignKey(Termopt, related_name='termoref_solicitac')
	proposta = models.ForeignKey(Termolx, related_name='proposta_termolx')
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_atendente = models.ForeignKey(User, related_name='usuario_atendente')
	data_inicio_atendimento = models.DateTimeField('data_inicio_atendimento', default=datetime.now())
	data_fim_atendimento = models.DateTimeField('data_inicio_atendimento', default=datetime.now())
	estado = models.CharField(max_length=20, choices=ESTADO_SOLICITACAO)	
	usuario_solicitantes = models.ManyToManyField(User, related_name='usuario_solicitantes')
	usuario_em_analise = models.ManyToManyField(User, related_name='usuario_em_analise')

	def __unicode__(self):
		return self.estado
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now
############################################################################################

# MODELO DE SUGESTÃO:
############################################################################################
# O solicitante da criação do termo, quem a principio no perfil de professor não possui direito nem
# capacidades para criar e propor um novo termo, poderia fazer uma sugestão para o linguista.
# Várias pessoas poderiam assinar como solicitantes do mesmo termo e poderiam dar novas sugestões.
# O linguista no seu processo de criação do termo pode utilizar todas essas sugestões para inspiração.
class Sugestao(models.Model):
	solicitacao = models.ForeignKey(Solicitacao)
	termo = models.CharField(max_length=200)
	justificativa = models.CharField(max_length=1800)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_sugetao = models.ForeignKey(User, related_name='usuario_insere_sugetao')
	usuario_aprova_sugetao = models.ManyToManyField(User, related_name='usuario_aprova_sugetao')
	usuario_rejeita_sugetao = models.ManyToManyField(User, related_name='usuario_rejeita_sugetao')

	def __unicode__(self):
		return self.termo
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now
############################################################################################

# MODELO DE CERTIFICAÇÃO:
############################################################################################
# A agencia certificadora emite o certificado e disponibiliza para ser utilizado como "Carimbo"
# ou prova de que o termo pode ser utilizado com confiança
class Certificado(models.Model):
	termo = models.ForeignKey(Termolx)
	agencia_certificadora = models.CharField(max_length=20, choices=ESTADO_SOLICITACAO)
	corpo_certificado = models.CharField(max_length=500)
	data_insercao = models.DateTimeField('data_insercao', default=datetime.now())
	usuario_insere_certificado = models.ForeignKey(User, related_name='usuario_insere_certificado')

	def __unicode__(self):
		return self.agencia_certificadora
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_cert < now
