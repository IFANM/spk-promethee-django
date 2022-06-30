from django.http import HttpResponse
from django.shortcuts import redirect

# Create your decorators here.

def admin_leader(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == True or request.user.is_leader == True:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki akses ke Halaman ini')

	return wrapper_func



def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == True and request.user.is_leader == False:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki akses ke Halaman Admin')

	return wrapper_func



def leader_pelamar(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == False and request.user.is_leader == True:
				return view_func(request, *args, **kwargs)
			elif request.user.is_staff == False and request.user.is_leader == False:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki akses ke Halaman ini')

	return wrapper_func



def leader_only(view_func):
	def wrapper_func(request,*args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == False and request.user.is_leader == True:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki akses ke Halaman Leader')

	return wrapper_func



def pelamar_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff == False and request.user.is_leader == False:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Anda tidak memiliki akses ke Halaman Pelamar')

	return wrapper_func