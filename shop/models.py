from django.db import models
import uuid
import os
from django.utils.deconstruct import deconstructible
from django.core.files import File
from io import BytesIO
from PIL import Image
from print.models import PrintDoc
from login.models import User, Address
from django.core.validators import MinValueValidator
 
@deconstructible 
class path_and_rename(object):
	def __init__(self,path):
		self.sub_path=path
	def __call__(self,instance,filename):
		ext=filename.split('.')[-1]
		category=instance.category.category_name
		name=f"{instance.name}.{ext}"
		path=os.path.join(self.sub_path,category,name)
		return path

class Product(models.Model):
	name=models.CharField(max_length=32)
	p_id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	category=models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
	prices=models.IntegerField()
	description=models.TextField(blank=True, null=True)
	product_image=models.ImageField(upload_to=path_and_rename(os.path.join('products','images')))
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		im=Image.open(self.product_image)
		im = im.convert('RGB')
		im=im.resize((680,500))
		io=BytesIO()
		im.save(io,"JPEG")
		self.product_image=File(io, name=self.product_image.name)
		super().save(*args, **kwargs)
	class Meta:
		ordering=['-prices']

@deconstructible
class category_path:
	"""docstring for category"""
	def __init__(self, path):
		self.sub_path=path
	def __call__(self,instance,filename):
		ext=filename.split('.')[-1]
		name=f"{instance.category_name}.{ext}"
		path=os.path.join(self.sub_path,name)
		return path

class ProductCategory(models.Model):
	category_name=models.CharField(max_length=50, unique=True)
	category_image=models.ImageField(upload_to=category_path(os.path.join('products','category')))
	slug=models.SlugField(blank=True)
	def __str__(self):
		return self.category_name
	def save(self, *args, **kwargs):
		self.slug=self.category_name.replace(" ","-")
		self.slug = self.slug.lower()
		im=Image.open(self.category_image)
		im = im.convert('RGB')
		im=im.resize((250,200))
		io=BytesIO()
		im.save(io,"JPEG")
		self.category_image=File(io, name=self.category_image.name)
		super().save(*args, **kwargs)
 

class ProductWithCount(models.Model):
	product=models.ForeignKey('Product',on_delete=models.CASCADE)
	count=models.IntegerField(default=1)
	brand=models.CharField(max_length=50, blank=True, null=True)

class Cart(models.Model):
	"""docstring for Cart"""
	products=models.ManyToManyField('ProductWithCount', blank=True)
	printing=models.ManyToManyField(PrintDoc, blank=True)
	user=models.OneToOneField(User, on_delete=models.CASCADE)

class Order(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	transaction_id=models.CharField(blank=True, null=True, max_length=256)
	order_id=models.UUIDField(default=uuid.uuid4, unique=True)
	address=models.ForeignKey(Address, on_delete=models.CASCADE)
	shop_order=models.ManyToManyField('ProductWithCount', blank=True)
	print_order=models.ManyToManyField(PrintDoc, blank=True)
	method=models.CharField(max_length=50, blank=True, null=True)
	shipping_price=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	price=models.DecimalField(max_digits=6, decimal_places=2) 
	date=models.DateTimeField()
	active=models.BooleanField(default=False)
	delivered=models.BooleanField(default=False)
	not_responding=models.BooleanField(default=False)
	class Meta:
		ordering=['-date']

class CustomOrder(models.Model):
	"""Will contain Order for different User"""
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	address=models.ForeignKey(Address, on_delete=models.CASCADE)
	brand=models.CharField(max_length=64, blank=True, null=True)
	category=models.CharField(max_length=64, blank=True, null=True)
	number=models.IntegerField(validators=[MinValueValidator(1)], help_text="Only Number are allowed")
	expected_price=models.IntegerField(validators=[MinValueValidator(1)], help_text="Only number are allowed")
	additional_info=models.TextField(blank=True, null=True)
	delivered=models.BooleanField(default=False)	
	cancel=models.BooleanField(default=False)# cancel is true if user does not respond