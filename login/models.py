from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
import uuid
import random
def rand():
	no=random.randint(10000,99999)
	return no 
# Create your models here.

class Manager(BaseUserManager):
	def create_user(self, name, email, phone_no, password = None):
		if not email:
			raise ValueError('Users must have an email address')
		if not name:
			raise ValueError('Users must have a first name')
		if not phone_no:
			raise ValueError('User must have a mobile Number')
		user = self.model(name = name,
			email = self.normalize_email(email), phone_no= phone_no)
		user.set_password(password)
		print(user.password)
		user.save(using= self._db)
		return user

	def create_superuser(self, name, email, phone_no, password = None):
		if not email:
			raise ValueError('Users must have an email address')
		if not name:
			raise ValueError('Users must have a first name')
		if not phone_no:
			raise ValueError('User must have a mobile Number')
		user = self.model(name = name,
			email = self.normalize_email(email), phone_no= phone_no)
		user.set_password(password)
		user.is_superuser = True
		user.is_admin = True
		user.save(using= self._db)
		return user

class Address(models.Model):
	"""docstring for Address"""
	house_no=models.CharField(max_length=100)
	street=models.CharField(max_length=40)
	locality=models.CharField(max_length=100)
	city=models.CharField(max_length=100, default="New Delhi")
	state=models.CharField(max_length=100, default="Delhi")
	user=models.ForeignKey("User",on_delete=models.CASCADE)
	def __str__(self):
		return f"{self.house_no} {self.street} {self.locality} {self.city} {self.state}"
		
class User(AbstractBaseUser):
	name=models.CharField(max_length=256)
	email=models.EmailField(primary_key=True)
	user_id=models.UUIDField(default=uuid.uuid4)
	phone_no=models.CharField(max_length=12, unique=True)
	password=models.CharField(max_length=256)
	verified=models.BooleanField(default=False)
	is_admin = models.BooleanField(default = False)

	REQUIRED_FIELDS = ['name', 'phone_no', 'password']
	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	objects = Manager()

	def has_perm(self,perm , obj = None):
		return True

	def has_module_perms(self, app_label):
		if app_label == 'serve':
			if self.is_admin:
				return True
			else:
				return False
		return True

	@property
	def is_staff(self):
		return self.is_admin

	def is_active(self):
		return True

class Otp(models.Model):
	temp_no = models.IntegerField()
	user = models.OneToOneField('User', on_delete = models.CASCADE)

	def save(self, *args, **kwargs):
		self.temp_no = rand()
		super().save(*args, **kwargs)