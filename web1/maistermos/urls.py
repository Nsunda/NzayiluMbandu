#coding: utf8 
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from maistermos import views

urlpatterns = patterns('',

    url(r'^termopt/cadastra/$', views.cadastra_termopt, name='cadastra_termopt'),
    url(r'^termopt/lista/$', views.lista_termopt, name='lista_termopt'),
    url(r'^termopt/detalhe/(?P<pk>\d+)$', views.detalhe_termopt, name='detalhe_termopt'),


)