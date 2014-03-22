from django.db import models

# Create your models here.

class Termo(models.Model):
	termopt = models.CharField(max_length=200)
	conceitopt = models.CharField(max_length=1800)
	termokk = models.CharField(max_length=200)
	conceitokk = models.CharField(max_length=1800)
	def __unicode__(self):
		return self.termopt