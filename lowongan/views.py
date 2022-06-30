from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

from account.models import *
from account.decorators import *

from dss.models import *

from kriteria.models import *

from datetime import datetime

users = get_user_model()

# Create your views here.

#Lowongan
@login_required(login_url='login1')
@admin_leader
def lihat_lowV(request):
	db_low	 = lowongan.objects.all()
	db_cand  = candidate.objects.all()
	db_verif = verify.objects.all()

	low_ada = True
	if db_low.exists():
		if datetime.now().date() >= db_low[0].tgl_buka and datetime.now().date() < db_low[0].tgl_tutup:
			db_low.update(status='dibuka')
		else:
			db_low.update(status='ditutup')
	else:
		low_ada = False

	verif_ada = False
	if db_verif.exists():
		verif_ada = db_verif[0].verifikasi

	context = {
		'judul'		:'Lowongan',
		'judul_isi'	:'Lowongan',
		'tabel'		:db_low,
		#-----
		'jumlah'	:db_low.count(),
		'verif'		:verif_ada,
	}
	return render(request, 'lowongan/lihat_lowongan.html', context)


@login_required(login_url='login1')
@admin_only
def tambah_lowV(request):
	data_form = lowongan_form(request.POST or None)
	if request.method == 'POST':
		if data_form.is_valid():
			data_form.save()
			return redirect('lowongan:lihat_low')

	context = {
		'judul'		:'Lowongan',
		'judul_isi' :'Tambah Lowongan',
		'data'		:data_form,
	}
	return render(request, 'lowongan/formtu_lowongan.html', context)


@login_required(login_url='login1')
@admin_only
def ubah_lowV(request, ubah_id):
	data_ubah = lowongan.objects.get(id_lowongan=ubah_id)
	data_form = lowongan_form(request.POST or None, request.FILES or None, instance=data_ubah)
	if request.method == 'POST':
		if data_form.is_valid():
			data_form.save()
			return redirect('lowongan:lihat_low')

	context = {
		'judul'		:'Lowongan',
		'judul_isi'	:'Ubah Lowongan',
		'data'		:data_form,
	}
	return render(request, 'lowongan/formtu_lowongan.html', context)


@login_required(login_url='login1')
@admin_only
def hapus_lowV(request, hapus_id):
	lowongan.objects.filter(id_lowongan=hapus_id).delete()
	users.objects.filter(is_staff=False, is_leader=False).delete()
	kriteria.objects.all().delete()
	return redirect('lowongan:lihat_low')