#!/usr/bin/env python
#coding: utf8 

from django.shortcuts import render
from django.contrib import auth, messages
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

TAMANHO_PAGINA = 10

# VIEW PARA CONSULTAR O DICIONARIO:
############################################################################################
MENSAGEM_AJUDA_USO_DICIONARIO = 'ajuda uso dicionario'
DROPDOWNLIST_OPCAO = (
	'Portugues-Kikongo',
	'Kikongo-Portugues',
)

def consulta_termo(request):
	if request.method=='GET':
		#messages.info(request,MENSAGEM_AJUDA_USO_DICIONARIO)
		context = {'traducao_opcao_list': DROPDOWNLIST_OPCAO}
		return render(request, 'dicionario/consulta_termo.html', context)
	else:
		query_string = request.POST['q']
		filtro_busca = request.POST["filtro_busca"]
		linguas = filtro_busca.split("-")
		lingua_origem = linguas[0]
		lingua_destino = linguas[1]
		termopt = Termopt.objects.filter(termo=query_string).first()
		conceitos_list_query = None
		paginator_conceitos = None
				
		if lingua_origem == 'Portugues':
			termoOrigem = Termopt.objects.filter(termo=query_string).first()
		else:
			termolx_origen = Termolx.objects.filter(termo=query_string,linguax=lingua_origem).first()
			if termolx_origen == None:
				termoOrigem = termolx_origen
			else:
				termoOrigem = Termopt.objects.get(id=termolx_origen.termoref.id)

		context = {'traducao_opcao_list': DROPDOWNLIST_OPCAO}
		if termoOrigem == None:
			termoDestino = termoOrigem
			messages.info(request,"O termo %s nao existe" % query_string)
			return render(request, 'dicionario/consulta_termo.html', context)
		else:
			conceitos_list_query_all = Conceito.objects.filter(termoref=termopt.id,linguax=lingua_destino)
			# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
			paginator_conceitos = Paginator(conceitos_list_query_all, TAMANHO_PAGINA)
			page = request.GET.get('page')
			try:
				conceitos_list_query = paginator_conceitos.page(page)
			except PageNotAnInteger: 
				 conceitos_list_query = paginator_conceitos.page(1) # pagina não é inteiro, apresenta a primeira
			except EmptyPage: 
				conceitos_list_query = paginator_conceitos.page(paginator_conceitos.num_pages) # pagina fora do range, apresenta ultima
			#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

		if lingua_destino == 'Portugues':
			termoDestino = termoOrigem
		else:
			termoDestino = Termolx.objects.filter(termoref=termopt,linguax=lingua_destino).first()
			if termoDestino == None:
				messages.info(request,"Nenhum resultado para o termo %s na lingua destino" % query_string)
		context = {'traducao_opcao_list': DROPDOWNLIST_OPCAO,'termoOrigem':query_string,'lingua_origem':lingua_origem,
						'termoDestino':termoDestino,'lingua_destino':lingua_destino, 
						'conceitos_list_query': conceitos_list_query, 'paginator_conceitos':paginator_conceitos}
		return render(request, 'dicionario/consulta_termo.html', context)

@login_required
def aprova_adi_conceito(request):
	context = RequestContext(request)
	conceito_id = None
	conceito = None
	if request.method == 'GET':
		conceito_id = request.GET['conceito_id']
		if conceito_id != None:
			conceito = Conceito.objects.get(id=conceito_id)
			conceito.usuario_aprova_conceito.add(request.user)
			atualiza = conceito.usuario_aprova_conceito.count()
		return HttpResponse(atualiza)

@login_required
def aprova_rem_conceito(request):
	context = RequestContext(request)
	conceito_id = None
	conceito = None
	if request.method == 'GET':
		conceito_id = request.GET['conceito_id']
		if conceito_id != None:
			conceito = Conceito.objects.get(id=conceito_id)
			conceito.usuario_aprova_conceito.remove(request.user)
			atualiza = conceito.usuario_aprova_conceito.count()
		return HttpResponse(atualiza)

@login_required
def rejeita_adi_conceito(request):
	context = RequestContext(request)
	conceito_id = None
	conceito = None
	if request.method == 'GET':
		conceito_id = request.GET['conceito_id']
		if conceito_id != None:
			conceito = Conceito.objects.get(id=conceito_id)
			conceito.usuario_rejeita_conceito.add(request.user)
			atualiza = conceito.usuario_rejeita_conceito.count()
		return HttpResponse(atualiza)

@login_required
def rejeita_rem_conceito(request):
	context = RequestContext(request)
	conceito_id = None
	conceito = None
	if request.method == 'GET':
		conceito_id = request.GET['conceito_id']
		if conceito_id != None:
			conceito = Conceito.objects.get(id=conceito_id)
			conceito.usuario_rejeita_conceito.remove(request.user)
			atualiza = conceito.usuario_rejeita_conceito.count()
		return HttpResponse(atualiza)

@login_required
def aprova_adi_sugestao(request):
	context = RequestContext(request)
	sugestao_id = None
	sugestao = None
	if request.method == 'GET':
		sugestao_id = request.GET['sugestao_id']
		if sugestao_id != None:
			sugestao = Sugestao.objects.get(id=sugestao_id)
			sugestao.usuario_aprova_sugestao.add(request.user)
			atualiza = sugestao.usuario_aprova_sugestao.count()
		return HttpResponse(atualiza)

@login_required
def aprova_rem_sugestao(request):
	context = RequestContext(request)
	sugestao_id = None
	sugestao = None
	if request.method == 'GET':
		sugestao_id = request.GET['sugestao_id']
		if sugestao_id != None:
			sugestao = Sugestao.objects.get(id=sugestao_id)
			sugestao.usuario_aprova_sugestao.remove(request.user)
			atualiza = sugestao.usuario_aprova_sugestao.count()
		return HttpResponse(atualiza)

@login_required
def rejeita_adi_sugestao(request):
	context = RequestContext(request)
	sugestao_id = None
	sugestao = None
	if request.method == 'GET':
		sugestao_id = request.GET['sugestao_id']
		if sugestao_id != None:
			sugestao = Sugestao.objects.get(id=sugestao_id)
			sugestao.usuario_rejeita_sugestao.add(request.user)
			atualiza = sugestao.usuario_rejeita_sugestao.count()
		return HttpResponse(atualiza)

@login_required
def rejeita_rem_sugestao(request):
	context = RequestContext(request)
	sugestao_id = None
	sugestao = None
	if request.method == 'GET':
		sugestao_id = request.GET['sugestao_id']
		if sugestao_id != None:
			sugestao = Sugestao.objects.get(id=sugestao_id)
			sugestao.usuario_rejeita_sugestao.remove(request.user)
			atualiza = sugestao.usuario_rejeita_sugestao.count()
		return HttpResponse(atualiza)

@login_required
def nao_estudo_solicitacao(request):
	context = RequestContext(request)
	solicitacao_id = None
	solicitacao = None
	if request.method == 'GET':
		solicitacao_id = request.GET['solicitacao_id']
		if solicitacao_id != None:
			solicitacao = Solicitacao.objects.get(id=solicitacao_id)
			solicitacao.usuario_em_analise.remove(request.user)
			atualiza = solicitacao.usuario_em_analise.count()
		return HttpResponse(atualiza)

@login_required
def sim_estudo_solicitacao(request):
	context = RequestContext(request)
	solicitacao_id = None
	solicitacao = None
	if request.method == 'GET':
		solicitacao_id = request.GET['solicitacao_id']
		if solicitacao_id != None:
			solicitacao = Solicitacao.objects.get(id=solicitacao_id)
			solicitacao.usuario_em_analise.add(request.user)
			atualiza = solicitacao.usuario_em_analise.count()
		return HttpResponse(atualiza)