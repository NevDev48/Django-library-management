from django.db import models

# Create your models here.

class reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id=models.CharField(max_length=200)
    reader_name=models.CharField(max_length=200)
    reader_contact=models.CharField(max_length=200)
    reader_address=models.TextField()
    active=models.BooleanField(default=True)

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

class jurnal(models.Model):
    def __str__(self):
        return self.judul
    judul = models.CharField(max_length=255)
    dokumen = models.FileField(upload_to='jurnal/')