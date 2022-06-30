from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decorators import *

from account.models import *
from account.decorators import *

from dss.models import *

from kriteria.models import *
from kriteria.decorators import *

import numpy as np

# Create your views here.

# ---ADMIN
# Nilai Admin-Leader
@login_required(login_url='login1')
@admin_leader
@alternatif_ada
@kriteria_ada
def lihat_nilaiV(request):
	db_nilai = nilai.objects.order_by('nama_alternatif', 'nama_kriteria')
	db_cand  = candidate.objects.order_by('id_candidate')
	db_krit  = kriteria.objects.order_by('id_kriteria')
	db_verif = verify.objects.all()

	verif_ada = False
	if db_verif.exists():
		verif_ada = db_verif[0].verifikasi

	context = {
		'judul'		:'Nilai',
		'judul_isi' :'Nilai Pelamar Berdasarkan Setiap Kriteria',
		'tabel'		:db_nilai,
		#---
		'jmlh_nilai':db_nilai.count(),
		'jmlh_data'	:db_cand.count() * db_krit.count(),
		'kurang'	:(db_cand.count() * db_krit.count()) - db_nilai.count(),
		'verif'		:verif_ada,
	}
	return render(request, 'nilai/lihat_nilai.html', context)


@login_required(login_url='login1')
@admin_only
def tambah_nilaiV(request):
	dk01 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k01')
	dk02 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k02')
	dk03 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k03')
	dk04 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k04')
	dk05 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k05')

	data_form = tambah_nilai_form(request.POST or None)
	if request.method == 'POST':
		if data_form.is_valid():
			row = nilai.objects.filter(nama_alternatif=request.POST['nama_alternatif'], nama_kriteria=request.POST['nama_kriteria'])
			if row.exists():
				messages.info(request, 'Maaf Data Sudah Dipakai!')
			else:
				data_form.save()
				return redirect('nilai:lihat_nilai')

	context = {
		'judul'		:'Nilai',
		'judul_isi'	:'Tambah Nilai',
		'data'		:data_form,
		#---
		'dk01'		:dk01,
		'dk02'		:dk02,
		'dk03'		:dk03,
		'dk04'		:dk04,
		'dk05'		:dk05,
	}
	return render(request, 'nilai/formtu_nilai_tambah.html', context)


@login_required(login_url='login1')
@admin_only
def ubah_nilaiV(request, ubah_id):
	dk01 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k01')
	dk02 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k02')
	dk03 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k03')
	dk04 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k04')
	dk05 = kriteria.objects.values_list('keterangan', flat=True).get(id_kriteria='k05')

	data_ubah 	  = nilai.objects.get(id_nilai=ubah_id)
	data_form = ubah_nilai_form(request.POST or None, instance=data_ubah)
	if request.method == 'POST':
		if data_form.is_valid():
			data_form.save()
			return redirect('nilai:lihat_nilai')

	context = {
		'judul'		:'Nilai',
		'judul_isi'	:'Ubah Nilai',
		'data'		:data_form,
		#---
		'dk01'		:dk01,
		'dk02'		:dk02,
		'dk03'		:dk03,
		'dk04'		:dk04,
		'dk05'		:dk05,
	}
	return render(request, 'nilai/formtu_nilai_ubah.html', context)


@login_required(login_url='login1')
@admin_only
def hapus_nilaiV(request, hapus_id):
	nilai.objects.filter(id_nilai=hapus_id).delete()
	return redirect('nilai:lihat_nilai')



# ---LEADER
# Detail_Nilai Leader-Pelamar
@login_required(login_url='login1')
@leader_pelamar
def detail_nilaiV(request, detail_id):
	db_nilai = nilai.objects.filter(nama_alternatif__id_candidate=detail_id)
	cand 	 = candidate.objects.get(id_candidate=detail_id)

	if request.user.is_leader == True:
		judul = 'Peringkat'
	else:
		judul = 'Hasil Keputusan'

	context = {
		'judul'		:judul,
		'judul_isi'	:'Detail Nilai',
		'tabel'		:db_nilai,
		'cand'		:cand,
	}
	return render(request, 'nilai/lihat_detail.html', context)