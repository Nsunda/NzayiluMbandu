from django.contrib import admin
from CriacaoTermo.models import Estado, Certificacao, Kik, Port


class KikInline(admin.TabularInline):
	model = Kik
	extra = 1
		

class PortAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				 {'fields': ['termopt']}),
		('Date information', {'fields': ['conceitopt', 'data_pubpt'], 'classes': ['collapse']}),
	]
	inlines = [KikInline]
	list_display = ('termopt', 'conceitopt', 'was_published_recently')
	list_filter = ['data_pubpt']
	search_fields = ['termopt']

admin.site.register(Port, PortAdmin)

class Certificacao(admin.TabularInline):
	model = Certificacao
	extra = 1

class KikAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				 {'fields': ['termokk']}),
		('Date information', {'fields': ['conceitokk', 'data_pubkk'], 'classes': ['collapse']}),
	]
	inlines = [Certificacao]
	list_display = ('termokk', 'conceitokk', 'was_published_recently')
	list_filter = ['data_pubkk']
	search_fields = ['termokk']

admin.site.register(Kik, KikAdmin)

class Estado(admin.TabularInline):
	model = Estado
	extra = 1

class CertificacaoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				 {'fields': ['certicado']}),
		('Date information', {'fields': ['observacao', 'data_cert'], 'classes': ['collapse']}),
	]
	inlines = [Estado]
	list_display = ('certicado', 'observacao', 'was_published_recently')
	list_filter = ['data_cert']
	search_fields = ['certicado']

admin.site.register(Certificacao, CertificacaoAdmin)