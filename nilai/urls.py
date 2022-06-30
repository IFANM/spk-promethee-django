from django.urls import path

from .views import *

app_name = 'nilai'
urlpatterns = [
	path('', lihat_nilaiV, name='lihat_nilai'),
	path('tambah_nilai', tambah_nilaiV, name='tambah_nilai'),
	path('ubah_nilai/<ubah_id>', ubah_nilaiV, name='ubah_nilai'),
	path('hapus_nilai<hapus_id>', hapus_nilaiV, name='hapus_nilai'),

	path('detail_nilai/<detail_id>', detail_nilaiV, name='detail_nilai'),
]