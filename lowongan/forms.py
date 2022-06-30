from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

# Create your forms here.

class lowongan_form(forms.ModelForm):
    class Meta:
        model = lowongan
        fields = {
        	'mata_pelajaran',
        	'jenjang',
        	'tgl_buka',
        	'tgl_tutup',
        }

        labels = {
        	'mata_pelajaran' :'Mata Pelajaran', 
        	'jenjang'		 :'Jenjang',
        	'tgl_buka'		 :'Tanggal Dibuka',
        	'tgl_tutup'		 :'Tanggal Ditutup',
        }

        widgets = {
        	'mata_pelajaran':forms.Select(
        		attrs={
        			'class':'form-control',
        		},
        		),
        	'jenjang':forms.Select(
        		attrs={
        			'class':'form-control',
        		},
        		),
			'tgl_buka':forms.SelectDateWidget(
				empty_label=("Tahun", "Bulan", "Hari"),
				attrs={
					'class':'custom-select col-sm-4',
				},
				),
			'tgl_tutup':forms.SelectDateWidget(
				empty_label=("Tahun", "Bulan", "Hari"),
				attrs={
					'class':'custom-select col-sm-4',
				},
				),
        }