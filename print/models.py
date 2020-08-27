from django.db import models
import os
from .validators import validate_size
from django.core.validators import MinValueValidator
from django.utils.deconstruct import deconstructible
from login.models import User
import uuid
# Create your models here.
@deconstructible
class path_and_rename:
	"""docstring for """
	def __init__(self, arg):
		self.sub_path=arg
	def __call__(self,instance,filename):
		self.sub_path=os.path.join(self.sub_path,instance.user.name+"_"+instance.user.phone_no,
			str(instance.user.printdoc_set.count()+1))
		ext=filename.split('.')[-1]
		filename="file"+"."+ext
		path=os.path.join(self.sub_path,filename)
		return path


class PrintDoc(models.Model):
	"""docstring for PrintDoc"""
	document_paper=(('p','Plain Paper'), 
		('e','Premium Glossy')
		)
	document_color=(('c','Colored'),
		('b','Black and White'))
	document=models.FileField(upload_to=path_and_rename("printing"),validators=[validate_size])
	doc_id=models.UUIDField(default=uuid.uuid4)
	name_of_file=models.CharField(max_length=500)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	copies=models.IntegerField(validators=[MinValueValidator(1)], default=1)
	color=models.CharField(max_length=2, choices=document_color, default='c')
	pages=models.IntegerField(validators=[MinValueValidator(1)])
	paper_type=models.CharField(max_length=2, choices=document_paper, default='p')
	price=models.DecimalField(max_digits=9,decimal_places=2)
	deleted=models.BooleanField(default=False)
	time=models.DateTimeField(blank=True, null=True)