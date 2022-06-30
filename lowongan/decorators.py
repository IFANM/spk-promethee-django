from django.http import HttpResponse
from django.shortcuts import redirect

from .models import *

# Create your decorators here.

def lowongan_ada(view_func):
	def wrapper_func(request, *args, **kwargs):
		low = lowongan.objects.all()

		if low.exists():
			return view_func(request, *args, **kwargs)
		else:
			return redirect('lowongan:lihat_low')
	
	return wrapper_func