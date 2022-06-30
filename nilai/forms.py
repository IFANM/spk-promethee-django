from django import forms

from .models import *

# Create your forms here.

class tambah_nilai_form(forms.ModelForm):
    class Meta:
        model = nilai
        fields = {
            'nama_alternatif',
            'nama_kriteria',
            'nilai',
        }

        labels = {
            'nama_alternatif':'Nama Alternatif',
            'nama_kriteria'  :'Nama Kriteria',
            'nilai'	         :'Nilai',
        }

        widgets = {
            'nama_alternatif':forms.Select(
                attrs={
                    'class':'form-control',
                },
                ),
            'nama_kriteria':forms.Select(
                attrs={
                    'class':'form-control',
                    'onchange':'select_ket_krit(this);',
                },
                ),
            'nilai':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':'0',
                    'max':'100',
                    'step':'1',
                },
                ),
        }



class ubah_nilai_form(forms.ModelForm):
    class Meta:
        model = nilai
        fields = {
            'nama_alternatif',
            'nama_kriteria',
            'nilai',
        }

        labels = {
            'nama_alternatif':'Nama Alternatif',
            'nama_kriteria'  :'Nama Kriteria',
            'nilai'          :'Nilai',
        }

        widgets = {
            'nama_alternatif':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly',
                },
                ),
            'nama_kriteria':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly',
                },
                ),
            'nilai':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':'0',
                    'max':'100',
                    'step':'any',
                },
                ),
        }