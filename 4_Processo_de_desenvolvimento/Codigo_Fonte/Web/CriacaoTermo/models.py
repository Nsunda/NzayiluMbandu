from django.db import models
import datetime
from django.utils import timezone


class Port(models.Model):
	termopt = models.CharField(max_length=200)
	conceitopt = models.CharField(max_length=1800)
	data_pubpt = models.DateTimeField('date_published')
	def __unicode__(self):
		return self.termopt

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubpt < now
	was_published_recently.admin_order_field = 'data_pubpt'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

	def test_was_published_recently_with_old_port(self):
		"""
    was_published_recently() vai retornar False para CriacaoTermo cuja data_pubpt
    é mais que 1 dia
    """
		old_port = Port(data_pubpt=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_port.was_published_recently(), False)

	def test_was_published_recently_with_recent_port(self):
		"""
    was_published_recently() deve retornar True para os Termo cujo data_pubpt 
     está dentro do último dia
    """
		recent_port = Port(data_pubpt=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_port.was_published_recently(), True)


class Kik(models.Model):
	termopt = models.ForeignKey(Port)
	termokk = models.CharField(max_length=200)
	conceitokk = models.CharField(max_length=2000)
	data_pubkk = models.DateTimeField('date_published')
	def __unicode__(self):
		return self.termokk

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_pubkk < now
	was_published_recently.admin_order_field = 'data_pubkk'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

	def test_was_published_recently_with_old_kik(self):
		"""
    was_published_recently() vai retornar False para CriacaoTermo cuja data_pubkk
    é mais que 1 dia
    """
		old_kik = Kik(data_pubkk=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_kik.was_published_recently(), False)

	def test_was_published_recently_with_recent_termokk(self):
		"""
    was_published_recently() deve retornar True para as CriacaoTermo cujo data_pubkk 
     está dentro do último dia
    """
		recent_kik = Kik(data_pubkk=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_kik.was_published_recently(), True)


class Certificacao(models.Model):
	termokk = models.ForeignKey(Termokk)
	certificado = models.CharField(max_length=45)
	observacao = models.CharField(max_length=1800)
	data_cert = models.DateTimeField('date_published')
	def __unicode__(self):
		return self.certificado
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.data_cert < now
	was_published_recently.admin_order_field = 'data_cert'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

	def test_was_published_recently_with_old_certificado(self):
		"""
    was_published_recently() vai retornar False para CriacaoTermo cuja data_cert
    é mais que 1 dia
    """
		old_certificado = Certificacao(data_cert=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_certificado.was_published_recently(), False)

	def test_was_published_recently_with_recent_certificado(self):
		"""
    was_published_recently() deve retornar True para as CriacaoTermo cujo data_cert 
     está dentro do último dia
    """
		recent_certficado = Certificacao(data_cert=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_certficado.was_published_recently(), True)

class Estado(models.Model):
	certificado = models.ForeignKey(Certificacao)
	estado_texto = models.CharField(max_length=9)
	def __unicode__(self):
		return self.estado