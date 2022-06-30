from django.urls import path

from .views import *

app_name = 'lowongan'
urlpatterns = [
	path('', lihat_lowV, name='lihat_low'),
	path('tambah_low', tambah_lowV, name='tambah_low'),
	path('ubah_low/<int:ubah_id>', ubah_lowV, name='ubah_low'),
	path('hapus_low/<int:hapus_id>', hapus_lowV, name='hapus_low'),
]