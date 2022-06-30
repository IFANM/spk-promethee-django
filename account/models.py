from django.db import models
from django.core import validators
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .validators import *

# Create your models here.

class users_manager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Masukkan email pengguna')
		if not password:
			raise ValueError('Masukkan password pengguna')

		user = self.model(
				email = self.normalize_email(email),
				
			)
		user.set_password(password)
		user.is_active = True
		user.save(using=self._db)
		return user

	def create_leader(self, email, password):
		user = self.create_user(
				email,
				password = password,
			)
		user.is_leader = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
				email,
				password = password,
			)
		user.is_staff 	  = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


 
class users(AbstractBaseUser, PermissionsMixin):
	id_user		= models.AutoField(auto_created=True, primary_key=True, serialize=False)
	email		= models.EmailField(max_length=25, unique=True, validators=[validate_email])
	is_active	= models.BooleanField(default=True)
	is_leader 	= models.BooleanField(default=False)
	is_staff 	= models.BooleanField(default=False)
	is_superuser= models.BooleanField(default=False)
	date_joined	= models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)
	last_login	= models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

	USERNAME_FIELD	= 'email'
	REQUIRED_FIELDS	= []

	objects			= users_manager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		'Does the user have a spesific permission?'
		return self.is_staff

	def has_module_perms(self, employee):
		'Does the user have permissions to view the app "app_label"'
		return self.is_staff

	def set_password(self, raw_password):
		self.password = make_password(raw_password)

	@property
	def active(self):
		'Is the user active?'
		return self.is_active

	@property
	def leader(self):
		'Is the user a leader?'
		return self.is_leader

	@property
	def staff(self):
		'Is the user a staff?'
		return self.is_staff



def increment_candidate():
	last_id = candidate.objects.all().order_by('id_candidate').last()
	if not last_id:
		return 'a' + '01'
	cand_id 	 = last_id.id_candidate
	cand_int 	 = int(cand_id[1:])
	new_cand_int = cand_int + 1
	new_cand_id  = 'a' + str(new_cand_int).zfill(2)
	return new_cand_id

class candidate(models.Model):
	JENKEL = {
		('laki-laki', 'Laki-laki'),
		('perempuan', 'Perempuan'),
	}

	STAT = {
		('seleksi', 'Seleksi'),
		('diterima', 'Diterima'),
		('ditolak', 'Ditolak'),
	}

	LUL = {
		('d1', 'D1'),
		('d2', 'D2'),
		('d3', 'D3'),
		('d4', 'D4'),
		('s1', 'S1')
	}

	id_candidate	= models.CharField(max_length=3, default=increment_candidate, primary_key=True)
	nama_depan		= models.CharField(max_length=25, null=True)
	nama_belakang	= models.CharField(max_length=25, null=True)
	jenis_kelamin	= models.CharField(max_length=25, choices=JENKEL, default='laki-laki')
	tgl_lahir		= models.DateField(blank=True, null=True)	
	no_telp			= models.CharField(max_length=13, null=True, blank=True, validators=[validators.MinLengthValidator(10)])
	alamat	 		= models.TextField(null=True, blank=True)
	foto_profil		= models.ImageField(default='default.jpg', blank=True)
	cv				= models.FileField(default='cv.pdf', blank=True)
	status			= models.CharField(max_length=25, choices=STAT, default='seleksi')
	cand_mail 		= models.OneToOneField(
							users,
							null=True,
							blank=True,
							on_delete=models.CASCADE,
							limit_choices_to={'is_leader':False, 'is_staff':False}
						)

	def __str__(self):
		return self.nama_depan + " " + self.nama_belakang