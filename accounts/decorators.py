from django.http import HttpResponse 
from django.shortcuts import redirect 

def unauthenticated_user(view_func):
	def wrapper_func(requset, *args , **kwargs):
		if requset.user.is_authenticated :	
			return redirect('home')
		else :
			return view_func(requset, *args , **kwargs)

	return wrapper_func

def allowed_users(allowed_roles = []):
	def decorator(view_func):
		def wrapper_func(requset , *args , **kwargs):
			group = None
			if requset.user.groups.exists():
				group = requset.user.groups.all()[0].name 

			if group in allowed_roles:

				return view_func(requset , *args, **kwargs)
			else :
				return HttpResponse('Permission Required ')
		return	wrapper_func
	return decorator
def admin_only(view_func):
	def wrapper_func(requset , *args , **kwargs) :
		group = None 
		if requset.user.groups.exists():
			group = requset.user.groups.all()[0].name

		if group == 'customers':
			return redirect('/user/'+str(requset.user.id))
		if group == 'admins':
			return view_func(requset, *args , **kwargs)

	return wrapper_func