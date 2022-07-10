from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import *

from account.models import *
from account.decorators import *

from lowongan.models import *

from kriteria.models import *
from kriteria.decorators import *

from nilai.models import *
from nilai.decorators import *

import numpy as np

# Create your views here.

# ---LEADER
@login_required(login_url='login1')
@leader_only
def cetak_peringkatV(request):
	db_per 	= peringkat.objects.all()
	db_cand = candidate.objects.all()
	db_low	= lowongan.objects.all()
	
	template_path = 'dss/leader/cetak_pimpinan.html'

	context = {
		'judul':'Cetak Peringkat',
		'tabel':db_per,
		'data' :db_low[0],
		#---
		'jmlh' :db_cand.count(),
		'today'	:datetime.now().date(),
	}

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="peringkat.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	#membuat pdf
	pisa_status = pisa.CreatePDF(
		html, dest=response)
	
	#tampilan error
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')

	return response



# ---PELAMAR
@login_required(login_url='login1')
@pelamar_only
def cetak_suratV(request, detail_id):
	db_nilai = nilai.objects.filter(nama_alternatif__id_candidate=detail_id)
	db_cand  = candidate.objects.get(id_candidate=detail_id)
	db_per 	 = peringkat.objects.get(nama_lengkap=db_cand)
	db_low	 = lowongan.objects.all()
	
	template_path = 'dss/pelamar/cetak_pelamar.html'

	context = {
		'judul'	:'Cetak Surat',
		'tabel'	:db_nilai,
		'data1'	:db_cand,
		'data2' :db_per,
		'data3' :db_low[0],
		#---
		'today'	:datetime.now().date()
	}

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="surat.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	#membuat pdf
	pisa_status = pisa.CreatePDF(
		html, dest=response)
	
	#tampilan error
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')

	return response



# ---PROMETHEE
@login_required(login_url='login1')
@admin_leader
@alternatif_ada
@kriteria_ada
@nilai_lengkap
def lihat_hasil_akhirV(request):
	dbp   = peringkat.objects.all()
	dbve  = verify.objects.all()
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')
	dbk_v1 = kriteria.objects.order_by('id_kriteria').values_list('id_kriteria', 'nama_kriteria')
	dbk_v2 = kriteria.objects.order_by('id_kriteria').values_list(
		'kaidah', 'tipe_preferensi', 'parameter_p', 'parameter_q'
		)

	#---GET--- Tabel Evaluasi Data
	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_a = np.reshape(a, (dbc.count(), dbk.count()))

	#membulatkan nilai pada array
	ax = np.array([])
	for i in range(len(arr_a)):
		for j in range(len(arr_a[i])):
			if i == 0:
				ax = np.append(ax, np.array(arr_a[j][i]))
			else:
				ubah = "{:.0f}".format(arr_a[j][i])
				ax = np.append(ax, np.array(ubah))

	arr_nilai = np.reshape(ax, (dbc.count(), dbk.count()))
	
	#mengubah ke tipe data String
	arr_nilai_s = arr_nilai.astype('U32')

	#mengubah db.kriteria1 ke array
	b1 = np.array([])
	for i in range(len(dbk_v1)):
		for j in dbk_v1[i]:
			b1 = np.append(b1, np.array(j))

	arr_kriteria1 = np.reshape(b1, (dbk.count(), 2))

	#mengubah db.kriteria2 ke array
	b2 = np.array([])
	for i in range(len(dbk_v2)):
		for j in dbk_v2[i]:
			b2 = np.append(b2, np.array(j))

	arr_kriteria2 = np.reshape(b2, (dbk.count(), 4))

	#menggabungkan 3 array
	gabung = np.concatenate((arr_kriteria1, arr_nilai_s, arr_kriteria2), axis=1)

	#cek tb_peringkat ada
	per_ada = True
	if dbp.exists():
		per_ada = True
	else:
		per_ada = False

	#cek tb_verify ada
	verif_ada = False
	if dbve.exists():
		verif_ada = dbve[0].verifikasi
	else:
		baru = verify(verifikasi = False)
		baru.save()
		verif_ada = dbve[0].verifikasi

	#---POST--- Verifikasi
	if request.method == 'POST' and 'verifikasi' in request.POST:
		dbve.update(verifikasi = True)
		return redirect('dss:lihat_hasil_akhir')

	context = {
		'judul'		:'Hasil Akhir',
		'judul_isi'	:'Tabel Verifikasi Data Nilai',
		'matriks'	:gabung,
		#-----
		'alt'		:dbc,
		'jmlh'		:dbc.count(),
		'peringkat' :per_ada,
		'verifikasi':verif_ada,
	}
	return render(request, 'dss/lihat_hasil_akhir.html', context)


@login_required(login_url='login1')
@leader_only
def cek_ulangV(request):
	verify.objects.all().update(verifikasi = False)
	return redirect('dss:lihat_hasil_akhir')


@login_required(login_url='login1')
@leader_only
def hitung_peringkatV(request):
	dbp   = peringkat.objects.all()
	dbve  = verify.objects.all()
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	if request.method == 'POST' and 'hitung' in request.POST:
		#mengubah db.nilai ke array
		a = np.array([])
		for i in range(len(dbn_v)):
			a = np.append(a, np.array(dbn_v[i]))

		arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

		#membandingkan alternatif
		b = np.array([])
		for i in range(len(dbc)):
			for j in range(len(dbc)):
				if i == j:
					pass
				else:
					b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

		arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

		#membandingkan nilai array matriks
		c = np.array([])
		d = np.array([])
		for i in range(len(dbk)):
			for j in range(len(dbc)):
				for k in range(len(dbc)):
					if j == k:
						pass
					else:
						if dbk[i].kaidah == 'minimasi':
							if arr_nilai[j][i] > arr_nilai[k][i]:
								pref = 0
							else:
								if dbk[i].tipe_preferensi == 'usual':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= 0:
										pref = 0
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'quasi':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'linear':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= 0:
										pref = 0
									elif selisih > 0 and selisih <= dbk[i].parameter_p:
										pref = selisih / dbk[i].parameter_p
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'level':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
										pref = 0.5
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'linear-quasi':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
										pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
									else:
										pref = 1
									
						else:
							if arr_nilai[j][i] > arr_nilai[k][i]:
								if dbk[i].tipe_preferensi == 'usual':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= 0:
										pref = 0
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'quasi':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'linear':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= 0:
										pref = 0
									elif selisih > 0 and selisih <= dbk[i].parameter_p:
										pref = selisih / dbk[i].parameter_p
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'level':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
										pref = 0.5
									else:
										pref = 1
									
								if dbk[i].tipe_preferensi == 'linear-quasi':
									
									selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
									if selisih <= dbk[i].parameter_q:
										pref = 0
									elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
										pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
									else:
										pref = 1
									
							else:
								pref = 0
							
						c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))
						d = np.append(d, np.array(pref))

		#mengubah ke bentuk array 2D
		arr_ip 		 = np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
		
		#menghitung total ip dan mengubah ke bentuk array 2D
		e 			 = (1/dbk.count())*(np.sum(arr_ip, axis=0))
		arr_total_ip = np.reshape(e, ( dbc.count()*(dbc.count()-1), 1 ))

		#membuat list id alternatif
		f = np.array([])
		for i in range(len(dbc)):
			f = np.append(f, np.array(dbc[i].id_candidate))

		arr_alt = np.reshape(f, ( dbc.count(), 1 ))

		#membuat matriks total nilai
		index_totip = 0
		g = np.zeros((dbc.count(), dbc.count()))
		for i in range(len(dbc)):
			for j in range(len(dbc)):
				if i == j:
					pass
				else:
					g[i][j] = arr_total_ip[index_totip]
					index_totip += 1

		
		#menghitung leaving flow
		arr_lf = np.sum(g, axis=1, keepdims=True) / (dbc.count()-1)

		#menghitung entering flow
		arr_ef = np.sum(g.T, axis=1, keepdims=True) / (dbc.count()-1)

		#menghitung net flow
		arr_net = arr_lf - arr_ef

		#membuat list nama alternatif
		g = np.array([])
		for i in range(len(dbc)):
			g = np.append(g, np.array(dbc[i].nama_depan + ' ' + dbc[i].nama_belakang))

		#sorting ranking
		rank = np.array([], dtype=np.int)
		net_flow = np.reshape(arr_net, (dbc.count()))
		for i in range(len(dbc)):
			rank = np.append(rank, np.array(int(i+1)))
			for j in range(len(dbc)):
				if j > i:
					if net_flow[i] < net_flow[j]:
						tmp_alt 	= f[i]
						tmp_nama	= g[i]
						tmp_arr_net = net_flow[i]

						f[i]		= f[j]
						g[i]		= g[j]
						net_flow[i]	= net_flow[j]

						f[j]		= tmp_alt
						g[j]		= tmp_nama
						net_flow[j]	= tmp_arr_net

		#menyamakan array 2D
		f 		 = np.reshape(f, (dbc.count(), 1))
		g 		 = np.reshape(g, (dbc.count(), 1))
		net_flow = np.reshape(net_flow, (dbc.count(), 1))
		net_flow = net_flow.astype('float')
		rank 	 = np.reshape(rank, (dbc.count(), 1))

		#menggabungkan array
		gabung_per = np.concatenate((f, g, net_flow, rank), axis=1)

		if dbp.exists():
			dbp.delete()
		else:
			for data in gabung_per:
				nama_cand = candidate.objects.get(id_candidate=data[0])
				sim_per = peringkat(
					id_peringkat = None,
					nama_lengkap = nama_cand,
					nilai_akhir  = "{:.6f}".format(data[2].astype('float')),
					urutan		 = data[3].astype('int'),
					)
				sim_per.save()
			return redirect('dss:lihat_peringkat')



@login_required(login_url='login1')
@leader_only
def lihat_peringkatV(request):
	db_per 	   = peringkat.objects.all()
	cek_status = peringkat.objects.filter(nama_lengkap__status='seleksi')

	seleksi = True
	if cek_status.exists():
		seleksi = True
	else:
		seleksi = False

	context = {
		'judul'		:'Hasil Akhir',
		'judul_isi'	:'Peringkat Hasil Perhitungan',
		'tabel'		:db_per,
		#---
		'seleksi'	:seleksi,
	}
	return render(request, 'dss/lihat_peringkat.html', context)


@login_required(login_url='login1')
@leader_only
def hapus_peringkatV(request):
	peringkat.objects.all().delete()
	candidate.objects.all().update(status='seleksi')
	return redirect('dss:lihat_hasil_akhir')



#Perhitungan
@login_required(login_url='login1')
@leader_only
def lihat_selisihV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))

	arr_selisih   = np.reshape(c, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	arr_selisih_s = arr_selisih.astype('U32')

	gabung = np.concatenate((arr_banding_alternatif, arr_selisih_s.T), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Selisih Nilai Alternatif',
		'matriks'	:gabung,
		#-----
		'krit'		:dbk,
		'jmlh'		:dbk.count(),
	}
	return render(request, 'dss/perhitungan/lihat_selisih.html', context)


@login_required(login_url='login1')
@leader_only
def lihat_prefV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					if dbk[i].kaidah == 'minimasi':
						if arr_nilai[j][i] > arr_nilai[k][i]:
							pref = 0
						else:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
					else:
						if arr_nilai[j][i] > arr_nilai[k][i]:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
						else:
							pref = 0
						
					d = np.append(d, np.array(pref))

	arr_ip 	= np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	arr_ip_s	= arr_ip.astype('U32')

	gabung = np.concatenate((arr_banding_alternatif, arr_ip_s.T), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Nilai Preferensi',
		'matriks'	:gabung,
		#-----
		'krit'		:dbk,
		'jmlh'		:dbk.count(),
	}
	return render(request, 'dss/perhitungan/lihat_pref.html', context)
	

@login_required(login_url='login1')
@leader_only
def lihat_total_ipV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					if dbk[i].kaidah == 'minimasi':
						if arr_nilai[j][i] > arr_nilai[k][i]:
							pref = 0
						else:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
					else:
						if arr_nilai[j][i] > arr_nilai[k][i]:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
						else:
							pref = 0
						
					c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))
					d = np.append(d, np.array(pref))

	#mengubah ke bentuk array 2D
	arr_ip 		 = np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	#menghitung total ip dan mengubah ke bentuk array 2D
	e 			 = (1/dbk.count())*(np.sum(arr_ip, axis=0))
	arr_total_ip = np.reshape(e, ( 1, dbc.count()*(dbc.count()-1)))

	#mengubah tipe data array
	arr_total_ip_s = arr_total_ip.astype('U32')

	#menggabungkan 2 array 2D
	gabung = np.concatenate((arr_banding_alternatif, arr_total_ip_s.T), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Total Nilai Indeks Preferensi',
		'matriks'	:gabung,
		#-----
		'krit'		:dbk,
		'jmlh'		:dbk.count(),
	}
	return render(request, 'dss/perhitungan/lihat_total_ip.html', context)


@login_required(login_url='login1')
@leader_only
def lihat_leavingfV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					if dbk[i].kaidah == 'minimasi':
						if arr_nilai[j][i] > arr_nilai[k][i]:
							pref = 0
						else:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
					else:
						if arr_nilai[j][i] > arr_nilai[k][i]:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
						else:
							pref = 0
						
					c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))
					d = np.append(d, np.array(pref))

	#mengubah ke bentuk array 2D
	arr_ip 		 = np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	#menghitung total ip dan mengubah ke bentuk array 2D
	e 			 = (1/dbk.count())*(np.sum(arr_ip, axis=0))
	arr_total_ip = np.reshape(e, ( dbc.count()*(dbc.count()-1), 1 ))

	#mengubah tipe data array

	#membuat list alternatif
	f = np.array([])
	for i in range(len(dbc)):
		f = np.append(f, np.array(dbc[i].id_candidate))

	arr_alt = np.reshape(f, ( dbc.count(), 1 ))

	#membuat matriks total nilai
	index_totip = 0
	g = np.zeros((dbc.count(), dbc.count()))
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				g[i][j] = arr_total_ip[index_totip]
				index_totip += 1

	#menghitung leaving flow
	arr_lf = np.sum(g, axis=1, keepdims=True) / (dbc.count()-1)

	#mengubah tipe data
	arr_lf = arr_lf.astype('float')

	#menggabungkan array 2D
	gabung = np.concatenate((arr_alt, g, arr_lf), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Leaving Flow',
		'matriks'	:gabung,
		#-----
		'alt'		:dbc,
	}
	return render(request, 'dss/perhitungan/lihat_leavingf.html', context)


@login_required(login_url='login1')
@leader_only
def lihat_enteringfV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					if dbk[i].kaidah == 'minimasi':
						if arr_nilai[j][i] > arr_nilai[k][i]:
							pref = 0
						else:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
					else:
						if arr_nilai[j][i] > arr_nilai[k][i]:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
						else:
							pref = 0
						
					c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))
					d = np.append(d, np.array(pref))

	#mengubah ke bentuk array 2D
	arr_ip 		 = np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	#menghitung total ip dan mengubah ke bentuk array 2D
	e 			 = (1/dbk.count())*(np.sum(arr_ip, axis=0))
	arr_total_ip = np.reshape(e, ( dbc.count()*(dbc.count()-1), 1 ))

	#mengubah tipe data array

	#membuat list alternatif
	f = np.array([])
	for i in range(len(dbc)):
		f = np.append(f, np.array(dbc[i].id_candidate))

	arr_alt = np.reshape(f, ( dbc.count(), 1 ))

	#membuat matriks total nilai
	index_totip = 0
	g = np.zeros((dbc.count(), dbc.count()))
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				g[i][j] = arr_total_ip[index_totip]
				index_totip += 1

	#menghitung entering flow
	arr_ef = np.sum(g.T, axis=1, keepdims=True) / (dbc.count()-1)

	#mengubah tipe data
	arr_ef = arr_ef.astype('float')

	#menggabungkan array 2D
	gabung = np.concatenate((arr_alt, g.T, arr_ef), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Entering Flow',
		'matriks'	:gabung,
		#-----
		'alt'		:dbc,
	}
	return render(request, 'dss/perhitungan/lihat_enteringf.html', context)


@login_required(login_url='login1')
@leader_only
def lihat_netfV(request):
	dbc   = candidate.objects.order_by('id_candidate')
	dbk   = kriteria.objects.order_by('id_kriteria')
	dbn_v = nilai.objects.order_by('nama_alternatif', 'nama_kriteria').values_list('nilai')

	#mengubah db.nilai ke array
	a = np.array([])
	for i in range(len(dbn_v)):
		a = np.append(a, np.array(dbn_v[i]))

	arr_nilai = np.reshape(a, (dbc.count(), dbk.count()))

	#membandingkan alternatif
	b = np.array([])
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				b = np.append(b, np.array(dbc[i].id_candidate + ' - ' + dbc[j].id_candidate))

	arr_banding_alternatif = np.reshape(b, (dbc.count()*(dbc.count()-1), 1))

	#membandingkan nilai array matriks
	c = np.array([])
	d = np.array([])
	for i in range(len(dbk)):
		for j in range(len(dbc)):
			for k in range(len(dbc)):
				if j == k:
					pass
				else:
					if dbk[i].kaidah == 'minimasi':
						if arr_nilai[j][i] > arr_nilai[k][i]:
							pref = 0
						else:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
					else:
						if arr_nilai[j][i] > arr_nilai[k][i]:
							if dbk[i].tipe_preferensi == 'usual':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= 0:
									pref = 0
								elif selisih > 0 and selisih <= dbk[i].parameter_p:
									pref = selisih / dbk[i].parameter_p
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'level':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = 0.5
								else:
									pref = 1
								
							if dbk[i].tipe_preferensi == 'linear-quasi':
								
								selisih = abs(arr_nilai[j][i]-arr_nilai[k][i])
								if selisih <= dbk[i].parameter_q:
									pref = 0
								elif selisih > dbk[i].parameter_q and selisih <= dbk[i].parameter_p:
									pref = (selisih-dbk[i].parameter_q)/(dbk[i].parameter_p-dbk[i].parameter_q)
								else:
									pref = 1
								
						else:
							pref = 0
						
					c = np.append(c, np.array(arr_nilai[j][i]-arr_nilai[k][i]))
					d = np.append(d, np.array(pref))

	#mengubah ke bentuk array 2D
	arr_ip 		 = np.reshape(d, ( dbk.count(), dbc.count()*(dbc.count()-1) ))
	
	#menghitung total ip dan mengubah ke bentuk array 2D
	e 			 = (1/dbk.count())*(np.sum(arr_ip, axis=0))
	arr_total_ip = np.reshape(e, ( dbc.count()*(dbc.count()-1), 1 ))

	#mengubah tipe data array

	#membuat list alternatif
	f = np.array([])
	for i in range(len(dbc)):
		f = np.append(f, np.array(dbc[i].id_candidate))

	arr_alt = np.reshape(f, ( dbc.count(), 1 ))

	#membuat matriks total nilai
	index_totip = 0
	g = np.zeros((dbc.count(), dbc.count()))
	for i in range(len(dbc)):
		for j in range(len(dbc)):
			if i == j:
				pass
			else:
				g[i][j] = arr_total_ip[index_totip]
				index_totip += 1

	#menghitung leaving flow
	arr_lf = np.sum(g, axis=1, keepdims=True) / (dbc.count()-1)

	#menghitung entering flow
	arr_ef = np.sum(g.T, axis=1, keepdims=True) / (dbc.count()-1)

	#menghitung net flow
	arr_net = arr_lf - arr_ef

	#mengubah tipe data
	arr_lf  = arr_lf.astype('float')
	arr_ef  = arr_ef.astype('float')
	arr_net = arr_net.astype('float')

	#menggabungkan array 2D
	gabung = np.concatenate((arr_alt, arr_lf, arr_ef, arr_net), axis=1)

	context = {
		'judul'		:'Perhitungan',
		'judul_isi'	:'Menghitung Net Flow',
		'matriks'	:gabung,
		#-----
		'alt'		:dbc,
	}
	return render(request, 'dss/perhitungan/lihat_netf.html', context)
