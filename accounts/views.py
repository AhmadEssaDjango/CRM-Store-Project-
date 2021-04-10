from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages 
from django.contrib.auth import authenticate ,  login , logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group , User
from .models import * 

from .forms import OrderForm , CustomerForm , CreateUserForm ,ProductCreateForm , CreateTagForm
from .decorators import admin_only , unauthenticated_user , allowed_users 
from .filters import OrderFilter



@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userStore(request) : 
	outDoor =  Product.objects.filter(category= 'Out Door')
	indoor = Product.objects.filter(category='Indoor')
	total = Product.objects.all().count()
	context = {
		'total' : total , 
		'title' : 'Store', 
		'outdoor' : outDoor ,
		'indoor' : indoor,
	}

	return render(request , 'accounts/user-store.html' , context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customers'])
def UserPage(request, user_id):
	orders = request.user.customer.order_set
	
	context = {
		'total_orders' : orders.count,
		'title' : request.user,
		'delivered' : orders.filter(status = 'delivered').count,
		'pending' : orders.filter(status = 'pending').count
	}
	return render(request , 'accounts/user.html' , context)

def UserLogout(request) :
	logout(request)
	return redirect('login')


@unauthenticated_user
def UserLogin(request):
	
	if request.method == 'POST' :
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request , username = username , password= password)

		if user is not None  :
			login(request , user )
			return redirect('home')
		else :
			messages.info(request, "Wrong Login Information !")


	return render(request , 'accounts/login.html')

@unauthenticated_user
def UserRegister(request):

	form = CreateUserForm()
	if request.method == 'POST' :
		form = CreateUserForm(request.POST) 
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(name = 'customers')
			customer = Customer.objects.create(
					user = user ,
					name = form.cleaned_data.get('username') ,
					email = form.cleaned_data.get('email')
				)
			user.groups.add(group)

			username = form.cleaned_data.get('username')
			messages.success(request , " Account created , Please login "+ username )
			return redirect('login')
	context = {
		'form' : form		
	}
	return render(request , 'accounts/register.html', context )

@login_required(login_url = 'login')
@admin_only
def home(request):
	orders = Order.objects.all()[:5]
	customers = Customer.objects.all()[:20]

	total_customers = Customer.objects.count()
	total_orders = Order.objects.count()

	delivered = Order.objects.filter(status = 'Delivered').count()
	pending = Order.objects.filter(status = 'Pending').count()

	context =  {
		'orders' : orders ,
		'customers' : customers,
		'total_orders':total_orders,
		'total_customers' : total_customers ,
		'delivered' : delivered ,
		'pending' : pending,
	}

	return render(request , 'accounts/dashboard.html' , context )

@login_required(login_url = 'login')
@admin_only
def products(request):
 
	products = Product.objects.all()
	context = {
		'products' : products , 
		'title' : 'Products'
	}

	return render(request , 'accounts/products.html' , context )

@login_required(login_url = 'login')
@admin_only
def createProduct(request):
	categorys = ['Indoor' , 'Out Door']
	tags = Tag.objects.all()
	form = ProductCreateForm()
	if request.method == 'POST':
		form = ProductCreateForm(request.POST , request.FILES)

		if form.is_valid():
			product = form.save()
			return redirect('/products')
	context = {
 		'form' : form , 
 		'categorys' : categorys,
 		'tags' : tags
 	}
	return render(request , 'accounts/create_product.html' , context )


@login_required(login_url = 'login')
@admin_only
def updateProduct(request , product_id):
	old_product = get_object_or_404(Product , id=product_id)
	form = ProductCreateForm(instance=old_product)
	tags = Tag.objects.all()
	
	if request.method == 'POST' :
		form = ProductCreateForm(request.POST, request.FILES, instance=old_product)
		if form.is_valid() :
			form.save()
			return redirect('products')

	context= {
		'form' : form ,
		'categorys' :  ['Indoor','Out Door'],
		'tags' :  tags,
		'old_product':old_product

	}

	return render(request , 'accounts/create_product.html' , context)

@login_required(login_url = 'login')
@admin_only
def deleteProduct(request, product_id):
	product = get_object_or_404(Product , id = product_id)
	try : 
		product.delete()
	except err :
		throw(err)
	return redirect('/products')



@login_required(login_url = 'login')
@admin_only
def customer(request , customer_id):
	customer = get_object_or_404(Customer , id=customer_id)
	orders = customer.order_set.all()
	total_orders = orders.count()

	myFilter = OrderFilter(request.GET , queryset=orders)
	orders = myFilter.qs
	if request.method == 'POST' : 
		myFilter = OrderFilter(request.POST)
		
	context = {
		'customer' : customer,
		'total_orders' : total_orders,
		'orders' : orders,
		'myFilter': myFilter
	}

	return render(request , 'accounts/customer.html' , context )

@login_required(login_url = 'login')
@admin_only
def createOrder(request , customer_id) :
	OrderFormSet = inlineformset_factory(
			Customer , 
			Order ,
			fields = ('product','status'),
			extra = 5 
			)

	customer = get_object_or_404(Customer , id=customer_id)
	formset = OrderFormSet(queryset=Order.objects.none() , instance=customer)

	if request.method == 'POST':
		formset = OrderFormSet(request.POST , instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = { 
		'customer' : customer ,
		'formset' : formset}
	return render(request, 'accounts/order_form.html' , context)

@login_required(login_url = 'login')
@admin_only
def UpdateOrder(request , order_id) :
	old_order = get_object_or_404(Order , id=order_id) 
	form = OrderForm(instance = old_order)
	if request.method == 'POST' :
		form = OrderForm(request.POST , instance = old_order)
		if form.is_valid():
			form.save() 
			return redirect('/')
	context = {'form' : form}

	return render(request , 'accounts/order_form.html' , context)


@login_required(login_url = 'login')
@admin_only
def DeleteOrder(request , order_id) :

	item = get_object_or_404(Order , id=order_id)
	
	if request.method == 'POST':
		item.delete()
		return redirect('/')
	
	context = {
		'item' : item
	}
	
	return render(request , 'accounts/delete.html' , context)

@login_required(login_url='login')
def createTag(request) :
	form = CreateTagForm()
	if request.method == 'POST' : 
		form = CreateTagForm(request.POST) 	
		if form.is_valid():
			tag = form.save()
			messages.success(request , f'The Tag " {tag} " has been added successfully ! ')
			
	context = {
		'form' : form ,

	}
	return render(request , 'accounts/create_tag.html' , context )
