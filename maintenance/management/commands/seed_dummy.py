from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from maintenance.models import Aset, Perawatan


class Command(BaseCommand):
    help = 'Membuat data dummy aset dan perawatan untuk akun admin'

    def handle(self, *args, **options):
        # Cari user admin
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stderr.write(self.style.ERROR('❌ Tidak ada akun superuser/admin ditemukan!'))
                return
            self.stdout.write(f'Menggunakan akun admin: {admin_user.username}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error mencari admin: {e}'))
            return

        # =============================================
        # HAPUS DATA LAMA (biar bersih)
        # =============================================
        Perawatan.objects.all().delete()
        Aset.objects.all().delete()
        self.stdout.write('Data lama dihapus.')

        # =============================================
        # BUAT DATA ASET (dengan user=admin)
        # =============================================
        trk1 = Aset.objects.create(
            user=admin_user,
            kode_aset='TRK-001', nama_kendaraan='Truk Hino 500',
            jenis='Truk', km_terakhir=47000
        )
        trk2 = Aset.objects.create(
            user=admin_user,
            kode_aset='TRK-002', nama_kendaraan='Truk Mitsubishi Colt',
            jenis='Truk', km_terakhir=31000
        )
        alb1 = Aset.objects.create(
            user=admin_user,
            kode_aset='ALB-001', nama_kendaraan='Excavator Komatsu PC200',
            jenis='Alat Berat', km_terakhir=8500
        )
        mtr1 = Aset.objects.create(
            user=admin_user,
            kode_aset='MTR-001', nama_kendaraan='Motor Honda Vario',
            jenis='Motor', km_terakhir=22000
        )
        self.stdout.write('4 Aset berhasil dibuat.')

        # =============================================
        # BUAT DATA PERAWATAN
        # =============================================

        # TRK-001 — servis berikutnya sudah dekat (WARNING)
        Perawatan.objects.create(
            aset=trk1, jenis_perawatan='ganti_oli',
            tanggal=date.today() - timedelta(days=75),
            km_saat_servis=42000, dicatat_oleh='Budi Santoso',
            catatan='Ganti oli mesin 10W-40',
            next_service_km=47000,
            next_service_tanggal=date.today() + timedelta(days=10),
            is_anomali=False
        )
        Perawatan.objects.create(
            aset=trk1, jenis_perawatan='servis_rutin',
            tanggal=date.today() - timedelta(days=150),
            km_saat_servis=38000, dicatat_oleh='Budi Santoso',
            catatan='Servis rutin 40.000 KM',
            next_service_km=48000,
            next_service_tanggal=date.today() + timedelta(days=60),
            is_anomali=False
        )

        # TRK-002 — sudah overdue
        Perawatan.objects.create(
            aset=trk2, jenis_perawatan='ganti_oli',
            tanggal=date.today() - timedelta(days=100),
            km_saat_servis=26000, dicatat_oleh='Agus Prayitno',
            catatan='Ganti oli + filter oli',
            next_service_km=31000,
            next_service_tanggal=date.today() - timedelta(days=10),
            is_anomali=False
        )
        Perawatan.objects.create(
            aset=trk2, jenis_perawatan='ganti_ban',
            tanggal=date.today() - timedelta(days=200),
            km_saat_servis=20000, dicatat_oleh='Agus Prayitno',
            catatan='Ganti 4 ban depan belakang',
            next_service_km=60000,
            next_service_tanggal=date.today() + timedelta(days=400),
            is_anomali=False
        )

        # ALB-001 — kondisi normal
        Perawatan.objects.create(
            aset=alb1, jenis_perawatan='servis_rutin',
            tanggal=date.today() - timedelta(days=30),
            km_saat_servis=8000, dicatat_oleh='Hendra Wijaya',
            catatan='Servis rutin excavator, cek hidrolik',
            next_service_km=18000,
            next_service_tanggal=date.today() + timedelta(days=150),
            is_anomali=False
        )

        # MTR-001 — ada anomali di data lama
        Perawatan.objects.create(
            aset=mtr1, jenis_perawatan='ganti_oli',
            tanggal=date.today() - timedelta(days=5),
            km_saat_servis=22000, dicatat_oleh='Rizky Firmansyah',
            catatan='Ganti oli mesin',
            next_service_km=27000,
            next_service_tanggal=date.today() + timedelta(days=85),
            is_anomali=False
        )
        Perawatan.objects.create(
            aset=mtr1, jenis_perawatan='ganti_oli',
            tanggal=date.today() - timedelta(days=60),
            km_saat_servis=19000, dicatat_oleh='Rizky Firmansyah',
            catatan='',
            next_service_km=24000,
            next_service_tanggal=date.today() + timedelta(days=30),
            is_anomali=True,
            pesan_anomali='KM saat ini (19000) lebih kecil dari KM terakhir (20500). Kemungkinan salah input.'
        )

        self.stdout.write(self.style.SUCCESS('Data dummy berhasil dibuat! (7 perawatan, 4 aset)'))
