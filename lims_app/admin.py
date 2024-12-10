from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(reader)
admin.site.register(Category)
admin.site.register(Book_lib)
admin.site.register(jurnal)
admin.site.register(BorrowHistory)
admin.site.register(ContactUs)