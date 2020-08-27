from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, ProductCategory, Cart, ProductWithCount, Order, CustomOrder
from django.utils import timezone
from login.models import User, Address
from paytm import Checksum
from django.conf import settings
from print.models import PrintDoc 
from .forms import CustomOrderForm
from print.views import make_dir, exists
import os
from django.contrib.auth.decorators import login_required
from login.views import sendmail
# Create your views here.
def check(session):
	if 'id' in session:
		return True
	else:
		return False
def category(request):
	obs=ProductCategory.objects.all()
	return render(request,"shop/show.html",{'obs':obs})

def product(request,id):		#this should be made form type
	try:
		ob=Product.objects.get(p_id=id)	#this id corresponds to send id by user
	except exception as e:
		return redirect("shop:show")
	else:
		return render(request,"shop/buy.html",{'ob':ob})

def make_product(request):
	"""handling products not in catalog entry"""
	user=ret_user(request.session)
	if user is None:
		return redirect('login:login')
	verified=request.session.get('verified',False)
	if not verified:
		return redirect('login:verify_user')
	if request.method=="POST":
		form=CustomOrderForm(user,request.POST)
		try:
			ob=form.save(commit=False)
			ob.user=user
			ob.save()
			sendmail(['krishstationers12@gmail.com'],
				'Custom Order placed','please check it at serve9899/custom-order')
			return render(request,"shop/get_back.html")
		except Exception as e:
			return HttpResponse('Please fill all the information')
	else:
		return HttpResponse("You should not be here.")
	"""	base=settings.BASE_DIR
		path=os.path.join(base,"orders",user.name+"_"+user.phone_no)
		make_dir(path)
		filename=str(timezone.now())+".txt"
		path=os.path.join(path,filename)
		with open(path,"w+") as file:
			val="User: "
			val=val+user.name+"\n"+"Address: "
			for ob in user.address_set.all():
				val=val+ob.house_no+" "+ob.street+" "+ob.locality+" "+ob.city+" "+ob.state
				val=val+"\n"
			val=val+"brand: "+request.POST['brand']+"\n"
			val=val+"type: "+request.POST['type']+"\n"
			val=val+"copies: "+str(request.POST['copies'])+"\n"
			val=val+"Expected Price: "+ str(request.POST['price'])+"\n"
			val=val+"Additional Info: "+ request.POST['add-info']+"\n"
			file.write(val)"""

	

@login_required
def specific_category(request,category):
	"""I cant remove the login because it will give you error because of custom login page"""
	user=request.user
	category=category.replace("-"," ")
	try:
		ob=ProductCategory.objects.get(category_name__iexact=category)
	except Exception as e:
		return HttpResponse("Please go back and try again.")
	else:
		products=ob.product_set.all()
		form=CustomOrderForm(curr_user=user)
		return render(request,"shop/products.html",{'obs':products,'cat':category,'form':form}) 

"""def buy(request,id):	#make a forms type object
	warning=""
	if 'id' not in request.session:
		return redirect('login:login')
	if request.session['verified']==False:
		return redirect('login:verify_user')
	try:
		user=User.objects.get(email__iexact=request.session['id'])
	except Exception as e:
		return HttpResponse("Please login again")
	if request.method=="POST":
		add_id=request.POST['address']
		try:
			ob=Product.objects.get(p_id=id)
			add=Address.objects.get(id=add_id)
		except Exception as e:
			warning="Product not Found. Something Wrong"
			return HttpResponse('Something wrong. we will surely get back to this')
		else:
			now=timezone.now()
			o=Orders(Product_name=ob.name,p_id=ob.p_id,active=True,user=user,address=add,buy_date=now)
			o.save()
			return render(request,'shop/success.html')
	add=user.address_set.all()
	return render(request,'shop/confirm.html',{'address':add, 'id':id})"""

def ret_user(session):
	try:
		user=User.objects.get(email__iexact=session['id'])
	except Exception:
		return None
	return user

@login_required
def add_to_cart(request):
	user=request.user
	if user is None:
		return redirect('login:login')
	if request.method=="POST":
		cart=user.cart
		"""in the post method always pass the Product with count's id"""
		"""also to take care of printing order pass the type too"""
		if request.POST['type']=='S':
			product=Product.objects.get(p_id=request.POST['product_id'])
			p=ProductWithCount()
			p.product=product
			if int(request.POST['count'])<=0:
				return HttpResponse("So sorry currently negative Orders are not allowed. Please go back and try again")
			p.count=request.POST['count']
			if 'brand' in request.POST:
				p.brand=request.POST.get('brand')
			p.save()
			cart.products.add(p)
		elif request.POST['type']=='P':
			doc=PrintDoc.objects.get(id=request.POST['print_id'])
			cart.printing.add(doc)
		else:
			return HttpResponse("No s or p chhosen")	#replace if with referer
	return redirect('shop:show-cart')

@login_required
def remove_from_cart(request):
	user=request.user
	if request.method=="POST":
		cart=user.cart
		if request.POST['type']=='S':
			product=ProductWithCount.objects.get(id=request.POST['product_id'])
			cart.products.remove(product) 
			product.delete()
		elif request.POST['type']=='P':
			doc=PrintDoc.objects.get(id=request.POST['print_id'])
			cart.printing.remove(doc)
			doc.delete()
		else:
			return HttpResponse("You have done something wrong with POST request")
	return referer(request.META)

@login_required
def checkout(request):
	"""after this i will be displaying confirmation where price etc are shown also address is selected"""
	"""it selects the address and redirect to the payments page"""
	user=request.user
	if not user.verified:
		return redirect('login:verify_user')
	cart=user.cart
	if request.method=="POST":
		o=Order()
		o.user=user
		o.address=Address.objects.get(id=request.POST['add_id'])	#form field for giving address
		price=0
		for ob in cart.products.all():
			price=price+(ob.product.prices*ob.count)
		for ob in cart.printing.all():
			price=price+ob.price
		if price < 50:
			return HttpResponse('We are only delivering items worth more than Rs. 50')
		o.price=price
		o.date=timezone.now()
		o.method=request.POST['method']
		o.save()
		for product in cart.products.all():
			o.shop_order.add(product)
		for prints in cart.printing.all():
			o.print_order.add(prints)
		o.save()
		cart.products.clear()
		cart.printing.clear()
		if o.method=="online":
			payload=generate(o)
			return render(request,'payments/merchant.html',{'para':payload})
		elif o.method=="cash":
			o.active=True
			o.save()
			sendmail(['krishstationers12@gmail.com']
				,'Order Placed','Please check server9899/show-table')
			return render(request,'shop/success.html')
	add=user.address_set.all()
	stationery=cart.products.all()
	printing=cart.printing.all()
	price=0
	for ob in cart.products.all():
		price=price+(ob.product.prices*ob.count)
	for ob in cart.printing.all():
		price=price+ob.price
	return render(request,'shop/confirm.html',{'address':add,'stationery':stationery,
		'print_doc':printing, 'price':price})

@login_required
def show_cart(request):
	user=request.user
	if not user.verified:
		return redirect('login:verify_user')
	cart=user.cart
	products=cart.products.all()
	printing=cart.printing.all()
	price=0
	for ob in cart.products.all():
		price=price+ob.product.prices*ob.count
	for ob in cart.printing.all():
		price=price+ob.price
	return render(request,'shop/showCart.html',{'products':products,'print_doc':printing,'price':price})

def referer(meta):
	red=meta.get('HTTP_REFERER')
	if red==None:
		return redirect('login:home')
	else:
		return redirect(red)

def generate(order):
	dic={
	"mid":"WqmatC77859343122059",
	"order_id":str(order.order_id),
	"customer_id":str(order.user.user_id),
	"txn_amount":str(order.price),
	"channel_id":"WEB",
	"website":"WEBSTAGING",
	"mobile_no":str(order.user.phone_no),
	"industry_type_id":"Retail",
	"callback_url":"http://127.0.0.1:8000/payments/verify"
	}
	checksum=Checksum.generate_checksum(dic,"2aqz4AwRzEM#8Wl@")
	dic["checksum"]=checksum
	return dic

def cancel_order(request):
	if not check(request.session):
		return redirect('login:login')
	user=ret_user(request.session)
	if request.session['verified']==False:
		return redirect('login:verify_user')
	if request.method=="POST":
		try:
			order=Order.objects.get(order_id=request.POST['order_id'])
		except Exception:
			return HttpResponse("Cannot process your request now")
		else:
			cancel=True
			if order.print_order.exists():
				cancel=False
			order.active=True
			order.delivered=True
			order.save()
			return render(request,'shop/cancel.html',{'cancel':cancel})
	else:
		return HttpResponse("Wrong Page")
