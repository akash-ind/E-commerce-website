from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from shop.models import Order, CustomOrder
from print.models import PrintDoc
from django.utils.encoding import smart_str
from django.utils import timezone
from django.conf import settings
import os
from datetime import timedelta
import shutil
# Create your views here. 
def login_form(request):
	warning=""
	if request.method=="POST":
		name=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=name,password=password)
		if user is not None:
			login(request,user)
			return redirect('serve:show-table')#add urls
		else:
			warning="Credentials do not match"
	return render(request,'serve/login.html')

@login_required(login_url='serve:login')
def show(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	quer=Order.objects.filter(active=True).filter(delivered=False)
	quer=quer.order_by("-date")
	quer=quer.order_by("address")
	return render(request,'serve/show_table.html',{'objects':quer})

@login_required(login_url='serve:login')
def expand_order(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	if request.method=="POST":
		order_id=request.POST['id']
		ob=Order.objects.get(order_id=order_id)
		return render(request,'serve/expand.html',{'ob':ob})
	return HttpResponse("wrong Page go back")

@login_required(login_url='serve:login')
def cancel_order(request):
	if request.method=="POST":
		order_id=request.POST['id']
		ob=Order.objects.get(order_id=order_id)
		ob.not_responding=True
		ob.active=False
		ob.save()
		return redirect('serve:show-table')
	return HttpResponse("wrong Page go back")

def get_object(model,dic):
	for key, val in dic.items():
		ob=model.objects.get(key=val)
		return ob

@login_required(login_url="serve:login")
def cancel_custom(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	if request.method=="POST":
		ob=CustomOrder.objects.get(id=request.POST['id'])
		ob.cancel=True
		ob.delivered=True
		ob.save()
		return redirect('serve:view-custom-order')
	return HttpResponse('Wrong Page')

@login_required(login_url="serve:login")
def expand_custom(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	if request.method=="POST":
		ob=CustomOrder.objects.get(id=request.POST['id'])
		return render(request,'serve/expand-custom.html',{'ob':ob})
	return HttpResponse('Wrong Page')

@login_required(login_url="serve:login")
def process(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	if request.method=="POST":
		try:
			o=Order.objects.get(order_id=request.POST['order'])
		except Exception:
			return HttpResponse("Something Wrong happened")
		else:
			o.active=False
			o.delivered=True
			o.save()
			return redirect('serve:show-table')
	return HttpResponse('Wrong Page')

@login_required(login_url="serve:login")
def logout_user(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	logout(request)
	return redirect('serve:login')


@login_required(login_url="serve:login")
def printing_process(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	obj=PrintDoc.objects.filter(order__active=True).filter(deleted=False)
	return render(request,'serve/process-prints.html',{'obs':obj})

@login_required(login_url="serve:login")
def download_file(request,id):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	media=settings.MEDIA_ROOT
	try:
		ob=PrintDoc.objects.get(id=id)
	except Exception:
		return HttpResponse("go back and try again")
	else:
		path=os.path.join(media, ob.document.name)
		response=FileResponse(open(path))
		return response

@login_required(login_url="serve:login")
def download_info(request,id):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	media=settings.MEDIA_ROOT
	try:
		ob=PrintDoc.objects.get(id=id)
	except Exception:
		return HttpResponse("GO back and try again")
	else:
		file=os.path.dirname(ob.document.name)
		file=os.path.join(file,'info.txt.conf')
		path=os.path.join(media,file)
		response=FileResponse(open(path))
		return response

@login_required(login_url="serve:login")
def deletefile(request,id):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	media=settings.MEDIA_ROOT
	try:
		ob=PrintDoc.objects.get(id=id)
	except Exception:
		return HttpResponse("go back and try again")
	else:
		file=os.path.dirname(ob.document.name)
		path=os.path.join(media,file)
		shutil.rmtree(path)
		ob.deleted=True
		ob.save()
		return redirect('serve:provide-print')

@login_required(login_url="serve:login")
def process_custom_order(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	obs=CustomOrder.objects.filter(delivered=False)
	return render(request,'serve/process-custom.html',{'obs':obs})

@login_required(login_url="serve:login")
def delivered_custom_order(request,id):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	try:
		ob=CustomOrder.objects.get(id=id)
	except Exception:
		return HttpResponse("go back and try again")
	else:
		ob.delivered=True
		ob.save()
		return redirect('serve:view-custom-order')

@login_required(login_url="serve:login")
def delete_unprocessed_prints(request):
	if not request.user.is_superuser():
		return HttpResponse("Access Denied")
	val=timezone.now()-timedelta(hours=3)
	obs=PrintDoc.objects.filter(time__lte=val).filter(deleted=False)
	media=settings.MEDIA_ROOT
	for ob in obs:
		cart=ob.user.cart
		for docs in cart.printing.all():
			if ob == docs:
				cart.printing.remove(ob)
		file=os.path.dirname(ob.document.name)
		path=os.path.join(media,file)
		shutil.rmtree(path)
		ob.deleted=True
		ob.save()
		return redirect('serve:provide-print')
