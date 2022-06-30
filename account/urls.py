from django.urls import path

from .views import *

app_name = 'account'
urlpatterns = [
	path('index_admin', index_adminV, name='index_admin'),
	path('index_leader', index_leaderV, name='index_leader'),
	path('index_pelamar', index_pelamarV, name='index_pelamar'),

	path('profil', profilV, name='profil'),
	path('ubah_profil', ubah_profilV, name='ubah_profil'),

	path('lihat_user', lihat_userV, name='lihat_user'),

	path('lihat_cand', lihat_candV, name='lihat_cand'),
	path('tambah_cand', tambah_candV, name='tambah_cand'),
	path('ubah_cand/<ubah_id>', ubah_candV, name='ubah_cand'),
	path('hapus_cand/<hapus_id>', hapus_candV, name='hapus_cand'),

	path('detail_cand/<det_id>', detail_candV, name='detail_cand'),
	path('terima/<keput_id>', terimaV, name='terima'),
	path('tolak/<keput_id>', tolakV, name='tolak'),

	path('hasil_keputusan', hasil_keputusanV, name='hasil_keputusan'),
]