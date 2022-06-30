from django.db import models
from django.core import validators

from account import models as account_models
from kriteria import models as kriteria_models

# Create your models here.

class nilai(models.Model):
	id_nilai		= models.AutoField(auto_created=True, primary_key=True, serialize=False)
	nama_alternatif	= models.ForeignKey(
						account_models.candidate,
						on_delete=models.CASCADE,
					)
	nama_kriteria	= models.ForeignKey(
						kriteria_models.kriteria,
						on_delete=models.CASCADE,
					)
	nilai 			= models.FloatField(null=True)

	def __str__(self):
		return str(self.nama_alternatif)