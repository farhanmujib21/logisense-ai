from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('input/', views.input_perawatan, name='input_perawatan'),
    path('aset/tambah/', views.tambah_aset, name='tambah_aset'),
    path('riwayat/', views.riwayat, name='riwayat'),
    path('aset/<str:kode_aset>/', views.detail_aset, name='detail_aset'),
    path('api/aset/', api_views.api_aset_list, name='api_aset_list'),
    path('api/aset/<int:pk>/', api_views.api_aset_detail, name='api_aset_detail'),
    path('api/perawatan/', api_views.api_perawatan_list, name='api_perawatan_list'),
    path('api/perawatan/<int:pk>/', api_views.api_perawatan_detail, name='api_perawatan_detail'),
]