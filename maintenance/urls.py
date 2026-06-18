from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('input/', views.input_perawatan, name='input_perawatan'),
    path('aset/tambah/', views.tambah_aset, name='tambah_aset'),
    path('riwayat/', views.riwayat, name='riwayat'),
    path('aset/<str:kode_aset>/', views.detail_aset, name='detail_aset'),
]