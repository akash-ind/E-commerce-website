from django import template

register=template.Library()

@register.simple_tag
def mult(no, no2):
	return float(no)*float(no2)