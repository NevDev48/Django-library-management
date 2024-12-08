from django.urls import path
from .views import *

urlpatterns = [
    path('loginAuthPage', loginAuthPage, name='loginAuthPage'),
    path('logout/', logout_view, name='logout'),
    path('home', home, name='home'),  # Tambahkan name='home'

    #reader tab
    path('readers', readers_tab, name='readers'),  # Tambahkan name='readers'
    path('add_readers', add_readers_tab, name='add_readers'),
    path("update_readers", update_readers_tab, name='update_readers'),
    path('update_readers_tab/<int:id>/',update_reader,name="update_reader"),
    path('delete/<int:id>/',delete_reader,name="delete"),

    #books tab
    path('books', books_tab, name='books'),
    path('add_books', add_books_tab, name="add_books"),
    path('save_books', save_books, name="save_books"),
    path('update_books_tab/<int:id>/', update_books_tab, name="update_books_tab"),
    path('update_books/<int:id>/', update_books, name='update_books'),
    path('delete_book/<int:id>/', delete_book, name='delete_book'),

    #jurnal tab
    path('jurnal', jurnal_tab, name='jurnal'),
    path('jurnal/save/', save_jurnal, name='save_jurnal'),
    path('delete_jurnal/<int:jurnal_id>/', delete_jurnal, name='delete_jurnal'),

    #page
    path('beranda', beranda, name='beranda'),
    path('jurnal_page', jurnal_page, name='jurnal_page'),
    path('buku', buku, name='buku'),
    path('riwayat', riwayat, name='riwayat'),
    path('profil', profil, name='profil'),
    path('login', loginPage, name='login'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('password/<int:reader_id>/', ubah_password_tab, name='password'),
]
