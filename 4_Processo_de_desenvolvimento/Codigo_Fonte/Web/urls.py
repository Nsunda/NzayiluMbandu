from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
url(r'^CriacaoTermo/', include('CriacaoTermo.urls')),
url(r'^admin/', include(admin.site.urls)),
	)