from django.http import HttpResponse
from django.shortcuts import redirect

from .models import *

# Create your decorators here.

def kriteria_ada(view_func):
	def wrapper_func(request, *args, **kwargs):
		krit = kriteria.objects.all()

		if krit.exists():
			return view_func(request, *args, **kwargs)
		else:
			return redirect('kriteria:lihat_krit')

	return wrapper_func