from django.shortcuts import render, redirect
from .forms import UploadDocument
from .models import PrintDoc
from login.models import User
import os
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
single_sided={
	'p':{
		'c':4,
		'b':2
		},
	'e':{
		'c':10,
		'b':7,
	}
}
double_sided={
	'p':{
		'c':6,
		'b':3
	}
}
def check(session):
	if 'id' not in session:
		return False
	else:
		return True
@login_required
def print(request): 
	form=UploadDocument()
	if request.method=="POST":
		user=request.user
		if user is None:
			return redirect('login:login')
		form=UploadDocument(request.POST,request.FILES)
		if form.is_valid():
			ob=form.save(commit=False)
			if ob.pages<=0:
				return HttpResponse(f"You cannot print {ob.pages} pages")
			ob.user=user
			if request.POST['double_sided']=="True":
				if ob.paper_type=='e':
					return HttpResponse('Double Sided is not available in Glossy paper as they are smooth only one side')
				ob.price=ob.pages*ob.copies*double_sided[ob.paper_type][ob.color]
			else:
				ob.price=ob.pages*ob.copies*single_sided[ob.paper_type][ob.color]
			handle_file(request.FILES['document'], ob,request.POST['double_sided'],request.POST['some_other_info'])
			ob.time=timezone.now()
			ob.save()
			return render(request,'print/add-to-cart.html',{'print_id':ob.id})
	return render(request,'print/upload_file.html',{'form':form})


def handle_file(file, fob, two, info):
	base=settings.MEDIA_ROOT
	file.name=file.name.split('/')[-1]
	path=os.path.join(base,"printing", fob.user.name+"_"+fob.user.phone_no,
		str(fob.user.printdoc_set.count()+1), "info.txt")
#	import random
	make_dir(os.path.dirname(path))
#	while exists(path):
#		path=path+str(int(random.uniform(1,100)))
	text_path=path+".conf"
	with open(text_path, 'w+') as text:
		val="color: "+fob.color+"\n"
		val=val+"copies: "+str(fob.copies)+"\n"
		val=val+"pages: "+str(fob.pages)+"\n"
		val=val+"paper type: "+str(fob.paper_type)+"\n"
		val=val+"two_sided: "+str(two)+"\n"
		if info is not None:
			val=val +"some_other_info:"+info+"\n"
		text.write(val)
#	with open(path,'wb+') as f:
#		for chunks in file.chunks():
#			f.write(chunks) 

def make_dir(path):
	if not exists(path):
		make_dir(os.path.dirname(path))
		os.mkdir(path)
	else:
		return
def exists(path):
	return os.path.exists(path)