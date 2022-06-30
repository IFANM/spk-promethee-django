from django.urls import path

from .views import *

app_name = 'kriteria'
urlpatterns = [
	path('', lihat_kritV, name='lihat_krit'),
	path('tambah_krit', tambah_kritV, name='tambah_krit'),
	path('ubah_krit/<ubah_id>', ubah_kritV, name='ubah_krit'),
	path('hapus_krit/<hapus_id>', hapus_kritV, name='hapus_krit'),
]