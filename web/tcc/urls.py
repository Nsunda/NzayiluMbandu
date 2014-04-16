from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'tcc.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name="../templates/default.html"), name="default"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^maistermos/', include('maistermos.urls')),
)