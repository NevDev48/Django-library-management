from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='home'),  # Tambahkan name='home'

    #reader tab
    path('readers', readers_tab, name='readers'),  # Tambahkan name='readers'
    path('add_readers', add_readers_tab, name='add_readers'),
    path("update_readers", update_readers_tab, name='update_readers'),
    path('update_readers_tab/<int:id>/',update_reader,name="update_reader"),
    path('delete/<int:id>/',delete_reader,name="delete"),

    #books tab
    path('books', books, name='books'),
]
