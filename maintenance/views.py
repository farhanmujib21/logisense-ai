
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Aset, Perawatan
from .forms import PerawatanForm, AsetForm
from .logic import hitung_next_service, deteksi_anomali, cek_status_kendaraan
from django.contrib.auth.decorators import login_required


# =============================================
# DASHBOARD - Halaman Utama
# =============================================
@login_required
def dashboard(request):
    aset_list = Aset.objects.filter(user=request.user)
    data_dashboard = []

    for aset in aset_list:
        perawatan_terakhir = Perawatan.objects.filter(aset=aset).first()
        status, pesan_status = cek_status_kendaraan(perawatan_terakhir)
        data_dashboard.append({
            'aset': aset,
            'perawatan_terakhir': perawatan_terakhir,
            'status': status,
            'pesan_status': pesan_status,
        })

    context = {
        'data_dashboard': data_dashboard,
        'total_aset': aset_list.count(),
        'total_overdue': sum(1 for d in data_dashboard if d['status'] == 'overdue'),
        'total_warning': sum(1 for d in data_dashboard if d['status'] == 'warning'),
    }
    return render(request, 'maintenance/dashboard.html', context)


# =============================================
# FORM INPUT PERAWATAN
# =============================================
@login_required
def input_perawatan(request):
    if request.method == 'POST':
        form = PerawatanForm(request.POST, user=request.user)
        if form.is_valid():
            perawatan = form.save(commit=False)

            # Jalankan deteksi anomali
            is_anomali, pesan_anomali = deteksi_anomali(
                aset=perawatan.aset,
                km_sekarang=perawatan.km_saat_servis,
                tanggal_servis=perawatan.tanggal,
                jenis_perawatan=perawatan.jenis_perawatan,
            )

            # Hitung next service
            next_km, next_tanggal = hitung_next_service(
                jenis_perawatan=perawatan.jenis_perawatan,
                km_sekarang=perawatan.km_saat_servis,
                tanggal_servis=perawatan.tanggal,
            )

            # Simpan semua data
            perawatan.is_anomali = is_anomali
            perawatan.pesan_anomali = pesan_anomali
            perawatan.next_service_km = next_km
            perawatan.next_service_tanggal = next_tanggal
            perawatan.save()

            # Update KM terakhir di aset
            aset = perawatan.aset
            aset.km_terakhir = perawatan.km_saat_servis
            aset.save()

            # Tampilkan peringatan jika ada anomali
            if is_anomali:
                messages.warning(
                    request,
                    f"⚠️ Data tersimpan dengan peringatan anomali: {pesan_anomali}"
                )
            else:
                messages.success(
                    request,
                    f"✅ Data perawatan berhasil disimpan! "
                    f"Next service: KM {next_km} atau {next_tanggal}"
                )

            return redirect('dashboard')
    else:
        form = PerawatanForm(user=request.user)

    return render(request, 'maintenance/input_perawatan.html', {'form': form})


# =============================================
# RIWAYAT PERAWATAN
# =============================================
@login_required
def riwayat(request):
    perawatan_list = Perawatan.objects.select_related('aset').filter(aset__user=request.user)

    # Filter berdasarkan aset jika ada query
    aset_filter = request.GET.get('aset')
    if aset_filter:
        perawatan_list = perawatan_list.filter(aset__kode_aset=aset_filter)

    context = {
        'perawatan_list': perawatan_list,
        'aset_list': Aset.objects.filter(user=request.user),
        'aset_filter': aset_filter,
    }
    return render(request, 'maintenance/riwayat.html', context)


# =============================================
# DETAIL ASET
# =============================================
@login_required
def detail_aset(request, kode_aset):
    aset = get_object_or_404(Aset, kode_aset=kode_aset, user=request.user)
    perawatan_list = Perawatan.objects.filter(aset=aset)
    perawatan_terakhir = perawatan_list.first()
    status, pesan_status = cek_status_kendaraan(perawatan_terakhir)

    context = {
        'aset': aset,
        'perawatan_list': perawatan_list,
        'perawatan_terakhir': perawatan_terakhir,
        'status': status,
        'pesan_status': pesan_status,
    }
    return render(request, 'maintenance/detail_aset.html', context)

# =============================================
# TAMBAH ASET BARU
# =============================================
@login_required
def tambah_aset(request):
    if request.method == 'POST':
        form = AsetForm(request.POST)
        if form.is_valid():
            aset = form.save(commit=False)
            aset.user = request.user
            aset.save()
            messages.success(request, f"✅ Data aset {aset.kode_aset} berhasil ditambahkan!")
            return redirect('dashboard')
    else:
        form = AsetForm()

    return render(request, 'maintenance/tambah_aset.html', {'form': form})