#!/usr/bin/env python
#coding: utf8 

from django import forms
from django.forms import ModelForm
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado

# Create your views here.
class TermoptForm(ModelForm):
	class Meta:
		model = Termopt
		fields = ('termo','conceito')
		widgets = {
            'conceito': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

	def __init__(self, *args, **kwargs):
		super(TermoptForm, self).__init__(*args, **kwargs)
		self.fields['termo'].label = 'Termo'
		self.fields['conceito'].label = 'Conceito'



