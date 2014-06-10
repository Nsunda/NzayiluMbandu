#coding: utf8 
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from maistermos import views

urlpatterns = patterns('',

    url(r'^$', views.mais_termos, name='mais_termos'),
    

    url(r'^termopt/cadastra/$', views.cadastra_termopt, name='cadastra_termopt'),
    url(r'^termopt/lista/$', views.lista_termopt, name='lista_termopt'),
    url(r'^termopt/detalhe/(?P<pk>\d+)$', views.detalhe_termopt, name='detalhe_termopt'),
    url(r'^termopt/edita/(?P<pk>\d+)$', views.edita_termopt, name='edita_termopt'),
    url(r'^termopt/remove/(?P<pk>\d+)$', views.remove_termopt, name='remove_termopt'),

    url(r'^conceito/cadastra/(?P<pk>\d+)$', views.cadastra_conceito, name='cadastra_conceito'),
    url(r'^conceito/detalhe/(?P<pk>\d+)$', views.detalhe_conceito, name='detalhe_conceito'),
    url(r'^conceito/edita/(?P<pk>\d+)$', views.edita_conceito, name='edita_conceito'),
    url(r'^conceito/remove/(?P<pk>\d+)$', views.remove_conceito, name='remove_conceito'),
    url(r'^conceito/aprova/(?P<pk>\d+)$', views.aprova_conceito, name='aprova_conceito'),
    url(r'^conceito/rejeita/(?P<pk>\d+)$', views.rejeita_conceito, name='rejeita_conceito'),
	
	url(r'^solicitacao/cria/$', views.cria_solicitacao, name='cria_solicitacao'),
    url(r'^solicitacao/cadastra/(?P<pk>\d+)$', views.cadastra_solicitacao, name='cadastra_solicitacao'),
    url(r'^solicitacao/lista/$', views.lista_solicitacao, name='lista_solicitacao'),
    url(r'^solicitacao/detalhe/(?P<pk>\d+)$', views.detalhe_solicitacao, name='detalhe_solicitacao'),
    url(r'^solicitacao/remove/(?P<pk>\d+)$', views.remove_solicitacao, name='remove_solicitacao'),
    url(r'^solicitacao/inicioanalise/(?P<pk>\d+)$', views.inicio_analise_solicitacao, name='inicio_analise_solicitacao'),


    url(r'^sugestao/cadastra/(?P<pk>\d+)$', views.cadastra_sugestao, name='cadastra_sugestao'),
    url(r'^sugestao/detalhe/(?P<pk>\d+)$', views.detalhe_sugestao, name='detalhe_sugestao'),
    url(r'^sugestao/edita/(?P<pk>\d+)$', views.edita_sugestao, name='edita_sugestao'),
    url(r'^sugestao/remove/(?P<pk>\d+)$', views.remove_sugestao, name='remove_sugestao'),

    url(r'^termolx/cadastra/(?P<pk>\d+)$', views.cadastra_termolx, name='cadastra_termolx'),
    url(r'^termolx/lista/$', views.lista_termolx, name='lista_termolx'),
    url(r'^termolx/detalhe/(?P<pk>\d+)$', views.detalhe_termolx, name='detalhe_termolx'),
    url(r'^termolx/edita/(?P<pk>\d+)$', views.edita_termolx, name='edita_termolx'),
    url(r'^termolx/remove/(?P<pk>\d+)$', views.remove_termolx, name='remove_termolx'),

    url(r'^certificado/certificar/(?P<pk>\d+)$', views.certificar_termo, name='certificar_termo'),
    url(r'^certificado/negar/(?P<pk>\d+)$', views.negar_certificado, name='negar_certificado'),
    url(r'^certificado/lista/$', views.lista_certificado, name='lista_certificado'),
    url(r'^certificado/detalhe/(?P<pk>\d+)$', views.detalhe_certificado, name='detalhe_certificado'),
    url(r'^certificado/edita/(?P<pk>\d+)$', views.edita_certificado, name='edita_certificado'),
)