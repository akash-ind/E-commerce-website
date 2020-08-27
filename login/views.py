from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegisterForm, LoginForm, MailForm, AddressForm
from .models import User, Address, Otp
from shop.models import Order,Cart
from shop.models import Product
from django.contrib.auth import hashers
from django.http import HttpResponse
import uuid
from datetime import datetime, timedelta
from django.contrib.auth import login as log_in, logout as log_out, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
	verified=False
	user = request.user
	if not user.is_anonymous:
		an=True
		if user.verified:
			verified=True
	else:
		an=False
	return render(request,'login/home.html',{'id':an,'verified':verified})

def contact(request):
	return render(request,'login/contactUs.html')

def register_user(request):
	user = request.user
	if not user.is_anonymous:
		return redirect('login:home')
	warning=""
	Userform=RegisterForm(request.POST or None)
	if request.method == "POST":
		if Userform.is_valid():			#i am using Javascript to check for confirm password and password matching
			try:
				User.objects.get(email__iexact=form.cleaned_data['email'])
				warning="User with following email exists"
			except Exception as e:
				ob=Userform.save()
				cart=Cart()
				cart.user=ob
				cart.save()
				otp = Otp()
				otp.user = ob
				otp.save()
				log_in(request, ob)
				return redirect('login:verify_user')
	return render(request,"login/register.html",{'form1': Userform, 'warning':warning})

	

@login_required
def mail(request):
	warning=""
	if request.method == "POST":
		try:
			ob=request.user
			if ob.verified == False:
				form=MailForm(request.POST)
				if form.is_valid():
					if form.cleaned_data['code']==ob.otp.temp_no:
						ob.verified=True
						request.session['verified']=True
						ob.save()
						return redirect('shop:show')
					else:
						warning="Entered Code is wrong"
			else:
				warning="You are already verified"
				return redirect('login:home')
		except Exception as e:
			warning="User not found. Try contacting the admin"
			return redirect('login:login')
	ob=request.user
	email=[]
	email.append(ob.email)
	subject="Verification Code"
	message=f"Your verification code is \n {ob.otp.temp_no}"
	sendmail(email,subject,message)
	form=MailForm()
	return render(request,'login/mail.html',{'form':form,'warning':warning})


def sendmail(email,subject,message):
	from_email="shop@krishstationers.in"
	send_mail(subject,message,from_email,email)
	return



def login(request):
	warning=""
	user = request.user
	if not user.is_anonymous:
		return redirect('login:home')
	if request.method == "POST":
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()
		else:
			return HttpResponse('Please enable cookies')
		form=LoginForm(request.POST)
		if form.is_valid():
			try:
				email=form.cleaned_data['email']
				password = form.cleaned_data['password']
				print(password)
				user = authenticate(request,email= email, password=password)
				if user is not None:
					log_in(request, ob)
				else:
					raise Exception
			except Exception as e:
				print(e)
				warning="Credentials do not match"
				return render(request,'login/login.html',{'form':form,'warning':warning})
			else:
				return redirect('login:home')
	request.session.set_test_cookie()
	form=LoginForm(request.POST or None)
	return render(request,'login/login.html',{'form':form,'warning': warning})


def logout(request):
	log_out(request)
	return redirect('login:home')


def reset(request):
	warning=""
	if request.method == "POST":
		email=request.POST['email']
		try:
			ob=User.objects.get(email__iexact=email)
		except Exception as e:
			warning="No User with this email"
		else:
			token=uuid.uuid4()
			subject="Reset Password"
			msg=f"Follow this link to reset your password. \
			This link will expire in 1 hour.\n{request.META['HTTP_HOST']}/change-password/{token}"
			ob.reset_pass_token=token
			ob.reset_time=timezone.now()
			ob.save()
			sendmail([ob.email],subject,msg)
			return HttpResponse('Check your Email for further instructions')
	return render(request,'login/forgot-password.html',{'warning':warning})
	


def verify(request,id):
	try:
		ob=User.objects.get(reset_pass_token=id)
	except Exception:
		return HttpResponse('This link is not valid')
	else:
		if ob.reset_time+timedelta(seconds=3600)>timezone.now():
			return redirect('login:change_pass',id=id)
		else:
			return HttpResponse('This link expired. Request for new one')




def change_password(request,id):
	if request.method=="POST":
		password=request.POST['password']
		id=request.POST['id']
		try:
			ob=User.objects.get(reset_pass_token=id)
		except Exception:
			return HttpResponse('Your password cannot be changed now')
		else:
			if ob.reset_time+timedelta(seconds=3600)>timezone.now():
				password=hashers.make_password(password)
				ob.reset_pass_token=uuid.uuid4()
				ob.password=password
				ob.save()
				return redirect('login:login')
			else:
				return HttpResponse('Your request cannot be processed now')
	return render(request,'login/change_pass.html',{'id':id})
	



@login_required
def account(request):
	ob = request.user
	orders=ob.order_set.all()
	return render(request,'login/user.html',{'user':ob,'orders':orders})




def review(request,id):
	try:
		order=Orders.objects.get(p_id=id)
	except Exception:
		return HttpResponse("This id is unfortunately not found")
	else:
		return render(request,'review_order.html',{'order':order})




def cancel(request,id):
	try:
		order=Orders.objects.get(p_id=id)
	except Exception:
		return HttpResponse("This id is unfortunately not found")
	else:
		order.active=False
		order.save()
		return redirect('login:home')




@login_required
def add_address(request):
	add=AddressForm()
	if request.method=="POST":
		user=request.user
		add=AddressForm(request.POST)
		if add.is_valid():
			ob=add.save(commit=False)
			ob.user=user
			ob.save()
			red=request.META.get('HTTP_REFERER')
			if red !=None:
				return redirect(red)
			else:
				return redirect('home') 
	return render(request,'login/address.html',{'form':add})
