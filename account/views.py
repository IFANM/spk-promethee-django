from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decorators import *

from dss.models import *

from lowongan.models import *
from lowongan.decorators import *

users = get_user_model()

# Create your views here.

# ---ADMIN
#Index
@login_required(login_url='login1')
@admin_only
def index_adminV(request):
	user 	  = request.user

	context = {
		'judul'		:'Arrava',
		'judul_isi'	:'SPK - Pemilihan Pengajar',
	}
	return render(request, 'account/admin/index_admin.html', context)


#User
@login_required(login_url='login1')
@admin_leader
def lihat_userV(request):
	db_user = users.objects.all()

	user 	  = request.user
	data_form = user_change_form(request.POST or None, instance=user)

	if request.method == 'POST':
		if data_form.is_valid():
			olah = data_form.save(commit=False)
			if request.user.is_staff == True:
				olah.is_active    = True
				olah.is_staff     = True
				olah.is_superuser = True
				olah.save()
			elif request.user.is_leader == True:
				olah.is_active = True
				olah.is_leader = True
				olah.save()
	
	context = {
		'judul'		:'User',
		'judul_isi'	:'Daftar User',
		'tabel'		:db_user,
		'data2'		:data_form,
	}
	return render(request, 'account/lihat_user.html', context)


#Candidate
@login_required(login_url='login1')
@admin_leader
@lowongan_ada
def lihat_candV(request):
	db_cand = candidate.objects.order_by('id_candidate')
	db_low	= lowongan.objects.all()
	db_verif= verify.objects.all()
	
	low_status = ''
	if db_low.exists():
		low_status = db_low[0].status

	verif_ada = False
	if db_verif.exists():
		verif_ada = db_verif[0].verifikasi

	context = {
		'judul'		:'Pelamar',
		'judul_isi'	:'Daftar Pelamar',
		'tabel'		:db_cand,
		#-----
		'jumlah'	:db_cand.count(),
		'status'	:low_status,
		'verif' 	:verif_ada,
	}
	return render(request, 'account/lihat_candidate.html', context)


@login_required(login_url='login1')
@admin_only
def tambah_candV(request):
	data_form1 = candidate_form(request.POST or None, request.FILES or None)
	data_form2 = user_create_form(request.POST or None)

	if request.method == 'POST':
		if data_form2.is_valid():
			user = data_form2.save()
			if data_form1.is_valid():
				profil = data_form1.save(commit=False)
				profil.cand_mail = user
				profil.save()
				return redirect('account:lihat_cand')
			else:
				users.objects.filter(id_user=user.id_user).delete()
				messages.info(request, 'Maaf Data Profil Tidak Valid!')
		else:
			messages.info(request, 'Maaf Data User Tidak Valid!')

	context = {
		'judul'		:'Pelamar',
		'judul_isi' :'Tambah Pelamar',
		'data1'		:data_form1,
		'data2'		:data_form2,
	}
	return render(request, 'account/formtu_tambah_cand.html', context)


@login_required(login_url='login1')
@admin_only
def ubah_candV(request, ubah_id):
	data_ubah1 = candidate.objects.get(id_candidate=ubah_id)
	data_form1 = candidate_form(request.POST or None, request.FILES or None, instance=data_ubah1)

	data_ubah2 = users.objects.get(id_user=data_ubah1.cand_mail.id_user)
	data_form2 = user_change_form(request.POST or None, instance=data_ubah2)

	if request.method == 'POST' and 'ubah_candidate' in request.POST:
		if data_form1.is_valid():
			data_form1.save()
			return redirect('account:lihat_cand')

	elif request.method == 'POST' and 'ubah_user' in request.POST:
		if data_form2.is_valid():
			olah = data_form2.save(commit=False)
			olah.is_active = True
			olah.save()
			return redirect('account:lihat_cand')

	context = {
		'judul'		:'Pelamar',
		'judul_isi'	:'Ubah Pelamar',
		'data1'		:data_form1,
		'data2'		:data_form2,
	}
	return render(request, 'account/formtu_ubah_cand.html', context)


@login_required(login_url='login1')
@admin_only
def hapus_candV(request, hapus_id):
	cand = candidate.objects.get(id_candidate=hapus_id)
	users.objects.filter(id_user=cand.cand_mail.id_user).delete()
	return redirect('account:lihat_cand')



# ---LEADER

@login_required(login_url='login1')
@leader_only
def index_leaderV(request):
	user 	  = request.user
	
	context = {
		'judul'		:'Arrava',
		'judul_isi' :'SPK - Pemilihan Pengajar',
	}
	return render(request, 'account/leader/index_leader.html', context)


@login_required(login_url='login1')
@leader_only
def detail_candV(request, det_id):
	data 	  = candidate.objects.get(id_candidate=det_id)
	data_form = candidate_form(instance=data)

	context = {
		'judul'		:'Pelamar',
		'judul_isi'	:'Detail Pelamar',
		'data1'		:data_form,
	}
	return render(request, 'account/formtu_tambah_cand.html', context)


@login_required(login_url='login1')
@leader_only
def terimaV(request, keput_id):
	candidate.objects.filter(id_candidate=keput_id).update(status='diterima')
	return redirect('dss:lihat_peringkat')


@login_required(login_url='login1')
@leader_only
def tolakV(request, keput_id):
	candidate.objects.filter(id_candidate=keput_id).update(status='ditolak')
	return redirect('dss:lihat_peringkat')



# ---PELAMAR

@login_required(login_url='login1')
@pelamar_only
def index_pelamarV(request):
	candidate  = request.user.candidate

	context = {
		'judul'		:'Arrava',
		'judul_isi' :'SPK - Pemilihan Pengajar',
	}
	return render(request, 'account/pelamar/index_pelamar.html', context)


@login_required(login_url='login1')
@pelamar_only
def profilV(request):
	candidate  = request.user.candidate
	db_verif = verify.objects.all()

	verif_ada = False
	if db_verif.exists():
		verif_ada = db_verif[0].verifikasi

	context = {
		'judul'		:'Profil',
		'judul_isi' :'Profi Data Diri ',
		'data'		:candidate,
		#---
		'verif'		:verif_ada,
	}
	return render(request, 'account/pelamar/profil.html', context)


@login_required(login_url='login1')
@pelamar_only
def ubah_profilV(request):
	candidate  = request.user.candidate
	data_form1 = profil_cand_form(request.POST or None, request.FILES or None, instance=candidate)

	user 	   = request.user
	data_form2 = user_change_form(request.POST or None, instance=user)

	if request.method == 'POST' and 'ubah_candidate' in request.POST:
		if data_form1.is_valid():
			data_form1.save()
			return redirect('account:profil')

	elif request.method == 'POST' and 'ubah_user' in request.POST:
		if data_form2.is_valid():
			olah = data_form2.save(commit=False)
			olah.is_active = True
			olah.save()
			return redirect('account:profil')

	context = {
		'judul'		:'Profil',
		'judul_isi' :'Ubah Profil',
		'data1'		:data_form1,
		'data2'		:data_form2,
	}
	return render(request, 'account/pelamar/ubah_profil.html', context)


@login_required(login_url='login1')
@pelamar_only
def hasil_keputusanV(request):
	cand 	 = request.user.candidate
	db_per	 = peringkat.objects.all()

	per_ada = True
	if db_per.exists():
		db_per = peringkat.objects.get(nama_lengkap=cand)
	else:
		per_ada = False

	context = {
		'judul'		:'Hasil Keputusan',
		'judul_isi'	:'Hasil Keputusan',
		'data'		:db_per,
		#-----
		'peringkat'	:per_ada,
	}
	return render(request, 'account/pelamar/hasil_keputusan.html', context)