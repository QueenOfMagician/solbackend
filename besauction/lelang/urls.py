from django.urls import path
from .views import BarangViews, BidView, RiwayatLelangView, TambahBarangView, BarangSearchView, BarangSayaViews, \
    PesananSayaViews

urlpatterns = [
    path("list-barang/", BarangViews.as_view(), name="listbarang"),
    path("barangsaya/", BarangSayaViews.as_view(), name="barangsaya"),
    path("bid/", BidView.as_view(), name="Bidding"),
    path("riwayat/", RiwayatLelangView.as_view(), name="riwayat"),
    path("tambahbarang/", TambahBarangView.as_view(), name="tambahbarang"),
    path('search/', BarangSearchView.as_view(), name='search'),
    path("pesanansaya/", PesananSayaViews.as_view(), name="pesanansaya")
]

