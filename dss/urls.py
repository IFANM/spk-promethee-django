from django.urls import path

from .views import *

app_name = 'dss'
urlpatterns = [
	path('cetak_peringkat', cetak_peringkatV, name='cetak_peringkat'),
	path('cetak_surat/<detail_id>', cetak_suratV, name='cetak_surat'),

	path('lihat_hasil_akhir', lihat_hasil_akhirV, name='lihat_hasil_akhir'),
	path('cek_ulang', cek_ulangV, name='cek_ulang'),

	path('hitung_peringkat', hitung_peringkatV, name='hitung_peringkat'),
	path('lihat_peringkat', lihat_peringkatV, name='lihat_peringkat'),
	path('hapus_peringkat', hapus_peringkatV, name='hapus_peringkat'),

	path('lihat_selisih', lihat_selisihV, name='lihat_selisih'),
	path('lihat_pref', lihat_prefV, name='lihat_pref'),
	path('lihat_total_ip', lihat_total_ipV, name='lihat_total_ip'),
	path('lihat_enteringf', lihat_enteringfV, name='lihat_enteringf'),
	path('lihat_leavingf', lihat_leavingfV, name='lihat_leavingf'),
	path('lihat_netf', lihat_netfV, name='lihat_netf'),
]