from django.contrib import admin
from maistermos.models import Solicitacoes, Termos, Certificacao

# Registrar os Models no Admin.

class SolicitacaoAdmin(admin.ModelAdmin):
    fields = ['termopt', 'solicitante', 
    		'data_solicita', 'estado']

admin.site.register(Solicitacoes, SolicitacaoAdmin)

admin.site.register(Termos)

admin.site.register(Certificacao)

