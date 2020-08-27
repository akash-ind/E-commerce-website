from django.shortcuts import render
from paytm import Checksum
from .models import TransactionDetails
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from login.models import User
from shop.models import Order
import requests
import json
def get_user(session):
	user=User.objects.get(email__iexact=session['id'])
	return user
@csrf_exempt
def verify_payment(request):
	if request.method=="POST":
		mess={}
		mid=request.POST["MID"]
		txn_id=request.POST["TXNID"]
		order_id=request.POST["ORDERID"]
		bank_txn_id=request.POST["BANKTXNID"]
		txn_amount=request.POST["TXNAMOUNT"]
		status=request.POST["STATUS"]
		resp_code=request.POST["RESPCODE"]
		resp_msg=request.POST["RESPMSG"]
		txn_date=request.POST["TXNDATE"]
		gateway_name=request.POST["GATEWAYNAME"]
		bank_name=request.POST["BANKNAME"]
		payment_mode=request.POST["PAYMENTMODE"]
		checksumhash=request.POST["CHECKSUMHASH"]
		paytmChecksum = ""
		paytmParams = {}
		for key, value in request.POST.items(): 
			if key == 'CHECKSUMHASH':
				paytmChecksum = value
			else:
				paytmParams[key] = value
		isValidChecksum = Checksum.verify_checksum(paytmParams,'2aqz4AwRzEM#8Wl@', paytmChecksum)
		msg={}
		if isValidChecksum:
			msg['check_verify']=True
		else:
			msg['check_verify']=False
		order=Order.objects.get(order_id=order_id)
		if order.price!=float(txn_amount):
			return HttpResponse("Something wrong happened")
		if not success(mid,order_id):
			return HttpResponse('Tampering with POST data')
		if status=="TXN_SUCCESS":
			msg['txn']="Success"
			order.transaction_id=txn_id
			order.active=True
			order.deliver=True
			order.save()
		elif status=="TXN_FAILURE":
			msg["txn"]="Failure"
		elif status=="PENDING":
			msg["txn"]="Pending"
		user=User.objects.get(order__order_id=order_id)
		t=TransactionDetails()
		t.GATEWAYNAME=gateway_name
		t.RESPMSG=resp_msg
		t.BANKNAME=bank_name
		t.PAYMENTMODE=payment_mode
		t.RESPCODE=resp_code
		t.TXNID=txn_id
		t.TXNAMOUNT=txn_amount
		t.ORDERID=order_id
		t.STATUS=status
		t.BANKTXNID=bank_txn_id
		t.TXNDATE=txn_date
		t.CHECKSUMHASH=checksumhash
		t.user=user
		t.save()
		return render(request,'payments/done.html',{'msg':msg})
	else:
		return HttpResponse("Wrong Page Go Back")

def success(mid, order_id):
	para={}
	para["MID"]=mid
	para["ORDERID"]=order_id
	checksum=Checksum.generate_checksum(para,'2aqz4AwRzEM#8Wl@')
	para['CHECKSUMHASH']=checksum
	post_data= json.dumps(para)
	url = "https://securegw-stage.paytm.in/order/status"
	response=requests.post(url, data=post_data,headers={"Content-type":"application/json"}).json()
	order=Order.objects.get(order_id=order_id)
	if response['ORDERID']!=order_id:
		return False
	if response['TXNAMOUNT']!=order.price:
		return False
	return True