#!/usr/bin/env python
#coding: utf8 

from django.shortcuts import render
from maistermos.models import Solicitacoes, Termos, Certificacao
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.template import RequestContext

# Create your views here.

# Página inicial do módulo maistermos
def index(request):
    context = {}
    return render(request, 'maistermos/index.html', context)

# views do model solicitaçoes
def create_solicitacao(request):
	if request.method=='GET':
		create_solicitacao_form = CreateSolicitacaoForm()
		context = {'create_solicitacao_form': create_solicitacao_form}
		return render(request, 'maistermos/index.html', context)
	else:
		create_solicitacao_form = CreateSolicitacaoForm(request.POST)
		if create_solicitacao_form.is_valid():
			new_solicitacao = create_solicitacao_form.save(commit=False)
			#Turnaround para nao ter q trabalhar com modelos relacionados
			new_solicitacao.estado = 'Nao Atendida'
			new_solicitacao.data_solicita = timezone.now()
			new_solicitacao.solicitante = 'nome usuario do auth'
			new_solicitacao.save() 
			#messages.success(request, 'Entregador Cadastrado com sucesso')
			return HttpResponseRedirect('/maistermos/solicitacao/')
		#messages.info(request, 'Formulário Não OK')
		return HttpResponseRedirect('')
 
class CreateSolicitacaoForm(forms.ModelForm):
	class Meta:
		model = Solicitacoes
		fields = ('termopt','conceitopt','sugeretermokk','sugereconceitokk')

	def __init__(self, *args, **kwargs):
		super(CreateSolicitacaoForm, self).__init__(*args, **kwargs)
		self.fields['termopt'].label = 'Termo português'
		self.fields['conceitopt'].label = 'Conceito português'
		self.fields['sugeretermokk'].label = 'Sugestão termo kikongo'
		self.fields['sugereconceitokk'].label = 'Sugestão conceito kikongo'

class SolicitacoesList(ListView):
	model = Solicitacoes
	template_name = 'maistermos/lista_solicitacao.html'
	context_object_name = 'lista_solicitacao'
	success_url = reverse_lazy('lista_solicitacao')

class SolicitacaoDetail(DetailView):
    model = Solicitacoes
    template_name = 'maistermos/detalhe_solicitacao.html'

def edit_solicitacao(request, pk):
	solicitacao = Solicitacoes.objects.get(id=pk)
	if request.method=='GET':
		create_solicitacao_form = EditSolicitacaoForm(instance=solicitacao)
		context = {'create_solicitacao_form': create_solicitacao_form,
				   'solicitacao':solicitacao
		}
		return render(request, 'maistermos/editar_solicitacao.html', context)
	elif request.method=='POST':
		edit_solicitacao_form = EditSolicitacaoForm(request.POST,instance=solicitacao)
		if edit_solicitacao_form.is_valid():
			edit_solicitacao_form.save()
			#messages.success(request,'Funcionário atualizado com sucesso')
			return HttpResponseRedirect('/maistermos/solicitacao/')
		else:
			#messages.warning(request, 'Formulário Inválido')
			return render_to_response('editar_solicitacao.html', locals(),context_instance=RequestContext(request)) 

class EditSolicitacaoForm(forms.ModelForm):
	class Meta:
		model = Solicitacoes
		fields = ('termopt','conceitopt','sugeretermokk','sugereconceitokk')

	def __init__(self, *args, **kwargs):
		super(EditSolicitacaoForm, self).__init__(*args, **kwargs)
		self.fields['termopt'].label = 'Termo português'
		self.fields['conceitopt'].label = 'Conceito português'
		self.fields['sugeretermokk'].label = 'Sugestão termo kikongo'
		self.fields['sugereconceitokk'].label = 'Sugestão conceito kikongo'







class SolicitacaoUpdate(UpdateView):
	model = Solicitacoes
	template_name = 'maistermos/criar_solicitacao.html'
	fields = ['termopt','conceitopt','sugeretermokk','sugereconceitokk']
	success_url = reverse_lazy('lista_solicitacao')

class SolicitacaoDelete(DeleteView):
    model = Solicitacoes
    template_name = 'maistermos/apagar_solicitacao.html'
    success_url = reverse_lazy('lista_solicitacao')

# views do model termos
class TermosList(ListView):
	model = Termos
	template_name = 'maistermos/lista_termo.html'
	context_object_name = 'lista_termo'
	success_url = reverse_lazy('lista_termo')

class TermoCreate(CreateView):
	model = Termos
	template_name = 'maistermos/criar_termo.html'
	fields = ['solicitacao','termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_termo')

class TermoUpdate(UpdateView):
	model = Termos
	template_name = 'maistermos/criar_termo.html'
	fields = ['solicitacao','termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_termo')

# Views do Model Certificação
class CertificacaoList(ListView):
	model = Certificacao
	template_name = 'maistermos/lista_certificacao.html'
	context_object_name = 'lista_certificacao'
	success_url = reverse_lazy('lista_certificacao')

class CertificacaoCreate(CreateView):
	model = Certificacao
	template_name = 'maistermos/criar_certificacao.html'
	fields = ['termokk','certificado','status_certificado','observacao','data_cert']
	success_url = reverse_lazy('lista_certificacao')

class CertificacaoUpdate(UpdateView):
	model = Certificacao
	template_name = 'maistermos/criar_certificacao.html'
	fields = ['termokk','certificado','status_certificado','observacao','data_cert']
	success_url = reverse_lazy('lista_certificacao')
