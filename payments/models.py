from django.db import models
from login.models import User
# Create your models here.

class TransactionDetails(models.Model):
	GATEWAYNAME=models.CharField(max_length=30)
	RESPMSG=models.TextField()
	BANKNAME=models.CharField(max_length=500)
	PAYMENTMODE=models.CharField(max_length=30)
	RESPCODE=models.IntegerField()
	TXNID=models.CharField(max_length=70)
	TXNAMOUNT=models.DecimalField(max_digits=7,decimal_places=2)
	ORDERID=models.UUIDField()
	STATUS=models.CharField(max_length=30)
	BANKTXNID=models.CharField(max_length=256)
	TXNDATE=models.DateTimeField()
	CHECKSUMHASH=models.CharField(max_length=256)
	user=models.ForeignKey(User,on_delete=models.CASCADE)