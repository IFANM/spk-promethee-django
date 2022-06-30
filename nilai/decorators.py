from django.http import HttpResponse
from django.shortcuts import redirect

from .models import *
from account.models import *
from kriteria.models import *

# Create your decorators here.

def alternatif_ada(view_func):
	def wrapper_func(request, *args, **kwargs):
		cand = candidate.objects.all()

		if cand.exists():
			return view_func(request, *args, **kwargs)
		else:
			return redirect('account:lihat_cand')

	return wrapper_func



def nilai_lengkap(view_func):
	def wrapper_func(request, *args, **kwargs):
		nil  = nilai.objects.all()
		cand = candidate.objects.all()
		krit = kriteria.objects.all()

		if nil.count() < (cand.count() * krit.count()):
			if request.user.is_authenticated:
				if request.user.is_staff == True and request.user.is_leader == False:
					return redirect('nilai:lihat_nilai')
				elif request.user.is_staff == False and request.user.is_leader == True:
					return redirect('nilai:lihat_nilai')
				else:
					return HttpResponse('Anda tidak memiliki akses ke Halaman ini')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func