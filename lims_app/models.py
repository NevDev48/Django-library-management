from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id=models.CharField(max_length=200)
    password = models.CharField(max_length=200, default="")
    reader_name=models.CharField(max_length=200)
    reader_contact=models.CharField(max_length=200)
    reader_address=models.TextField()
    active=models.BooleanField(default=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Book_lib(models.Model):
    def __str__(self):
        return self.title
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True) 

class BorrowHistory(models.Model):
    reader = models.ForeignKey(reader, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book_lib, on_delete=models.CASCADE, related_name='borrow_history')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reader.reader_name} - {self.book.title} - {self.borrowed_at}"

class jurnal(models.Model):
    def __str__(self):
        return self.judul
    judul = models.CharField(max_length=255)
    dokumen = models.FileField(upload_to='jurnal/')

class ContactUs(models.Model):
    nama = models.CharField(max_length=100, verbose_name="Nama")
    email = models.EmailField(verbose_name="Email")
    isi_pesan = models.TextField(verbose_name="Isi Pesan")

    def __str__(self):
        return f"{self.nama} - {self.email}"