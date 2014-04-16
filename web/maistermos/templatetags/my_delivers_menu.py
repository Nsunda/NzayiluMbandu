from django import template
from rh.models import Funcionario
register = template.Library()

@register.inclusion_tag('meus_entregadores_menu.html')
def my_delivers():
	funcionarios = Funcionario.objects.values()
	return {'funcionarios':funcionarios}

@register.inclusion_tag('meus_entregadores_local.html')
def my_delivers_local():
	funcionarios = Funcionario.objects.values()
	return {'funcionarios':funcionarios}