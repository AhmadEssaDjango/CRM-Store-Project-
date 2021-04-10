from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
	class Meta : 
		model  = Order
		fields = '__all__'

class ProductCreateForm(ModelForm):
	class Meta:
		model = Product
		fields = [ 'name' , 'price' , 'category' , 'description' , 'tags' , 'photo' ]
		
class CustomerForm(ModelForm):
	class Meta : 
		model = Customer
		fields = '__all__'


class CreateUserForm(UserCreationForm) : 
	class Meta :
		model = User 
		fields =['username' , 'email' ,'password1' , 'password2' ]

class CreateTagForm(ModelForm):
	class Meta :
		model = Tag 
		fields = '__all__'