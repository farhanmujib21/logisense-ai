from django.contrib import admin
from .models import Aset, Perawatan

@admin.register(Aset)
class AsetAdmin(admin.ModelAdmin):
    list_display = ['kode_aset', 'nama_kendaraan', 'jenis', 'km_terakhir']

@admin.register(Perawatan)
class PerawatanAdmin(admin.ModelAdmin):
    list_display = ['aset', 'jenis_perawatan', 'tanggal', 'km_saat_servis', 'is_anomali']