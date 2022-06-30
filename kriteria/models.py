from django.db import models

# Create your models here.

def increment_kriteria():
	last_id = kriteria.objects.all().order_by('id_kriteria').last()
	if not last_id:
		return 'k' + '01'
	krit_id		 = last_id.id_kriteria
	krit_int	 = int(krit_id[1:])
	new_krit_int = krit_int + 1
	new_krit_id  = 'k' + str(new_krit_int).zfill(2)
	return new_krit_id

class kriteria(models.Model):
	KAID = {
		('maksimasi', 'Maksimasi'),
		('minimasi', 'Minimasi'),
	}

	TIPREF = {
		('usual', 'I: Usual'),
		('quasi', 'II: Quasi'),
		('linear', 'III: Linear'),
		('level', 'IV: Level'),
		('linear-quasi', 'V: Linear-Quasi'),
	}

	id_kriteria		= models.CharField(max_length=3, default=increment_kriteria, primary_key=True)
	nama_kriteria	= models.CharField(max_length=25, null=True)
	kaidah			= models.CharField(max_length=10, null=True, choices=KAID)
	tipe_preferensi	= models.CharField(max_length=25, null=True, choices=TIPREF)
	parameter_p		= models.FloatField(null=True, default=0)
	parameter_q		= models.FloatField(null=True, default=0)
	keterangan		= models.CharField(max_length=75, null=True, blank=True)

	def __str__(self):
		return self.nama_kriteria