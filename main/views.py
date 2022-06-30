from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .decorators import *
from account.forms import *
from account.models import *
from lowongan.models import *

# Create your views here.

@unauthenticated_user
def indexV(request):
	db_low  = lowongan.objects.all()
	db_cand = candidate.objects.all()

	low_ada = True
	if db_low.exists():
		if datetime.now().date() >= db_low[0].tgl_buka and datetime.now().date() < db_low[0].tgl_tutup:
			db_low.update(status='dibuka')
		else:
			db_low.update(status='ditutup')
	else:
		low_ada = False

	context = {
		'judul'		:'Beranda',
		'judul_isi'	:'Griya Belajar Pintar Arrava',
	}
	return render(request, 'index_anonym.html', context)


@unauthenticated_user
def lowong_kerjaV(request):
	db_low  = lowongan.objects.all()
	db_cand = candidate.objects.all()

	low = 0
	low_status= ''
	low_ada = True
	if db_low.exists():
		low = db_low[0]
		low_status= db_low[0].status
	else:
		low_ada = False

	context = {
		'judul'		:'Lowongan Kerja',
		'judul_isi' :'Informasi Lowongan Kerja',
		#-----
		'data'		:low,
		'status'	:low_status,
		'lowongan'  :low_ada,
	}
	return render(request, 'lowong_kerja.html', context)


@unauthenticated_user
def registrasiV(request):
	data_form1 = user_create_form(request.POST or None)
	data_form2 = profil_cand_form(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if data_form1.is_valid():
			user = data_form1.save()
			if data_form2.is_valid():
				profil = data_form2.save(commit=False)
				profil.cand_mail = user
				profil.save()
				return redirect('login1')
			else:
				users.objects.filter(id_user=user.id_user).delete()
				messages.info(request, 'Maaf Data Profil Tidak Valid!')
		else:
			messages.info(request, 'Maaf Data User Tidak Valid!')

	context = {
		'judul'		:'Registrasi',
		'judul_isi' :'Registrasi Pelamar',
		'data1'		:data_form1,
		'data2'		:data_form2,
	}
	return render(request, 'registrasi_pelamar.html', context)


@unauthenticated_user
def loginV(request):
	if request.method == 'POST':
		u_login = request.POST['username']
		p_login = request.POST['password']

		user = authenticate(request, username=u_login, password=p_login)
		
		if user is not None:
			login(request, user)
			if request.user.is_staff == True and request.user.is_leader == False:
				return redirect('account:index_admin')
			elif request.user.is_staff == False and request.user.is_leader == True:
				return redirect('account:index_leader')
			elif request.user.is_staff == False and request.user.is_leader == False:
				cand = candidate.objects.filter(cand_mail=request.user)
				if cand.exists():
					return redirect('account:index_pelamar')
				else:
					logout(request)
					messages.info(request, 'Maaf Email Anda tidak terhubung dengan Akun!')
					return redirect('login1')
		else:
			messages.info(request, 'Maaf Email atau Password tidak benar!')
			return redirect('login1')

	context = {
		'judul'		:'Masuk',
		'judul_isi'	:'Silahkan Masukkan Data Anda',
	}
	return render(request, 'login.html', context)


@login_required(login_url='login1')
def logoutV(request):
	context = {
		'judul'		:'Keluar',
		'judul_isi'	:'Anda Ingin Keluar Dari Sistem?',
	}

	if request.method == 'POST':
		logout(request)
		return redirect('index')

	return render(request, 'logout.html', context)