from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Aset, Perawatan
from .serializers import AsetSerializer, PerawatanSerializer
from .logic import hitung_next_service, deteksi_anomali


# =============================================
# API ASET
# =============================================

@api_view(['GET', 'POST'])
def api_aset_list(request):
    # GET — ambil semua aset
    if request.method == 'GET':
        aset = Aset.objects.all()
        serializer = AsetSerializer(aset, many=True)
        return Response({
            'status': 'success',
            'count': aset.count(),
            'data': serializer.data
        })

    # POST — tambah aset baru
    elif request.method == 'POST':
        serializer = AsetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Aset berhasil ditambahkan',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Data tidak valid',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_aset_detail(request, pk):
    try:
        aset = Aset.objects.get(pk=pk)
    except Aset.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Aset tidak ditemukan'
        }, status=status.HTTP_404_NOT_FOUND)

    # GET — detail satu aset
    if request.method == 'GET':
        serializer = AsetSerializer(aset)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    # PUT — update aset
    elif request.method == 'PUT':
        serializer = AsetSerializer(aset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Aset berhasil diperbarui',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # DELETE — hapus aset
    elif request.method == 'DELETE':
        nama = aset.nama_kendaraan
        aset.delete()
        return Response({
            'status': 'success',
            'message': f'Aset {nama} berhasil dihapus'
        }, status=status.HTTP_200_OK)


# =============================================
# API PERAWATAN
# =============================================

@api_view(['GET', 'POST'])
def api_perawatan_list(request):
    # GET — ambil semua perawatan
    if request.method == 'GET':
        perawatan = Perawatan.objects.select_related('aset').all()
        serializer = PerawatanSerializer(perawatan, many=True)
        return Response({
            'status': 'success',
            'count': perawatan.count(),
            'data': serializer.data
        })

    # POST — tambah perawatan baru
    elif request.method == 'POST':
        serializer = PerawatanSerializer(data=request.data)
        if serializer.is_valid():
            perawatan = serializer.save()

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

            perawatan.is_anomali = is_anomali
            perawatan.pesan_anomali = pesan_anomali
            perawatan.next_service_km = next_km
            perawatan.next_service_tanggal = next_tanggal
            perawatan.save()

            # Update KM aset
            aset = perawatan.aset
            aset.km_terakhir = perawatan.km_saat_servis
            aset.save()

            return Response({
                'status': 'success',
                'message': 'Data perawatan berhasil disimpan',
                'anomali_terdeteksi': is_anomali,
                'pesan_anomali': pesan_anomali if is_anomali else None,
                'next_service_km': next_km,
                'next_service_tanggal': str(next_tanggal),
                'data': PerawatanSerializer(perawatan).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_perawatan_detail(request, pk):
    try:
        perawatan = Perawatan.objects.get(pk=pk)
    except Perawatan.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Data perawatan tidak ditemukan'
        }, status=status.HTTP_404_NOT_FOUND)

    # GET — detail satu perawatan
    if request.method == 'GET':
        serializer = PerawatanSerializer(perawatan)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    # PUT — update perawatan
    elif request.method == 'PUT':
        serializer = PerawatanSerializer(perawatan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Data perawatan berhasil diperbarui',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # DELETE — hapus perawatan
    elif request.method == 'DELETE':
        perawatan.delete()
        return Response({
            'status': 'success',
            'message': 'Data perawatan berhasil dihapus'
        }, status=status.HTTP_200_OK)