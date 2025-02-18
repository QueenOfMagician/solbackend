from .models import BarangLelang, TransaksiLelang
from rest_framework import serializers
from django.utils import timezone
from akun.models import Pengguna

class BarangSerializers(serializers.ModelSerializer):
    penjual = serializers.StringRelatedField()
    class Meta:
        model = BarangLelang
        fields = '__all__'

class BarangSayaSerializers(serializers.ModelSerializer):
    penjual = serializers.StringRelatedField()
    bidder_tertinggi = serializers.SerializerMethodField()  # Custom field

    class Meta:
        model = BarangLelang
        fields = ["kode", "nama", "harga_saatini", "penjual", "bidder_tertinggi"]

    def get_bidder_tertinggi(self, obj):
        highest_bid = obj.transaksi.order_by('-harga_bid').first()
        if highest_bid:
            return highest_bid.pelelang
        return None

from rest_framework import serializers

class PesananSayaSerializers(serializers.ModelSerializer):
    bidder_tertinggi = serializers.SerializerMethodField()
    pernah_mengikuti = serializers.SerializerMethodField()

    class Meta:
        model = BarangLelang
        fields = [
            "kode",
            "nama",
            "harga_saatini",
            "penjual",
            "bidder_tertinggi",
            "pernah_mengikuti",
            "lelang_ditutup",
        ]

    def get_bidder_tertinggi(self, obj):
        highest_bid = (
            TransaksiLelang.objects.filter(barang=obj)
            .order_by("-harga_bid", "waktu_bid")
            .first()
        )
        return highest_bid.pelelang if highest_bid else None

    def get_pernah_mengikuti(self, obj):
        user = self.context["request"].user
        return TransaksiLelang.objects.filter(barang=obj, pelelang=user.username).exists()


class RiwayatBidSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransaksiLelang
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiLelang
        fields = ['barang', 'pelelang', 'harga_bid']
    def validate(self, data):
        barang = data['barang']
        harga_bid = data['harga_bid']
        if barang.lelang_ditutup < timezone.now():
            raise serializers.ValidationError("Lelang sudah ditutup.")
        if harga_bid <= barang.harga_saatini:
            raise serializers.ValidationError("Harga bid harus lebih tinggi dari harga saat ini.")
        return data

class TambahBarangSerializers(serializers.ModelSerializer):
    penjual = serializers.PrimaryKeyRelatedField(queryset=Pengguna.objects.all())

    class Meta:
        model = BarangLelang
        fields = ["nama", "deskripsi", "kategori", "harga_buka", "harga_saatini", "gambar", "lelang_dibuka", "lelang_ditutup", "penjual"]
        read_only_fields = ["harga_saatini"]

    def validate(self, data):
        if 'harga_buka' in data:
            data['harga_saatini'] = data['harga_buka']
        return data
