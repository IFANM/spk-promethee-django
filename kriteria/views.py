from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decorators import *

from account.decorators import *

from dss.models import *

from lowongan.decorators import *

# Create your views here.

# Kriteria Admin-Leader
@login_required(login_url='login1')
@admin_leader
@lowongan_ada
def lihat_kritV(request):
	db_krit = kriteria.objects.order_by('id_kriteria')
	db_verif= verify.objects.all()

	verif_ada = False
	if db_verif.exists():
		verif_ada = db_verif[0].verifikasi

	context = {
		'judul'		:'Kriteria',
		'judul_isi' :'Daftar Kriteria',
		'tabel'		:db_krit,
		#-----
		'verif' 	:verif_ada,
	}
	return render(request, 'kriteria/lihat_kriteria.html', context)


@login_required(login_url='login1')
@admin_only
def tambah_kritV(request):
	data_form = kriteria_form(request.POST or None)
	if request.method == 'POST':
		if data_form.is_valid():
			data_form.save()
			return redirect('kriteria:lihat_krit')

	context = {
		'judul'		:'Kriteria',
		'judul_isi'	:'Tambah Kriteria',
		'data'		:data_form,
	}
	return render(request, 'kriteria/formtu_kriteria.html', context)


@login_required(login_url='login1')
@admin_only
def ubah_kritV(request, ubah_id):
	data_ubah = kriteria.objects.get(id_kriteria=ubah_id)
	data_form = kriteria_form(request.POST or None, instance=data_ubah)
	if request.method == 'POST':
		if data_form.is_valid():
			data_form.save()
			return redirect('kriteria:lihat_krit')

	context = {
		'judul'		:'Kriteria',
		'judul_isi'	:'Ubah Kriteria',
		'data'		:data_form,
	}
	return render(request, 'kriteria/formtu_kriteria.html', context)


@login_required(login_url='login1')
@admin_only
def hapus_kritV(request, hapus_id):
	kriteria.objects.filter(id_kriteria=hapus_id).delete()
	return redirect('kriteria:lihat_krit')