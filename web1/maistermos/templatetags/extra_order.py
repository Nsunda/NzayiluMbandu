from django import template
register = template.Library()

#Adicionar Css aos campos de um form
@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})