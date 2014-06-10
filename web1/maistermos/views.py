#!/usr/bin/env python
#coding: utf8 

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado
from maistermos.forms import TermoptForm

# VIEW PARA CADASTRO DE TERMOS EM PORTUGUÊS:
############################################################################################
MENSAGEM_SUCESSO_CADASTRO = 'O termo foi cadastrado com sucesso'
MENSAGEM_ERRO_FORMULARIO_CADASTRO = 'O formulário esta com erro'
MENSAGEM_ERRO_TERMO_EXISTE_CADASTRO = 'O termo já existe'

@login_required
def cadastra_termopt(request):
	if request.method=='GET':
		termopt_form = TermoptForm()
		context = {'termopt_form': termopt_form}
		return render(request, 'maistermos/termopt/cadastra_termopt.html', context)
	else:
		termopt_form = TermoptForm(request.POST)
		if termopt_form.is_valid():
			termo = termopt_form.save(commit=False)
			cont_termopt = Termopt.objects.filter(termo=termo.termo).count()
			if cont_termopt == 0:
				# Essa linha de codigo cria o objeto na memória mas não salva, permitindo
				# utilizar os atributos.
				termo.data_insercao = timezone.now()
				termo.usuario_insere_termopt = request.user
				termo.save()
				messages.success(request, MENSAGEM_SUCESSO_CADASTRO)
				return HttpResponseRedirect('/maistermos/termopt/lista/')
			else:
				messages.info(request, MENSAGEM_SUCESSO_CADASTRO)
				return HttpResponseRedirect('/maistermos/termopt/cadastra/')
		messages.info(request, MENSAGEM_ERRO_FORMULARIO_CADASTRO)
		return HttpResponseRedirect('/maistermos/termopt/cadastra/')
############################################################################################

# VIEW PARA LISTAGEM DE TERMOS EM PORTUGUÊS:
############################################################################################
MENSAGEM_SUCESSO_LISTA = 'O termo foi cadastrado com sucesso'
MENSAGEM_ERRO_FORMULARIO_LISTA = 'O formulário esta com erro'
MENSAGEM_ERRO_TERMO_EXISTE_LISTA = 'O termo já existe'
MENSAGEM_ERRO_BUSCA = 'Não existem termos que cumpram as condições'

@login_required
def lista_termopt(request):
	if request.method=='GET':
		termospt_list = Termopt.objects.all()
		titulo_lista = 'Termos cadastrados'
		context = {'termospt_list': termospt_list,
					'titulo_lista': titulo_lista
		}
		return render(request, 'maistermos/termopt/lista_termopt.html', context)
	else:
		query_string = request.POST['q']
		termospt_list_query = Termopt.objects.filter(termo__contains=query_string)
		count_termospt_list_query = termospt_list_query.count()
		if count_termospt_list_query != 0:
			titulo_lista = 'Termos cadastrados'
		else:
			titulo_lista = 'Resultado da busca'
			messages.info(request, MENSAGEM_ERRO_BUSCA)
		context = {'termospt_list': termospt_list_query,
					'titulo_lista': titulo_lista
		}
		return render(request, 'maistermos/termopt/lista_termopt.html', context)
		
############################################################################################

# VIEW PARA DETALHES DE TERMOS EM PORTUGUÊS:
############################################################################################

@login_required
def detalhe_termopt(request, pk):
	if request.method=='GET':
		termopt = Termopt.objects.get(id=pk)
		context = {'termopt': termopt}
		return render(request, 'maistermos/termopt/detalhe_termopt.html', context)	
############################################################################################

