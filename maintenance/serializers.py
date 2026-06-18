from rest_framework import serializers
from .models import Aset, Perawatan


class AsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aset
        fields = '__all__'


class PerawatanSerializer(serializers.ModelSerializer):
    aset_detail = AsetSerializer(source='aset', read_only=True)
    jenis_perawatan_label = serializers.CharField(
        source='get_jenis_perawatan_display', read_only=True
    )

    class Meta:
        model = Perawatan
        fields = '__all__'