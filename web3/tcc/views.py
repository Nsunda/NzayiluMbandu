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

from dicionario.views import DROPDOWNLIST_OPCAO, TAMANHO_PAGINA

def consulta_termo(request):
	if request.method=='GET':
		context = {'traducao_opcao_list': DROPDOWNLIST_OPCAO}
		return render(request, '../templates/default.html', context)