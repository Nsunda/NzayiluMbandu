#!/usr/bin/env python
#coding: utf8 

from django import forms
from django.forms import ModelForm
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado

TEXT_AREA_ROWS = 6

TRADUCOES = (
	('Portugues-kikongo', 'Portugues-kikongo'),
	('kikongo-Portugues', 'kikongo-Portugues'),
)

#  FORM TERMO EM PORTUGUÊS:
class TermoptForm(ModelForm):
	class Meta:
		model = Termopt
		fields = ('termo','conceito')
		widgets = {
            'conceito': forms.Textarea(attrs={'cols': 80, 'rows': TEXT_AREA_ROWS}),
        }

	def __init__(self, *args, **kwargs):
		super(TermoptForm, self).__init__(*args, **kwargs)
		self.fields['termo'].label = 'Termo'
		self.fields['conceito'].label = 'Conceito principal'

# 
class ConceitoForm(ModelForm):
	class Meta:
		model = Conceito
		fields = ('linguax', 'contexto', 'conceito')
		widgets = {
            'conceito': forms.Textarea(attrs={'cols': 80, 'rows': TEXT_AREA_ROWS}),
        }

	def __init__(self, *args, **kwargs):
		super(ConceitoForm, self).__init__(*args, **kwargs)
		self.fields['linguax'].label = 'Lingua'
		self.fields['conceito'].label = 'Conceito'
		self.fields['contexto'].label = 'Contexto'

class SolicitacaoForm(ModelForm):
	class Meta:
		model = Solicitacao
		fields = ('linguax',)

	def __init__(self, *args, **kwargs):
		super(SolicitacaoForm, self).__init__(*args, **kwargs)
		self.fields['linguax'].label = 'Lingua solicitada'

class SugestaoForm(ModelForm):
	class Meta:
		model = Sugestao
		fields = ('termo', 'justificativa')
		widgets = {
            'justificativa': forms.Textarea(attrs={'cols': 80, 'rows': TEXT_AREA_ROWS}),
        }

	def __init__(self, *args, **kwargs):
		super(SugestaoForm, self).__init__(*args, **kwargs)
		self.fields['termo'].label = 'Termo sugerido'
		self.fields['justificativa'].label = 'Justificativa'

#  FORM TERMO NA LINGUA NACIONAL:
class TermolxForm(ModelForm):
	class Meta:
		model = Termolx
		fields = ('termo','justificativa')
		widgets = {
            'justificativa': forms.Textarea(attrs={'cols': 80, 'rows': TEXT_AREA_ROWS}),
        }

	def __init__(self, *args, **kwargs):
		super(TermolxForm, self).__init__(*args, **kwargs)
		self.fields['termo'].label = 'Novo termo'
		self.fields['justificativa'].label = 'Justificativa do termo'

#  FORM TERMO NA LINGUA NACIONAL:
class CertificadoForm(ModelForm):
	class Meta:
		model = Certificado
		fields = ('agencia_certificadora','corpo_certificado')
		widgets = {
            'corpo_certificado': forms.Textarea(attrs={'cols': 80, 'rows': TEXT_AREA_ROWS}),
        }

	def __init__(self, *args, **kwargs):
		super(CertificadoForm, self).__init__(*args, **kwargs)
		self.fields['agencia_certificadora'].label = 'Orgão certificador'
		self.fields['corpo_certificado'].label = 'Certificado'
