#coding: utf8 

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from dicionario import views

urlpatterns = patterns('',
    url(r'^$', views.consulta_termo, name='consultar_termo'),

    url(r'^conceito/aprova_adi/$', views.aprova_adi_conceito, name='aprova_adi_conceito'),
    url(r'^conceito/aprova_rem/$', views.aprova_rem_conceito, name='aprova_rem_conceito'),
    url(r'^conceito/rejeita_adi/$', views.rejeita_adi_conceito, name='rejeita_adi_conceito'),
    url(r'^conceito/rejeita_rem/$', views.rejeita_rem_conceito, name='rejeita_rem_conceito'),
	
	url(r'^sugestao/aprova_adi/$', views.aprova_adi_sugestao, name='aprova_adi_sugestao'),
    url(r'^sugestao/aprova_rem/$', views.aprova_rem_sugestao, name='aprova_rem_sugestao'),
    url(r'^sugestao/rejeita_adi/$', views.rejeita_adi_sugestao, name='rejeita_adi_sugestao'),
    url(r'^sugestao/rejeita_rem/$', views.rejeita_rem_sugestao, name='rejeita_rem_sugestao'),

    url(r'^solicitacao/nao_estudo/$', views.nao_estudo_solicitacao, name='nao_estudo_solicitacao'),
    url(r'^solicitacao/sim_estudo/$', views.sim_estudo_solicitacao, name='sim_estudo_solicitacao'),
    url(r'^solicitacao/get_estado_sol/$', views.get_estado_sol, name='get_estado_sol'),

    
)