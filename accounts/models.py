from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings 

class Tag(models.Model):
	name = models.CharField(max_length=200 , null=True)

	def __str__(self):
		return self.name

class Customer(models.Model):
	user = models.OneToOneField(User , on_delete=models.SET_NULL , null=True)
	name = models.CharField(max_length=200 , null=True)
	phone = models.CharField(max_length=200 , null=True)
	pic = models.ImageField( null=True , blank=True )
	email = models.CharField(max_length=200 , null=True)
	data_created = models.DateTimeField(auto_now_add=True , null=True)

	def __str__(self):
		return self.name

# def content_file_name(instance, filename):
#     return '/'.join(['content', instance.user.username, filename])
# upload_to= content_file_name,

class Product(models.Model):
		CATEGORY = (
					('Indoor' , 'Indoor'),
					('Out Door' , 'Out Door'),
					)

		name = models.CharField(max_length=200 , null=True)
		price = models.FloatField(default = 1 , null=True)
		category = models.CharField(max_length=200 , null=True , choices=CATEGORY)
		description = models.CharField(max_length=200 , null=True)
		data_created = models.DateTimeField(auto_now_add=True , null=True)
		tags = models.ManyToManyField(Tag)
		ordered = models.IntegerField(default = 0 , null= True)
		photo = models.ImageField(upload_to=settings.MEDIA_ROOT , null=True , blank=True)		
		 
		def __str__(self):
			return self.name  

		@property
		def photo_url(self) :
			if self.photo and hasattr(self.photo , 'url'):
				return self.photo.url 


class Order(models.Model):
	STATUS = (
				('Pending' , 'Pending'),
				('Out for Delivery' , 'Out for Delivery'),
				('Delivered' , 'Delivered'),
			)

	customer = models.ForeignKey(Customer , on_delete = models.SET_NULL, null = True)
	product = models.ForeignKey(Product , on_delete = models.SET_NULL , null = True)
	data_created = models.DateTimeField(auto_now_add=True , null=True)
	status =  models.CharField(max_length=200 , null=True , choices=STATUS)
	note = models.CharField(max_length=1000 , null=True )
	
	# def __str__(self):
	# 	return self.product