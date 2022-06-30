from django.db import models
from django.core import validators

from account import models as account_models
from kriteria import models as kriteria_models
from .validators import *

# Create your models here.

class peringkat(models.Model):
	id_peringkat = models.AutoField(auto_created=True, primary_key=True, serialize=False)
	nama_lengkap = models.ForeignKey(
						account_models.candidate,
						on_delete=models.CASCADE,
				 )
	nilai_akhir	 = models.FloatField(null=True)
	urutan		 = models.IntegerField(null=True)

	def __str__(self):
		return str(self.nama_lengkap)



class verify(models.Model):
	id_verify  = models.AutoField(auto_created=True, primary_key=True, serialize=False)
	verifikasi = models.BooleanField(default=False)

	def __int__(self):
		return self.id_verify