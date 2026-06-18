from datetime import date, timedelta

# =============================================
# ATURAN INTERVAL SERVIS (Rule-Based)
# =============================================
INTERVAL_SERVIS = {
    'ganti_oli':    {'km': 5000,  'bulan': 3},
    'servis_rutin': {'km': 10000, 'bulan': 6},
    'ganti_ban':    {'km': 40000, 'bulan': 24},
    'servis_besar': {'km': 20000, 'bulan': 12},
    'lainnya':      {'km': 10000, 'bulan': 6},
}

# =============================================
# FUNGSI 1: HITUNG NEXT SERVICE
# =============================================
def hitung_next_service(jenis_perawatan, km_sekarang, tanggal_servis):
    """
    Menghitung kapan servis berikutnya berdasarkan
    jenis perawatan, KM saat ini, dan tanggal servis.
    """
    interval = INTERVAL_SERVIS.get(jenis_perawatan, INTERVAL_SERVIS['lainnya'])

    next_km = km_sekarang + interval['km']
    next_tanggal = tanggal_servis + timedelta(days=interval['bulan'] * 30)

    return next_km, next_tanggal


# =============================================
# FUNGSI 2: DETEKSI ANOMALI
# =============================================
def deteksi_anomali(aset, km_sekarang, tanggal_servis, jenis_perawatan):
    """
    Memeriksa apakah data yang diinput mencurigakan.
    Mengembalikan (is_anomali, pesan_anomali).
    """
    pesan = []

    # Cek 1: KM tidak boleh lebih kecil dari KM terakhir
    if km_sekarang < aset.km_terakhir:
        pesan.append(
            f"KM saat ini ({km_sekarang}) lebih kecil dari KM terakhir "
            f"({aset.km_terakhir}). Kemungkinan salah input."
        )

    # Cek 2: KM tidak boleh loncat terlalu jauh (lebih dari 50.000 sekaligus)
    if km_sekarang - aset.km_terakhir > 50000:
        pesan.append(
            f"Selisih KM terlalu besar "
            f"({km_sekarang - aset.km_terakhir} KM). Harap periksa kembali."
        )

    # Cek 3: Tanggal tidak boleh di masa depan
    if tanggal_servis > date.today():
        pesan.append(
            f"Tanggal servis ({tanggal_servis}) tidak boleh di masa depan."
        )

    # Cek 4: Cek duplikat - servis jenis sama dalam 7 hari terakhir
    from .models import Perawatan
    servis_terakhir = Perawatan.objects.filter(
        aset=aset,
        jenis_perawatan=jenis_perawatan,
    ).order_by('-tanggal').first()

    if servis_terakhir:
        selisih_hari = (tanggal_servis - servis_terakhir.tanggal).days
        if 0 <= selisih_hari <= 7:
            pesan.append(
                f"Servis {jenis_perawatan.replace('_', ' ')} sudah dilakukan "
                f"{selisih_hari} hari lalu. Kemungkinan data duplikat."
            )

    is_anomali = len(pesan) > 0
    return is_anomali, " | ".join(pesan)


# =============================================
# FUNGSI 3: STATUS KENDARAAN
# =============================================
def cek_status_kendaraan(perawatan_terakhir):
    """
    Mengecek apakah kendaraan sudah mendekati
    atau melewati jadwal servis berikutnya.
    """
    if not perawatan_terakhir:
        return 'unknown', 'Belum ada data perawatan'

    hari_tersisa = (perawatan_terakhir.next_service_tanggal - date.today()).days

    if hari_tersisa < 0:
        return 'overdue', f'Terlambat {abs(hari_tersisa)} hari!'
    elif hari_tersisa <= 14:
        return 'warning', f'Servis dalam {hari_tersisa} hari lagi'
    else:
        return 'ok', f'Servis berikutnya {hari_tersisa} hari lagi'