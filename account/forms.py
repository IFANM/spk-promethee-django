from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

# Create your forms here.

users = get_user_model()

class user_create_form(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
			attrs={'class':'form-control', 'placeholder':'Masukkan Password',},
		))
	password2 = forms.CharField(label='Konfirmasi Password', widget=forms.PasswordInput(
			attrs={'class':'form-control', 'placeholder':'Masukkan Ulang Password',},
		))

	class Meta:
		model  = users
		fields = {
			'email',
			'password1',
			'password2',
		}

		labels = {
			'email'		:'Email',
		}

		widgets = {
			'email':forms.EmailInput(
				attrs={
					'class':'form-control',
					'placeholder':'abcdefg@gmail.com',
				},
				),
		}

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs	  = users.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('Email Sudah Digunakan')
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password2 and password1 and password2 != password1:
			raise forms.ValidationError('Password Tidak Sama')
		return password2

	def save(self, commit=True):
		user = super(user_create_form, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user



class user_change_form(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	def __init__(self, *args, **kwargs):
		super(user_change_form, self).__init__(*args, **kwargs)
		f = self.fields.get('user_permissions', None)
		if f is not None:
			f.queryset = f.queryset.select_related('content_type')

	def clean_password(self):
	# Regardless of what the user provides, return the initial value.
	# This is done here, rather than on the field, because the
	# field does not have access to the initial value
		return self.initial["password"]

	class Meta:
		model  = users
		fields = {
			'email',
			'password'
		}

		labels = {
			'email'		:'Email',
		}

		widgets	= {
			'email':forms.EmailInput(
				attrs={
					'class':'form-control',
					'placeholder':'abcdefg@gmail.com',
				},
				),
		}



class candidate_form(forms.ModelForm):
    class Meta:
        model = candidate
        fields = {
        	'id_candidate',
        	'nama_depan',
        	'nama_belakang',
        	'jenis_kelamin',
        	'tgl_lahir',
        	'no_telp',
        	'alamat',
        	'foto_profil',
        	'cv',
        	'cand_mail',
        }

        labels = {
        	'id_candidate'	:'ID',
        	'nama_depan'	:'Nama Depan',
			'nama_belakang'	:'Nama Belakang',
			'jenis_kelamin'	:'Jenis Kelamin',
			'tgl_lahir'		:'Tanggal Lahir',	
			'no_telp'		:'Nomor Telepon',
			'alamat'		:'Alamat',
			'foto_profil'	:'Foto Profil',
        	'cv'			:'Curiculum Vitae',
			'cand_mail'		:'Email',
        }

        widgets = {
        	'id_candidate':forms.TextInput(
        		attrs={
        			'class':'form-control',
        		},
        		),
        	'nama_depan':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Nama Depan Anda',
					'oninvalid':'this.setCustomValidity("Silahkan Isi Dulu")',
					'oninput':'setCustomValidity("")',
				},
				),
			'nama_belakang':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Nama Belakang Anda',
					'oninvalid':'this.setCustomValidity("Silahkan Isi Dulu")',
					'oninput':'setCustomValidity("")',
				},
				),
			'jenis_kelamin':forms.RadioSelect(
				attrs={
					'class':'custom-control-input',
				},
				),
			'tgl_lahir':forms.SelectDateWidget(
				empty_label=("Tahun", "Bulan", "Hari"),
				years=range(1990,2010),
				attrs={
					'class':'custom-select col-md-4 mb3',
					'required':'',
				},
				),
			'no_telp':forms.NumberInput(
				attrs={
					'class':'form-control',
					'placeholder':'08987654321',
				},
				),
			'alamat':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Alamat Rumah Anda',
				},
				),
			'foto_profil':forms.ClearableFileInput(),
			'cv':forms.ClearableFileInput(),
			'cand_mail':forms.Select(
				attrs={
					'class':'form-control',
					'placeholder':'abcdefg@gmail.com',
				},
				),
        }



class profil_cand_form(forms.ModelForm):
    class Meta:
        model = candidate
        fields = {
        	'id_candidate',
        	'nama_depan',
        	'nama_belakang',
        	'jenis_kelamin',
        	'tgl_lahir',
        	'no_telp',
        	'alamat',
        	'foto_profil',
        	'cv',
        }

        labels = {
        	'id_candidate'	:'ID',
        	'nama_depan'	:'Nama Depan',
			'nama_belakang'	:'Nama Belakang',
			'jenis_kelamin'	:'Jenis Kelamin',
			'tgl_lahir'		:'Tanggal Lahir',	
			'no_telp'		:'Nomor Telepon',
			'alamat'		:'Alamat',
			'foto_profil'	:'Foto Profil',
			'cv'			:'Curiculum Vitae',
        }

        widgets = {
        	'id_candidate':forms.TextInput(
        		attrs={
        			'class':'form-control',
        			'readonly':'readonly',
        		},
        		),
        	'nama_depan':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Nama Depan Anda',
					'oninvalid':'this.setCustomValidity("Silahkan Isi Dulu")',
					'oninput':'setCustomValidity("")',
				},
				),
			'nama_belakang':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Nama Belakang Anda',
					'oninvalid':'this.setCustomValidity("Silahkan Isi Dulu")',
					'oninput':'setCustomValidity("")',
				},
				),
			'jenis_kelamin':forms.RadioSelect(
				attrs={
					'class':'custom-control-input',
				},
				),
			'tgl_lahir':forms.SelectDateWidget(
				empty_label=("Tahun", "Bulan", "Hari"),
				years=range(1990,2010),
				attrs={
					'class':'custom-select col-md-4 mb3',
					'required':'',
				},
				),
			'no_telp':forms.NumberInput(
				attrs={
					'class':'form-control',
					'placeholder':'08987654321',
				},
				),
			'alamat':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Isi Alamat Rumah Anda',
				},
				),
			'foto_profil':forms.ClearableFileInput(),
			'cv':forms.ClearableFileInput(),
        }