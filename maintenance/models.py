from django.db import models
from django.contrib.auth.models import User

class Aset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    kode_aset = models.CharField(max_length=20, unique=True)
    nama_kendaraan = models.CharField(max_length=100)
    jenis = models.CharField(max_length=50)  # Truk, Alat Berat, dll
    km_terakhir = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.kode_aset} - {self.nama_kendaraan}"


class Perawatan(models.Model):
    JENIS_CHOICES = [
        ('ganti_oli', 'Ganti Oli'),
        ('servis_rutin', 'Servis Rutin'),
        ('ganti_ban', 'Ganti Ban'),
        ('servis_besar', 'Servis Besar'),
        ('lainnya', 'Lainnya'),
    ]

    aset = models.ForeignKey(Aset, on_delete=models.CASCADE)
    jenis_perawatan = models.CharField(max_length=50, choices=JENIS_CHOICES)
    tanggal = models.DateField()
    km_saat_servis = models.IntegerField()
    catatan = models.TextField(blank=True)
    dicatat_oleh = models.CharField(max_length=100)

    # Hasil kalkulasi next service
    next_service_km = models.IntegerField(null=True, blank=True)
    next_service_tanggal = models.DateField(null=True, blank=True)

    # Flag anomali
    is_anomali = models.BooleanField(default=False)
    pesan_anomali = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aset.kode_aset} - {self.jenis_perawatan} - {self.tanggal}"

    class Meta:
        ordering = ['-tanggal']