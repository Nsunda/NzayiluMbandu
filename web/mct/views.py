#!/usr/bin/env python
#coding: utf8 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.shortcuts import render
from mct.models import Solicitacoes, Termos, Certificacao

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from django.core.urlresolvers import reverse_lazy


# Create your views here.

# Página inicial do módulo RH
def index(request):
    context = {}
    return render(request, 'mct/index.html', context)


# views do model solicitaçoes
def detalhe_solicitacao(request, solicitacoes_id):
    p = get_object_or_404(Solicitacoes, pk=solicitacoes_id)
    return render_to_response('mct/detalhe_solicitacao.html', {'solicitacao': p})

class SolicitacoesList(ListView):
	model = Solicitacoes
	template_name = 'mct/lista_solicitacao.html'
	context_object_name = 'lista_solicitacao'
	success_url = reverse_lazy('lista_solicitacao')

class SolicitacaoCreate(CreateView):
	model = Solicitacoes
	template_name = 'mct/criar_solicitacao.html'
	fields = ['termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_solicitacao')

class SolicitacaoUpdate(UpdateView):
	model = Solicitacoes
	template_name = 'mct/criar_solicitacao.html'
	fields = ['termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_solicitacao')

class SolicitacaoDelete(DeleteView):
    model = Solicitacoes
    template_name = 'mct/apagar_solicitacao.html'
    success_url = reverse_lazy('lista_solicitacao')

# views do model termos
class TermosList(ListView):
	model = Termos
	template_name = 'mct/lista_termo.html'
	context_object_name = 'lista_termo'
	success_url = reverse_lazy('lista_termo')

class TermoCreate(CreateView):
	model = Termos
	template_name = 'mct/criar_termo.html'
	fields = ['solicitacao','termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_termo')

class TermoUpdate(UpdateView):
	model = Termos
	template_name = 'mct/criar_termo.html'
	fields = ['solicitacao','termopt','conceitopt','termokk','conceitokk']
	success_url = reverse_lazy('lista_termo')

# Views do Model Certificação
class CertificacaoList(ListView):
	model = Certificacao
	template_name = 'mct/lista_certificacao.html'
	context_object_name = 'lista_certificacao'
	success_url = reverse_lazy('lista_certificacao')

class CertificacaoCreate(CreateView):
	model = Certificacao
	template_name = 'mct/criar_certificacao.html'
	fields = ['termokk','certificado','status_certificado','observacao','data_cert']
	success_url = reverse_lazy('lista_certificacao')

class CertificacaoUpdate(UpdateView):
	model = Certificacao
	template_name = 'mct/criar_certificacao.html'
	fields = ['termokk','certificado','status_certificado','observacao','data_cert']
	success_url = reverse_lazy('lista_certificacao')

"""
def index(request):
    context = {}
    return render(request, 'mct/index.html', context)

def solicitacoes(request):
	lista_solicitacoes = Solicitacoes.objects.all().order_by('-termopt')[:10]
	context = {'lista_solicitacao':lista_solicitacoes}
	return render(request, 'mct/lista_solicitacao.html', context)

def detalhe_solicitacao(request, id_solicitacoes):
	solicitacao = get_object_or_404(Solicitacoes, pk=id_solicitacoes)
	context = {'solicitacao' : solicitacao }
	return render(request,'mct/detalhe_solicitacao.html',context)

def nova_solicitacao(request, termopt_solicitacao):
	return HttpResponse(termopt_solicitacao)
"""