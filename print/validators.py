from django.core.exceptions import ValidationError

def validate_size(obj):
	size=obj.size
	if size>10485760 :
		raise ValidationError("The maximum size which can be uploaded is 10 MB")
	else:
		return obj