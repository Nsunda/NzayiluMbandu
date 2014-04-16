#coding: utf8 

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from maistermos import views

urlpatterns = patterns('',
    url(r'^$', views.create_solicitacao, name='criar_solicitacao'),
    url(r'^solicitacao/$', views.SolicitacoesList.as_view(), name='lista_solicitacao'),
    url(r'^solicitacao/detalhe/(?P<pk>\d+)$', views.SolicitacaoDetail.as_view(), name='detalhe_solicitacao'),
    url(r'^solicitacao/edita/(?P<pk>\d+)$', views.edit_solicitacao, name='editar_solicitacao'),

    
    url(r'^solicitacao/remove/(?P<pk>\d+)$', views.SolicitacaoDelete.as_view(), name='apagar_solicitacao'),
    
    url(r'^termos/$', views.TermosList.as_view(), name='lista_termo'),
    url(r'^termos/criar/(?P<solicitacao_id>\d+)/$', views.TermoCreate.as_view(), name='criar_termo'),
    url(r'^termos/edita/(?P<pk>\d+)$', views.TermoUpdate.as_view(), name='editar_termo'),
    
    url(r'^certificacao/$', views.CertificacaoList.as_view(), name='lista_certificacao'),
    url(r'^certificacao/criar/$', views.CertificacaoCreate.as_view(), name='criar_certificacao'),
    url(r'^certificacao/edita/(?P<pk>\d+)$', views.CertificacaoUpdate.as_view(), name='editar_certificacao'),
)