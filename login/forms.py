from .models import User,Address
from django import forms

class RegisterForm(forms.ModelForm):
	"""docstring for RegisterForm"""
	confirm_password=forms.CharField(max_length=32,widget=forms.PasswordInput())
	class Meta:
		"""docstring for Meta"""
		model=User
		widgets={
			'password':forms.PasswordInput()
		}
		fields= ['name', 'email', 'phone_no', 'password']

class AddressForm(forms.ModelForm):
	class Meta:
		model=Address
		exclude=['user']

class LoginForm(forms.Form):
	email=forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput())

class MailForm(forms.Form):
	code=forms.IntegerField()