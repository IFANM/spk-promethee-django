from django import forms

from .models import *

# Create your forms here.

class kriteria_form(forms.ModelForm):
    class Meta:
        model = kriteria
        fields = {
        	'id_kriteria',
            'nama_kriteria',
        	'kaidah',
        	'tipe_preferensi',
        	'parameter_p',
        	'parameter_q',
            'keterangan',
        }

        labels = {
        	'id_kriteria'      :'ID',
            'nama_kriteria'    :'Nama Kriteria',
        	'kaidah'           :'Kaidah',
        	'tipe_preferensi'  :'Tipe Preferensi',
        	'parameter_p'      :'Parameter P',
        	'parameter_q'      :'Parameter Q',
            'keterangan'       :'Keterangan',
        }

        widgets = {
            'id_kriteria':forms.TextInput(
                attrs={
                    'class':'form-control',
                },
                ),
            'nama_kriteria':forms.TextInput(
                attrs={
                    'class':'form-control',
                },
                ),
            'kaidah':forms.Select(
                attrs={
                    'class':'form-control',
                },
                ),
            'tipe_preferensi':forms.Select(
                attrs={
                    'class':'form-control',
                },
                ),
            'parameter_p':forms.NumberInput(
                attrs={
                    'class':'form-control',
                },
                ),
            'parameter_q':forms.NumberInput(
                attrs={
                    'class':'form-control',
                },
                ),
            'keterangan':forms.TextInput(
                attrs={
                    'class':'form-control',
                },
                ),
        }