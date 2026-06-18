from django import forms
from .models import Perawatan, Aset


class AsetForm(forms.ModelForm):
    class Meta:
        model = Aset
        fields = ['kode_aset', 'nama_kendaraan', 'jenis', 'km_terakhir']
        widgets = {
            'kode_aset': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: TRK-001'}),
            'nama_kendaraan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Truk Hino 500'}),
            'jenis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Truk'}),
            'km_terakhir': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 15000'}),
        }
        labels = {
            'kode_aset': 'Kode Aset',
            'nama_kendaraan': 'Nama Kendaraan',
            'jenis': 'Jenis',
            'km_terakhir': 'KM Terakhir',
        }

class PerawatanForm(forms.ModelForm):
    class Meta:
        model = Perawatan
        fields = [
            'aset',
            'jenis_perawatan',
            'tanggal',
            'km_saat_servis',
            'catatan',
            'dicatat_oleh',
        ]
        widgets = {
            'aset': forms.Select(attrs={
                'class': 'form-select',
            }),
            'jenis_perawatan': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'km_saat_servis': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 45000',
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)',
            }),
            'dicatat_oleh': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama teknisi',
            }),
        }
        labels = {
            'aset': 'Kendaraan / Aset',
            'jenis_perawatan': 'Jenis Perawatan',
            'tanggal': 'Tanggal Servis',
            'km_saat_servis': 'KM Saat Servis',
            'catatan': 'Catatan',
            'dicatat_oleh': 'Dicatat Oleh',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PerawatanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['aset'].queryset = Aset.objects.filter(user=user)