from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Category, reader, Book_lib, jurnal

# Login page
def loginAuthPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, f'Welcome, {username}!')
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, "auth/login.html")

# Logout view
def logout_view(request):
    logout(request)  # Logout user
    messages.success(request, "You have been logged out successfully.")  # Logout message
    return redirect('loginAuthPage') 

# Home page - requires login
@login_required(login_url='loginAuthPage')
def home(request):
    return render(request, "home.html", context={"current_tab": "home"})

# Readers tab - requires login
@login_required(login_url='loginAuthPage')
def readers_tab(request):
    if request.method == "GET":
        readers = reader.objects.all()
        return render(request, "readers.html", context={"current_tab": "readers", "readers": readers})
    
    else:  # Handle POST request (search data)
        query = request.POST['query']
        readers = reader.objects.raw(
            "SELECT * FROM lims_app_reader WHERE reader_name LIKE %s",
            [f"%{query}%"]
        )
        return render(request, "readers.html", context={"current_tab": "readers", "readers": readers, "query": query})

# Add readers tab - requires login
@login_required(login_url='loginAuthPage')
def add_readers_tab(request):
    if request.method == "POST":
        # Get data from the form
        reference_id = request.POST.get('reader_nim')
        reader_name = request.POST.get('reader_name')
        reader_contact = request.POST.get('reader_contact')
        reader_address = request.POST.get('address')
        
        # Save data to the database
        reader_item = reader(
            reference_id=reference_id,
            reader_name=reader_name,
            reader_contact=reader_contact,
            reader_address=reader_address,
            active=True  # Default True as per model
        )
        reader_item.save() 
        
        return redirect('/readers')
    return render(request, "action/add_readers.html")

# Other views that require login

@login_required(login_url='loginAuthPage')
def save_reader(request):
    reader_item = reader(
        reference_id=request.POST['reader_nim'],
        reader_name=request.POST['reader_name'],
        reader_contact=request.POST['reader_contact'],
        reader_address=request.POST['address'],
        active=True,
    )
    reader_item.save()
    return redirect('/add_readers')

@login_required(login_url='loginAuthPage')
def delete_reader(request, id):
    try:
        reader_item = reader.objects.get(id=id)
        reader_item.delete()
    except reader.DoesNotExist:
        pass  # Handle case where reader doesn't exist
    return redirect('/readers') 

@login_required(login_url='loginAuthPage')
def update_readers_tab(request, id):
    readers = reader.objects.get(id=id)
    return render(request, 'action/update_readers.html', {"readers": readers})

@login_required(login_url='loginAuthPage')
def update_reader(request, id):
    reader_item = reader.objects.get(id=id)
    if request.method == "POST":
        reader_item.reference_id = request.POST['reader_nim']
        reader_item.reader_name = request.POST['reader_name']
        reader_item.reader_contact = request.POST['reader_contact']
        reader_item.reader_address = request.POST['address']
        reader_item.save()
        return redirect('/readers')
    return render(request, 'action/update_readers.html', {"reader": reader_item})

# Books views that require login
@login_required(login_url='loginAuthPage')
def books_tab(request):
    query1 = ''  
    if request.method == "GET":
        books = Book_lib.objects.all()
    else: 
        query1 = request.POST.get('query1', '')
        if query1:
            books = Book_lib.objects.filter(title__icontains=query1)
        else:
            books = Book_lib.objects.all()
    return render(request, "books.html", context={"current_tab": "books", "books": books, "query1": query1})

@login_required(login_url='loginAuthPage')
def add_books_tab(request):
    categories = Category.objects.all()
    return render(request, "action/add_books.html", {'categories': categories})

@login_required(login_url='loginAuthPage')
def save_books(request):
    if request.method == "POST":
        category = Category.objects.get(id=request.POST['category'])
        image = request.FILES.get('image')  # Get image file
        
        book_item = Book_lib(
            category=category,
            title=request.POST['title'],
            author=request.POST['author'],
            publication_date=request.POST['publication_date'],
            image=image,
        )
        book_item.save()
        return redirect("/books")

@login_required(login_url='loginAuthPage')
def update_books_tab(request, id):
    books = get_object_or_404(Book_lib, id=id)
    categories = Category.objects.all()
    return render(request, "action/update_books.html", {"books": books, 'categories': categories})

@login_required(login_url='loginAuthPage')
def update_books(request, id):
    book_item = get_object_or_404(Book_lib, id=id)
    if request.method == "POST":
        category = Category.objects.get(id=request.POST['category'])
        image = request.FILES.get('image')  # Get image file if available

        book_item.category = category
        book_item.title = request.POST['title']
        book_item.author = request.POST['author']
        book_item.publication_date = request.POST['publication_date']
        
        if image:
            book_item.image = image
        
        book_item.save()  # Save changes
        return redirect("/books")
    return render(request, 'action/update_books.html', {"book": book_item})

@login_required(login_url='loginAuthPage')
def delete_book(request, id):
    try:
        book_item = Book_lib.objects.get(id=id)
        book_item.delete()
    except Book_lib.DoesNotExist:
        return HttpResponse("Book not found", status=404)
    return redirect('/books')


#jurnal page
from django.shortcuts import render, redirect
from .models import jurnal

def jurnal_tab(request):
    if request.method == "GET":
        jurnals = jurnal.objects.all()
    return render(request, 'jurnal.html', {'current_tab': 'jurnal', 'jurnals': jurnals})

def save_jurnal(request):
    if request.method == "POST":
        judul = request.POST['judul']
        dokumen = request.FILES.get('dokumen')

        # Simpan data jurnal ke database
        jurnal_item = jurnal(
            judul=judul,
            dokumen=dokumen,
        )
        jurnal_item.save()
        return redirect('/jurnal')
    
def delete_jurnal(request, jurnal_id):
    jurnal_item = get_object_or_404(jurnal, id=jurnal_id)
    jurnal_item.delete()
    return redirect('/jurnal')
