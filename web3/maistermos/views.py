#!/usr/bin/env python
#coding: utf8 

from django.shortcuts import render
#from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado
from maistermos.forms import TermoptForm, ConceitoForm, SolicitacaoForm, SugestaoForm, TermolxForm, CertificadoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import render_to_response

TAMANHO_PAGINA = 5
MENSAGEM_ERRO_FORMULARIO = 'O formulário esta com erro'
MENSAGEM_SEM_PERMISSAO = 'Você não tem permissão de fazer isso'

def mais_termos(request):
	context = {}
	return render_to_response('maistermos/mais_termos.html', locals(), context_instance=RequestContext(request))
	
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA TERMOS EM PORTUGUÊS ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE TERMOS EM PORTUGUÊS:
MENSAGEM_SUCESSO_CADASTRO_TERMOPT = 'O termo em português foi cadastrado com sucesso'
MENSAGEM_ERRO_TERMO_EXISTE_CADASTRO_TERMOPT = "O termo em português já existe"
@login_required
def cadastra_termopt(request):
	if request.user.has_perm("maistermos.add_termopt"):
		if request.method=='GET':
			termopt_form = TermoptForm()
			return render_to_response('maistermos/termopt/cadastra_termopt.html', locals(), context_instance=RequestContext(request))
		else:
			termopt_form = TermoptForm(request.POST)
			if termopt_form.is_valid():
				termo = termopt_form.save(commit=False)
				cont_termopt = Termopt.objects.filter(termo=termo.termo).count()
				if cont_termopt == 0:
					termo.data_insercao = timezone.now()
					termo.usuario_insere_termopt = request.user
					termo.save()
					messages.success(request, MENSAGEM_SUCESSO_CADASTRO_TERMOPT)
					return HttpResponseRedirect('/maistermos/termopt/lista/')
				else:
					messages.info(request, MENSAGEM_ERRO_TERMO_EXISTE_CADASTRO_TERMOPT)
					return HttpResponseRedirect('/maistermos/termopt/cadastra/')
			messages.error(request, MENSAGEM_ERRO_FORMULARIO)
			return HttpResponseRedirect('/maistermos/termopt/cadastra/')
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect('/maistermos/termopt/lista/')

# LISTA DE TERMOS EM PORTUGUÊS:
MENSAGEM_ERRO_BUSCA = 'Não existem termos em português que cumpram as condições'
DROPDOWNLIST_OPCAO_LISTA_TERMO = (
	"Todos os termos",
	"Cadastrados por mim",)
@login_required
def lista_termopt(request):
	if request.method=='GET':
		termospt_list_all = Termopt.objects.all()
		titulo_lista = 'GERIR TERMOS EM PORTUGUÊS'
	else:
		filtro_busca = request.POST["filtro_busca"]
		query_string = request.POST['q']
		if filtro_busca == "Todos os termos":
			termospt_list_all = Termopt.objects.filter(termo__contains=query_string)
			titulo_lista = 'RESULTADO DA BUSCA EM: TODOS OS TERMOS EM PORTUGUÊS'
		else:
			termospt_list_all = Termopt.objects.filter(termo__contains=query_string, usuario_insere_termopt=request.user)
			titulo_lista = 'RESULTADO DA BUSCA EM: TERMOS EM PORTUGUÊS CADASTRADOS POR MIM'
		count_termospt_list_query = termospt_list_all.count()
		if count_termospt_list_query == 0:
			messages.info(request, MENSAGEM_ERRO_BUSCA)
	# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	paginator = Paginator(termospt_list_all, TAMANHO_PAGINA)
	page = request.GET.get('page')
	try:
		termospt_list = paginator.page(page)
	except PageNotAnInteger: 
		termospt_list = paginator.page(1) # pagina não é inteiro, apresenta a primeira
	except EmptyPage: 
		termospt_list = paginator.page(paginator.num_pages) # pagina fora do range, apresenta ultima
	#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	context = {'termospt_list': termospt_list, 'traducao_opcao_list': DROPDOWNLIST_OPCAO_LISTA_TERMO,
				'titulo_lista': titulo_lista, 'paginator': paginator}
	return render(request, 'maistermos/termopt/lista_termopt.html', context)

# DETALHES DE TERMOS EM PORTUGUÊS:
@login_required
def detalhe_termopt(request, pk):
	if request.method=='GET':
		termopt = Termopt.objects.get(id=pk)
		conceitos_list_query_all = Conceito.objects.filter(termoref=pk).order_by('-linguax')
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
		solicitacoes_list_all = Solicitacao.objects.filter(termoref=pk).order_by('-linguax')
		# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
		paginator_solicitacoes = Paginator(solicitacoes_list_all, TAMANHO_PAGINA)
		page = request.GET.get('page')
		try:
			solicitacoes_list_query = paginator_solicitacoes.page(page)
		except PageNotAnInteger: 
			solicitacoes_list_query = paginator_solicitacoes.page(1) # pagina não é inteiro, apresenta a primeira
		except EmptyPage: 
			solicitacoes_list_query = paginator_solicitacoes.page(paginator_solicitacoes.num_pages) # pagina fora do range, apresenta ultima
		#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
		context = {'solicitacoes_list_query': solicitacoes_list_query, 'termopt': termopt, 'conceitos_list_query':conceitos_list_query,
				 'paginator_solicitacoes': paginator_solicitacoes, 'paginator_conceitos':paginator_conceitos}
		return render(request, 'maistermos/termopt/detalhe_termopt.html', context)	

# EDICÃO DE TERMOS EM PORTUGUÊS:
MENSAGEM_SUCESSO_EDICAO_TERMOPT = 'O termo en português foi editado com sucesso'
@login_required
def edita_termopt(request, pk):
	termopt = Termopt.objects.get(id=pk)
	if request.user.has_perm("maistermos.change_termopt") and termopt.usuario_insere_termopt.username == request.user.username:
		if request.method=='GET':
			termopt_form = TermoptForm(instance=termopt)
			context = {'termopt_form': termopt_form, 'termopt':termopt}
			return render(request, 'maistermos/termopt/cadastra_termopt.html', context)
		else:
			termopt_form = TermoptForm(request.POST, instance=termopt)
			if termopt_form.is_valid():
				termo = termopt_form.save()
				messages.success(request, MENSAGEM_SUCESSO_EDICAO_TERMOPT)
				return HttpResponseRedirect('/maistermos/termopt/lista/')
			else:	
				messages.error(request, MENSAGEM_ERRO_FORMULARIO)
				return HttpResponseRedirect("/maistermos/termopt/edita/%s" % pk)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect('/maistermos/termopt/lista/')

# REMOÇÃO DE TERMOS EM PORTUGUÊS:
MENSAGEM_SUCESSO_REMOCAO_TERMOPT = 'O termo foi removido com sucesso'
MENSAGEM_ERRO_REMOCAO_TERMOPT = 'Não foi possível remover o termo'
@login_required
def remove_termopt(request, pk):
	termopt = Termopt.objects.get(id=pk)
	if request.user.has_perm("maistermos.delete_termopt") and termopt.usuario_insere_termopt.username == request.user.username:
		try:
			termopt.delete()
			messages.success(request, MENSAGEM_SUCESSO_REMOCAO_TERMOPT)
		except:
			messages.error(request, MENSAGEM_ERRO_REMOCAO_TERMOPT)
		return HttpResponseRedirect('/maistermos/termopt/lista/')
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect('/maistermos/termopt/lista/')
#___________________________________________________________________________________________

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA CONCEITOS ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE CONCEITOS:
MENSAGEM_SUCESSO_CADASTRO_CONCEITO = 'O conceito foi cadastrado com sucesso'
@login_required
def cadastra_conceito(request, pk):
	if request.user.has_perm("maistermos.add_conceito"):
		termopt = Termopt.objects.get(id=pk)
		if request.method=='GET':
			conceito_form = ConceitoForm()
			context = {'conceito_form': conceito_form, 'termopt': termopt}
			return render(request, 'maistermos/conceito/cadastra_conceito.html', context)
		else:
			conceito_form = ConceitoForm(request.POST)
			if conceito_form.is_valid():
				conceito = conceito_form.save(commit=False)
				conceito.termoref = termopt
				conceito.data_insercao = timezone.now()
				conceito.usuario_insere_conceito = request.user
				conceito.save()
				messages.success(request, MENSAGEM_SUCESSO_CADASTRO_CONCEITO)
				return HttpResponseRedirect("/maistermos/termopt/detalhe/%s" % pk)
			else:
				messages.error(request, MENSAGEM_ERRO_FORMULARIO)
				return HttpResponseRedirect('/maistermos/conceito/cadastra/%s' % pk)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect("/maistermos/termopt/detalhe/%s" % pk)

# DETALHES DE CONCEITOS:
@login_required
def detalhe_conceito(request, pk):
	if request.method=='GET':
		conceito = Conceito.objects.get(id=pk)
		context = {'conceito': conceito}
		return render(request, 'maistermos/conceito/detalhe_conceito.html', context)	

# EDICÃO DE CONCEITOS:
MENSAGEM_SUCESSO_EDICAO_CONCEITO = 'O conceito foi editado com sucesso'
@login_required
def edita_conceito(request, pk):
	conceito = Conceito.objects.get(id=pk)
	if request.user.has_perm("maistermos.change_conceito") and conceito.usuario_insere_conceito.username == request.user.username:
		termopt = conceito.termoref
		if request.method=='GET':
			conceito_form = ConceitoForm(instance=conceito)

			context = {'conceito_form': conceito_form, 'conceito':conceito, 'termopt':termopt}
			return render(request, 'maistermos/conceito/cadastra_conceito.html', context)
		else:
			conceito_form = ConceitoForm(request.POST, instance=conceito)
			if conceito_form.is_valid():
				termo = conceito_form.save()
				messages.success(request, MENSAGEM_SUCESSO_EDICAO_CONCEITO)
				return HttpResponseRedirect("/maistermos/conceito/detalhe/%s" %pk)
			else:	
				messages.error(request, MENSAGEM_ERRO_FORMULARIO)
				return HttpResponseRedirect("/maistermos/conceito/edita/%s" %pk)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect("/maistermos/conceito/detalhe/%s" %pk)

# REMOÇÃO DE CONCEITOS:
MENSAGEM_SUCESSO_REMOCAO_CONCEITO = 'O conceito foi removido com sucesso'
MENSAGEM_ERRO_REMOCAO_CONCEITO = 'Não foi possível remover o conceito'
@login_required
def remove_conceito(request, pk):
	conceito = Conceito.objects.get(id=pk)
	if request.user.has_perm("maistermos.change_conceito") and conceito.usuario_insere_conceito.username == request.user.username:
		try:
			conceito.delete()
			messages.success(request, MENSAGEM_SUCESSO_REMOCAO_CONCEITO)
			return HttpResponseRedirect("/maistermos/termopt/detalhe/%s" % conceito.termoref.id)
		except:
			messages.error(request, MENSAGEM_ERRO_REMOCAO_CONCEITO)
			return HttpResponseRedirect("/maistermos/termopt/detalhe/%s" % conceito.termoref.id)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect("/maistermos/termopt/detalhe/%s" % conceito.termoref.id)

# APROVO CONCEITO:
MENSAGEM_SUCESSO_APROVACAO_CONCEITO = 'Agora é público que você esta aprova este conceito'
MENSAGEM_ERRO_APROVACAO_CONCEITO = 'Não é possível tornar público o fato de você aprova este conceito'
def aprova_conceito(request, pk):
	conceito = Conceito.objects.get(id=pk)
	try:
		conceito.usuario_aprova_conceito.add(request.user)
		messages.success(request, MENSAGEM_SUCESSO_INICIO_ANALISE_SOLICITACAO)
	except:
		messages.error(request, MENSAGEM_ERRO_INICIO_ANALISE_SOLICITACAO)
	return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % pk)

# REJEITO CONCEITO:
MENSAGEM_SUCESSO_APROVACAO_CONCEITO = 'Agora é público que você esta aprova este conceito'
MENSAGEM_ERRO_APROVACAO_CONCEITO = 'Não é possível tornar público o fato de você aprova este conceito'
def rejeita_conceito(request, pk):
	conceito = Conceito.objects.get(id=pk)
	try:
		conceito.usuario_aprova_conceito.add(request.user)
		messages.success(request, MENSAGEM_SUCESSO_INICIO_ANALISE_SOLICITACAO)
	except:
		messages.error(request, MENSAGEM_ERRO_INICIO_ANALISE_SOLICITACAO)
	return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % pk)
#___________________________________________________________________________________________

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA SOLICITACAO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE SOLICITACAO:
MENSAGEM_AJUDA_CADASTRO_SOLICITACAO = 'Busque o termo em português que deseja solicitar na lingua nacional'
MENSAGEM_ERRO_TERMOPT_NAO_EXISTE = "Não é possível solicitar a criação de um novo termo nas linguas nacionais sem existir um termo de referência na lingua portuguesa."
@login_required
def cria_solicitacao(request):
	if request.method=='GET':
		messages.info(request,MENSAGEM_AJUDA_CADASTRO_SOLICITACAO)
		context = {}
		return render(request, 'maistermos/solicitacao/cria_solicitacao.html', context)
	else:
		query_string = request.POST['q_termopt']
		termopt_list = Termopt.objects.filter(termo=query_string)
		count_termospt = termopt_list.count()
		if count_termospt == 0:
			messages.error(request,MENSAGEM_ERRO_TERMOPT_NAO_EXISTE)
			context = {'termopt_list':termopt_list}
		else:
			for termopt_busca in termopt_list:
				solicitacoes_list_all = Solicitacao.objects.filter(termoref=termopt_busca.id).order_by('-linguax')
				termopt = termopt_busca
			# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
			paginator_solicitacoes = Paginator(solicitacoes_list_all, TAMANHO_PAGINA)
			page = request.GET.get('page')
			try:
				solicitacoes_list_query = paginator_solicitacoes.page(page)
			except PageNotAnInteger: 
				solicitacoes_list_query = paginator_solicitacoes.page(1) # pagina não é inteiro, apresenta a primeira
			except EmptyPage: 
				solicitacoes_list_query = paginator_solicitacoes.page(paginator_solicitacoes.num_pages) # pagina fora do range, apresenta ultima
			#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
			context = {'termopt_list':termopt_list, 'solicitacoes_list_query':solicitacoes_list_query,
						'paginator_solicitacoes':paginator_solicitacoes, 'termopt':termopt}
		return render(request, 'maistermos/solicitacao/cria_solicitacao.html', context)

# CADASTRO DE SOLICITACAO:
MENSAGEM_SUCESSO_CADASTRO_SOLICITACAO = 'A solicitação foi cadastrada com sucesso'
MENSAGEM_ERRO_FORMULARIO_SOLICITACAO = 'A solicitação dave especificar a lingua em que será criado o novo termo'
@login_required
def cadastra_solicitacao(request, pk):
	termopt = Termopt.objects.get(id=pk)
	if request.method=='GET': 
		sugestao_form = SugestaoForm()
		solicitacao_form = SolicitacaoForm()
		context = {'sugestao_form': sugestao_form, 'solicitacao_form': solicitacao_form,
					'termopt':termopt}
		return render(request, 'maistermos/solicitacao/cadastra_solicitacao.html', context)
	else:
		sugestao_form = SugestaoForm(request.POST)
		solicitacao_form = SolicitacaoForm(request.POST)
		if solicitacao_form.is_valid():
			solicitacao = solicitacao_form.save(commit=False)
			solicitacao_busca_list = Solicitacao.objects.filter(termoref=pk, linguax=solicitacao.linguax)
			cont_busca = solicitacao_busca_list.count()
			if cont_busca != 0:
				for solicitacao_busca in solicitacao_busca_list:
					solicitacao = Solicitacao.objects.get(id=solicitacao_busca.id)
			else:
				solicitacao.termoref = termopt
				solicitacao.data_insercao = timezone.now()
				solicitacao.estado = 'Nao Atendida'
				solicitacao.save()
			solicitacao.usuario_solicitantes.add(request.user)
			if sugestao_form.is_valid(): 
				sugestao = sugestao_form.save(commit=False)
				sugestao.solicitacao = solicitacao
				sugestao.data_insercao = timezone.now()
				sugestao.usuario_insere_sugestao = request.user
				sugestao.save()
			messages.success(request, MENSAGEM_SUCESSO_CADASTRO_SOLICITACAO)
			return HttpResponseRedirect("/maistermos/solicitacao/lista/")
		else:
			messages.error(request, MENSAGEM_ERRO_FORMULARIO_SOLICITACAO)
			return HttpResponseRedirect("/maistermos/solicitacao/cadastra/%s" % pk)

# LISTA DE SOLICITAÇÕES:
MENSAGEM_ERRO_BUSCA = 'Não existem termos que cumpram as condições'
DROPDOWNLIST_OPCAO_LISTA_SOLICITACAO = (
	"Todas as solicitacoes",
	"Minhas solicitacoes",)
@login_required
def lista_solicitacao(request):
	solicitacoes_list_all = Solicitacao.objects.all()
	if request.method=='GET':
		titulo_lista = 'TODAS AS SOLICITAÇÕES CADASTRADAS'
	else:
		filtro_busca = request.POST["filtro_busca"]
		query_string = request.POST['q']
		query_string_count = len(query_string)
		termopt_list = Termopt.objects.filter(termo=query_string)
		termopt_count = termopt_list.count()
		if termopt_count == 0:
			if query_string_count != 0:
				messages.info(request, 'O termo em português não existe')
			if filtro_busca == "Todas as solicitacoes":
				titulo_lista = 'TODOS AS SOLICITAÇÕES CADASTRADAS'
			else:
				solicitacoes_list_all = Solicitacao.objects.filter(usuario_solicitantes=request.user)
				titulo_lista = 'MINHAS SOLICITAÇÕES'
		else:
			if filtro_busca == "Todas as solicitacoes":
				for termopt in termopt_list:
					solicitacoes_list_all = Solicitacao.objects.filter(termoref=termopt.id)
					titulo_lista = 'TODOS OS TERMOS CADASTRADOS'
			else:
				for termopt in termopt_list:
					solicitacoes_list_all = Solicitacao.objects.filter(termoref=termopt.id, usuario_solicitantes=request.user)
					titulo_lista = 'MINHAS SOLICITAÇÕES'
			count_termospt_list_query = solicitacoes_list_all.count()
			if count_termospt_list_query == 0:
				messages.info(request, MENSAGEM_ERRO_BUSCA)
	# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	paginator = Paginator(solicitacoes_list_all, TAMANHO_PAGINA)
	page = request.GET.get('page')
	try:
		solicitacao_list = paginator.page(page)
	except PageNotAnInteger: 
		solicitacao_list = paginator.page(1) # pagina não é inteiro, apresenta a primeira
	except EmptyPage: 
		solicitacao_list = paginator.page(paginator.num_pages) # pagina fora do range, apresenta ultima
	#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	context = {'solicitacao_list': solicitacao_list, 'traducao_opcao_list': DROPDOWNLIST_OPCAO_LISTA_SOLICITACAO,
				'titulo_lista': titulo_lista, 'paginator': paginator}
	return render(request, 'maistermos/solicitacao/lista_solicitacao.html', context)	

# DETALHES DE SOLICITAÇÃO:
@login_required
def detalhe_solicitacao(request, pk):
	if request.method=='GET':
		solicitacao = Solicitacao.objects.get(id=pk)
		sugestao_list_query_all = Sugestao.objects.filter(solicitacao=solicitacao).order_by('-data_insercao')
		# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
		paginator = Paginator(sugestao_list_query_all, TAMANHO_PAGINA)
		page = request.GET.get('page')
		try:
			sugestao_list_query = paginator.page(page)
		except PageNotAnInteger: 
			sugestao_list_query = paginator.page(1) # pagina não é inteiro, apresenta a primeira
		except EmptyPage: 
			sugestao_list_query = paginator.page(paginator.num_pages) # pagina fora do range, apresenta ultima
		#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
		context = {'sugestao_list_query': sugestao_list_query,
					'solicitacao': solicitacao, 'paginator': paginator}
		return render(request, 'maistermos/solicitacao/detalhe_solicitacao.html', context)	

# REMOÇÃO DE SOLICITAÇÕES:
MENSAGEM_SUCESSO_REMOCAO_SOLICITACAO = 'a solicitação foi removida com sucesso'
MENSAGEM_ERRO_REMOCAO_SOLICITACAO = 'Não foi possível remover a solicitação'
@login_required
def remove_solicitacao(request, pk):
	solicitacao = Solicitacao.objects.get(id=pk)
	try:
		solicitacao.delete()
		messages.success(request, MENSAGEM_SUCESSO_REMOCAO_TERMO)
	except:
		messages.error(request, MENSAGEM_ERRO_REMOCAO_TERMO)
	return HttpResponseRedirect('/maistermos/solicitacao/lista/')

# INICIO NÁLISE SOLICITAÇÃO:
MENSAGEM_SUCESSO_INICIO_ANALISE_SOLICITACAO = 'Agora é público que você esta analisando esta solicitação'
MENSAGEM_ERRO_INICIO_ANALISE_SOLICITACAO = 'Não é possível tornar público o fato de você estar analisando'
def inicio_analise_solicitacao(request, pk):
	solicitacao = Solicitacao.objects.get(id=pk)
	try:
		solicitacao.usuario_em_analise.add(request.user)
		solicitacao.estado = 'Em criacao'
		solicitacao.save()
		messages.success(request, MENSAGEM_SUCESSO_INICIO_ANALISE_SOLICITACAO)
	except:
		messages.error(request, MENSAGEM_ERRO_INICIO_ANALISE_SOLICITACAO)
	return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % pk)
#___________________________________________________________________________________________

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA SUGESTÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE SUGESTAO:
MENSAGEM_SUCESSO_CADASTRO_SUGESTAO = 'A sugestão foi cadastrado com sucesso'
@login_required
def cadastra_sugestao(request, pk):
	solicitacao = Solicitacao.objects.get(id=pk)
	if request.method=='GET':
		sugestao_form = SugestaoForm()
		context = {'sugestao_form': sugestao_form, 'solicitacao': solicitacao}
		return render(request, 'maistermos/sugestao/cadastra_sugestao.html', context)
	else:
		sugestao_form = SugestaoForm(request.POST)
		if sugestao_form.is_valid():
			sugestao = sugestao_form.save(commit=False)
			sugestao.solicitacao = solicitacao
			sugestao.usuario_insere_sugestao = request.user
			sugestao.save()
			messages.success(request, MENSAGEM_SUCESSO_CADASTRO_SUGESTAO)
			return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % pk)
		else:
			messages.error(request, MENSAGEM_ERRO_FORMULARIO)
			return HttpResponseRedirect("/maistermos/sugestao/cadastra/%s" % pk)

# DETALHES DE SUGESTAO:
@login_required
def detalhe_sugestao(request, pk):
	if request.method=='GET':
		sugestao = Sugestao.objects.get(id=pk)
		context = {'sugestao': sugestao}
		return render(request, 'maistermos/sugestao/detalhe_sugestao.html', context)	

# EDICÃO DE SUGESTAO:
MENSAGEM_SUCESSO_EDICAO_SUGESTAO = 'A sugestão foi editada com sucesso'
@login_required
def edita_sugestao(request, pk):
	sugestao = Sugestao.objects.get(id=pk)
	if request.user.has_perm("maistermos.delete_sugestao") and sugestao.usuario_insere_sugestao.username == request.user.username:
		solicitacao = sugestao.solicitacao
		if request.method=='GET':
			sugestao_form = SugestaoForm(instance=sugestao)
			context = {'sugestao_form': sugestao_form, 'sugestao':sugestao, 'solicitacao':solicitacao}
			return render(request, 'maistermos/sugestao/cadastra_sugestao.html', context)
		else:
			sugestao_form = SugestaoForm(request.POST, instance=sugestao)
			if sugestao_form.is_valid():
				sugestao = sugestao_form.save()
				messages.success(request, MENSAGEM_SUCESSO_EDICAO_SUGESTAO)
				return HttpResponseRedirect("/maistermos/sugestao/detalhe/%s" %pk)
			else:	
				messages.error(request, MENSAGEM_ERRO_FORMULARIO)
				return HttpResponseRedirect("/maistermos/sugestao/edita/%s" %pk)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect("/maistermos/sugestao/detalhe/%s" %pk)

# REMOÇÃO DE SUGESTAO:
MENSAGEM_SUCESSO_REMOCAO_SUGESTAO = 'A sugestão foi removido com sucesso'
MENSAGEM_ERRO_REMOCAO_SUGESTAO = 'Não foi possível remover o conceito'
@login_required
def remove_sugestao(request, pk):
	sugestao = Sugestao.objects.get(id=pk)
	if request.user.has_perm("maistermos.delete_sugestao") and sugestao.usuario_insere_sugestao.username == request.user.username:
		try:
			sugestao.delete()
			messages.success(request, MENSAGEM_SUCESSO_REMOCAO_SUGESTAO)
			return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % sugestao.solicitacao.id)
		except:
			messages.error(request, MENSAGEM_ERRO_REMOCAO_SUGESTAO)
			return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % sugestao.solicitacao.id)
	else:
		messages.error(request, MENSAGEM_SEM_PERMISSAO)
		return HttpResponseRedirect("/maistermos/solicitacao/detalhe/%s" % sugestao.solicitacao.id)
#___________________________________________________________________________________________

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA TERMOS NAS LINGUAS NACIONAIS ANGOLANAS ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE TERMOS NAS LINGUAS NACIONAIS:
MENSAGEM_SUCESSO_CADASTRO_TERMOLX = 'O termo na lingua nacional foi cadastrado com sucesso'
MENSAGEM_ERRO_TERMO_EXISTE_CADASTRO_TERMOLX = 'O termo na lingua nacional já existe'
@login_required
def cadastra_termolx(request, pk):
	solicitacao = Solicitacao.objects.get(id=pk)
	if request.method=='GET':
		termolx_form = TermolxForm()

		sugestao_list_query_all = Sugestao.objects.filter(solicitacao=solicitacao).order_by('-data_insercao')
		# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
		paginator_sugestao = Paginator(sugestao_list_query_all, TAMANHO_PAGINA)
		page = request.GET.get('page')
		try:
			sugestao_list_query = paginator_sugestao.page(page)
		except PageNotAnInteger: 
			sugestao_list_query = paginator_sugestao.page(1) # pagina não é inteiro, apresenta a primeira
		except EmptyPage: 
			sugestao_list_query = paginator_sugestao.page(paginator_sugestao.num_pages) # pagina fora do range, apresenta ultima
		#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

		conceitos_list_query_all = Conceito.objects.filter(termoref=solicitacao.termoref).order_by('-linguax')
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

		context = {'termolx_form': termolx_form, 'solicitacao':solicitacao, 'paginator_sugestao': paginator_sugestao,
					'sugestao_list_query': sugestao_list_query, 'conceitos_list_query': conceitos_list_query,
					'paginator_conceitos': paginator_conceitos}
		return render(request, 'maistermos/termolx/cadastra_termolx.html', context)
	else:
		termolx_form = TermolxForm(request.POST)
		if termolx_form.is_valid():
			termo = termolx_form.save(commit=False)
			cont_termopt = Termolx.objects.filter(termo=termo.termo).count()
			if cont_termopt == 0:
				solicitacao.estado = 'Atendida'
				solicitacao.usuario_atendente = request.user
				solicitacao.data_fim_atendimento = timezone.now()
				solicitacao.save()
				termo.solicitacao = solicitacao
				termo.termoref = solicitacao.termoref
				termo.linguax = solicitacao.linguax
				termo.data_insercao = timezone.now()
				termo.usuario_insere_termolx = request.user
				termo.estado = 'Proposto'
				termo.save()
				messages.success(request, MENSAGEM_SUCESSO_CADASTRO_TERMOLX)
				return HttpResponseRedirect('/maistermos/termolx/lista/')
			else:
				messages.info(request, MENSAGEM_ERRO_TERMO_EXISTE_CADASTRO_TERMOLX)
				return HttpResponseRedirect("/maistermos/termolx/cadastra/%s" % pk)
		messages.error(request, MENSAGEM_ERRO_FORMULARIO)
		return HttpResponseRedirect("/maistermos/termolx/cadastra/%s" % pk)


# LISTA DE TERMOS NAS LINGUAS NACIONAIS: 
DROPDOWNLIST_OPCAO_LISTA_TERMO_LINGUAS = (
	"Todas as linguas",
	"Kikongo","Kibundo","Espanhol")
@login_required
def lista_termolx(request):
	if request.method=='GET':
		termoslx_list_all = Termolx.objects.all()
		titulo_lista = 'TERMOS CADASTRADOS'
	else:
		filtro_busca = request.POST["filtro_opcao"]
		traducao_busca = request.POST["traducao_opcao"]
		query_string = request.POST['q']
		if filtro_busca == "Todos os termos":
			titulo_lista = 'TODOS OS TERMOS CADASTRADOS'
			if traducao_busca == "Todas as linguas":
				termoslx_list_all = Termolx.objects.filter(termo__contains=query_string)
			else:
				termoslx_list_all = Termolx.objects.filter(termo__contains=query_string, linguax=traducao_busca)
		else:
			titulo_lista = 'MEUS TERMOS CADASTRADOS'
			if traducao_busca == "Todas as linguas":
				termoslx_list_all = Termolx.objects.filter(termo__contains=query_string, usuario_insere_termopt=request.user)
			else:
				termoslx_list_all = Termolx.objects.filter(termo__contains=query_string, linguax=traducao_busca, usuario_insere_termopt=request.user)	
		count_termospt_list_query = termoslx_list_all.count()
		if count_termospt_list_query == 0:
			messages.info(request, MENSAGEM_ERRO_BUSCA)
	# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	paginator = Paginator(termoslx_list_all, TAMANHO_PAGINA)
	page = request.GET.get('page')
	try:
		termoslx_list = paginator.page(page)
	except PageNotAnInteger: 
		termoslx_list = paginator.page(1) # pagina não é inteiro, apresenta a primeira
	except EmptyPage: 
		termoslx_list = paginator.page(paginator.num_pages) # pagina fora do range, apresenta ultima
	#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	context = {'termoslx_list': termoslx_list, 'filtro_opcao_list': DROPDOWNLIST_OPCAO_LISTA_TERMO,
				'titulo_lista': titulo_lista, 'paginator': paginator, 'traducao_opcao_list':DROPDOWNLIST_OPCAO_LISTA_TERMO_LINGUAS}
	return render(request, 'maistermos/termolx/lista_termolx.html', context)

# DETALHES DE TERMOS NAS LINGUAS NACIONAIS:
@login_required
def detalhe_termolx(request, pk):
	if request.method=='GET':
		certificado_form = CertificadoForm()
		termolx = Termolx.objects.get(id=pk)
		solicitacao = Solicitacao.objects.get(id=termolx.solicitacao.id)
		context = {'termolx': termolx, 'solicitacao': solicitacao, 'certificado_form':certificado_form}
		return render(request, 'maistermos/termolx/detalhe_termolx.html', context)	

# EDICÃO DE TERMOS NAS LINGUAS NACIONAIS:
MENSAGEM_SUCESSO_EDICAO_TERMOLX = 'O termo na lingua nacional foi editado com sucesso'
@login_required
def edita_termolx(request, pk):
	termolx = Termolx.objects.get(id=pk)
	if request.method=='GET':
		termolx_form = TermolxForm(instance=termolx)
		context = {'termolx_form': termolx_form, 'termolx':termolx}
		return render(request, 'maistermos/termolx/cadastra_termolx.html', context)
	else:
		termolx_form = TermolxForm(request.POST, instance=termolx)
		if termolx_form.is_valid():
			termo = termolx_form.save()
			messages.success(request, MENSAGEM_SUCESSO_EDICAO_TERMOLX)
			return HttpResponseRedirect('/maistermos/termolx/lista/')
		else:	
			messages.info(request, MENSAGEM_ERRO_FORMULARIO)
			return HttpResponseRedirect("/maistermos/termolx/edita/%s" % pk)
############################################################################################

# VIEW PARA EDICÃO DE TERMOS EM PORTUGUÊS:
############################################################################################
MENSAGEM_SUCESSO_REMOCAO_TERMOLX = 'O termo na lingua nacional foi removido com sucesso'
@login_required
def remove_termolx(request, pk):
	termolx = Termolx.objects.get(id=pk)
	try:
		termolx.delete()
		messages.info(request, MENSAGEM_SUCESSO_REMOCAO_TERMOLX)
	except:
		messages.info(request, MENSAGEM_ERRO_REMOCAO_TERMO)
	return HttpResponseRedirect('/maistermos/termolx/lista/')
############################################################################################

#___________________________________________________________________________________________


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ REGIÃO PARA CERTIFICADOS ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# CADASTRO DE TERMOS NAS LINGUAS NACIONAIS:
@login_required
def certificar_termo(request, pk):
	termolx = Termolx.objects.get(id=pk)
	if request.method=='GET':
		"""certificado_form = CertificadoForm()
		termolx = Termolx.objects.get(id=pk)
		
		context = {'certificado_form': certificado_form, 'termolx':termolx }
		return render(request, 'maistermos/certificado/cadastra_certificado.html', context)"""
	else:
		certificado_form = CertificadoForm(request.POST)
		if certificado_form.is_valid():
			certificado = certificado_form.save(commit=False)
			certificado.termolx = termolx
			certificado.usuario_insere_certificado = request.user
			certificado.data_insercao = timezone.now()
			certificado.save()
			termolx.estado = 'Certificado'
			termolx.save()
			messages.success(request, 'Termo certificado com sucesso')
			return HttpResponseRedirect("/maistermos/termolx/detalhe/%s" % pk)

@login_required
def negar_certificado(request, pk):
	termolx = Termolx.objects.get(id=pk)
	if request.method=='GET':
		"""termoslx_list_all = Termolx.objects.all()
		titulo_lista = 'TERMOS CADASTRADOS'"""
	else:
		termolx.estado = 'Nao certificado'
		termolx.nao_certificado = request.POST.get("justificativa_nao_certificado", False)
		termolx.save()
		solicitacao = termolx.solicitacao
		solicitacao.estado = 'Nao Atendida'
		solicitacao.save()
		messages.success(request, 'Não certificação justificada com sucesso')
		return HttpResponseRedirect("/maistermos/termolx/detalhe/%s" % pk)


# LISTA DE TERMOS NAS LINGUAS NACIONAIS: 
DROPDOWNLIST_OPCAO_FILTRO_CERTIFICADO = (
	"Todas as certificacoes",
	"Minhas certificacoes")
@login_required
def lista_certificado(request):
	certificados_list_all = Certificado.objects.all()
	if request.method=='GET':
		titulo_lista = 'TODAS AS CERTIFICAÇÕES'
	else:
		filtro_busca = request.POST["filtro_busca"]
		query_string = request.POST['q']
		query_string_count = len(query_string)
		termolx_list = Termopt.objects.filter(termo=query_string)
		termolx_count = termolx_list.count()
		if termolx_count == 0:
			if query_string_count != 0:
				messages.info(request, 'O termo em português não existe')
			if filtro_busca == "Todas as certificacoes":
				titulo_lista = 'TODOS AS CERTIFICAÇÕES'
			else:
				certificados_list_all = Certificado.objects.filter(usuario_insere_certificado=request.user)
				titulo_lista = 'MINHAS CERTIFICAÇÕES'
		else:
			if filtro_busca == "Todas as solicitacoes":
				for termolx in termolx_list:
					certificados_list_all = Certificado.objects.filter(termolx=termolx.id)
					titulo_lista = 'TODOS OS TERMOS CADASTRADOS'
			else:
				for termolx in termolx_list:
					certificados_list_all = Certificado.objects.filter(termolx=termolx.id, usuario_insere_certificado=request.user)
					titulo_lista = 'MINHAS SOLICITAÇÕES'
			count_termospt_list_query = certificados_list_all.count()
			if count_termospt_list_query == 0:
				messages.info(request, MENSAGEM_ERRO_BUSCA)
	# PAGINAÇÃO ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	paginator = Paginator(certificados_list_all, TAMANHO_PAGINA)
	page = request.GET.get('page')
	try:
		certificados_list = paginator.page(page)
	except PageNotAnInteger: 
		certificados_list = paginator.page(1) # pagina não é inteiro, apresenta a primeira
	except EmptyPage: 
		certificados_list = paginator.page(paginator.num_pages) # pagina fora do range, apresenta ultima
	#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
	context = {'certificados_list_all':certificados_list_all,'certificados_list': certificados_list, 'traducao_opcao_list': DROPDOWNLIST_OPCAO_FILTRO_CERTIFICADO,
				'titulo_lista': titulo_lista, 'paginator': paginator}
	return render(request, 'maistermos/certificado/lista_certificado.html', context)		

# DETALHES DE TERMOS NAS LINGUAS NACIONAIS:
@login_required
def detalhe_certificado(request, pk):
	if request.method=='GET':
		certificado = Certificado.objects.get(id=pk)
		context = {'certificado': certificado}
		return render(request, 'maistermos/certificado/detalhe_certificado.html', context)	

# EDICÃO DE TERMOS NAS LINGUAS NACIONAIS:
MENSAGEM_SUCESSO_EDICAO_TERMOLX = 'O termo na lingua nacional foi editado com sucesso'
@login_required
def edita_certificado(request, pk):
	termolx = Termolx.objects.get(id=pk)
	if request.method=='GET':
		termolx_form = TermolxForm(instance=termolx)
		context = {'termolx_form': termolx_form, 'termolx':termolx}
		return render(request, 'maistermos/termolx/cadastra_termolx.html', context)
	else:
		termolx_form = TermolxForm(request.POST, instance=termolx)
		if termolx_form.is_valid():
			termo = termolx_form.save()
			messages.success(request, MENSAGEM_SUCESSO_EDICAO_TERMOLX)
			return HttpResponseRedirect('/maistermos/termolx/lista/')
		else:	
			messages.info(request, MENSAGEM_ERRO_FORMULARIO)
			return HttpResponseRedirect("/maistermos/termolx/edita/%s" % pk)
