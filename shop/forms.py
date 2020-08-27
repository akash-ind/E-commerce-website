from django.forms import ModelForm
from django import forms
from login.models import Address
from .models import CustomOrder

class CustomOrderForm(ModelForm):
	"""Will Display Form for CustomOrder"""
	class Meta:
		model=CustomOrder
		exclude=['user','delivered','cancel']
		widgets={
			'additional_info':forms.Textarea(attrs= {'rows':2})
		}
	def __init__(self,curr_user,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['address'].queryset= Address.objects.filter(user=curr_user)
		self.fields['address'].empty_label=None
