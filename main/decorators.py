from django.http import HttpResponse
from django.shortcuts import redirect

from account.models import *

# Create your decorators here.

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == True and request.user.is_leader == False:
				return redirect('account:index_admin')
			elif request.user.is_staff == False and request.user.is_leader == True:
				return redirect('account:index_leader')
			elif request.user.is_staff == False and request.user.is_leader == False:
				return redirect('account:index_pelamar')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func



def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki hak akses')
		return wrapper_func
	return decorator