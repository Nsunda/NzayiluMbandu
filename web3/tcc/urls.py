from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from django.contrib.auth.views import login, logout

from tcc import views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', views.consulta_termo, name="default"),
    url(r'^ensino/$', TemplateView.as_view(template_name="../templates/ensino.html"), name="ensino"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^maistermos/', include('maistermos.urls')),
    url(r'^dicionario/', include('dicionario.urls')),

    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout, {'next_page': '/dicionario/'}),
)
