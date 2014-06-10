from django.contrib import admin
from maistermos.models import Termopt, Termolx, Conceito, Solicitacao, Sugestao, Certificado

# Registrar os Models no Admin.

class TermoptAdmin(admin.ModelAdmin):
    fields = ['termo', 'conceito']

admin.site.register(Termopt, TermoptAdmin)

admin.site.register(Termolx)

admin.site.register(Conceito)

