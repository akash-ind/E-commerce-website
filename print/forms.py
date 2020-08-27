from django import forms
from .models import PrintDoc

two=(
	("True","True"),
	("False","False")
	)
class UploadDocument(forms.ModelForm):
	double_sided=forms.ChoiceField(choices=two, initial="False")
	some_other_info=forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2}))
	class Meta:
		model=PrintDoc
		exclude=['user','price','doc_id','deleted','time']
		help_texts = {
			'document': ('Size of file should not be more than 10 MB'),
			'name_of_file': ('Write any name. You need to tell the name when collecting document'),
		}