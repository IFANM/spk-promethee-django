from django.db import models
from django.utils import timezone

# Create your models here.

class lowongan(models.Model):
	MAPEL = {
		('matematika', 'Matematika'),
		('b.indonesia', 'B.Indonesia'),
		('b.inggris', 'B.Inggris'),
		('ipa', 'IPA'),
		('ips', 'IPS'),
	}

	JENJ = {
		('tk', 'TK'),
		('sd', 'SD'),
		('smp', 'SMP'),
		('sma', 'SMA'),
	}

	STAT = {
		('dibuka', 'Dibuka'),
		('ditutup', 'Ditutup'),
	}

	id_lowongan	   = models.AutoField(auto_created=True, primary_key=True, serialize=False)
	mata_pelajaran = models.CharField(max_length=25, choices=MAPEL, default='matematika')
	jenjang		   = models.CharField(max_length=10, choices=JENJ, default='sd')
	status		   = models.CharField(max_length=10, choices=STAT, default='ditutup')
	tgl_buka	   = models.DateField(null=True, default=timezone.now)
	tgl_tutup	   = models.DateField(null=True, default=timezone.now)

	def __str__(self):
		return self.mata_pelajaran