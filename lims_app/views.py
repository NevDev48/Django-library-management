from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import BorrowHistory, Category, reader, Book_lib, jurnal


#VIEWS ADMIN
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
        raw_password = request.POST.get('password')  # Ambil password mentah
        reader_contact = request.POST.get('reader_contact')
        reader_address = request.POST.get('address')
        
        # Hash password
        hashed_password = make_password(raw_password)
        
        # Save data to the database
        reader_item = reader(
            reference_id=reference_id,
            reader_name=reader_name,
            password=hashed_password,
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
        password=request.POST['password'],
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

@login_required(login_url='loginAuthPage')
def jurnal_tab(request):
    if request.method == "GET":
        jurnals = jurnal.objects.all()
    return render(request, 'jurnal.html', {'current_tab': 'jurnal', 'jurnals': jurnals})

@login_required(login_url='loginAuthPage')
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
    
@login_required(login_url='loginAuthPage')
def delete_jurnal(request, jurnal_id):
    jurnal_item = get_object_or_404(jurnal, id=jurnal_id)
    jurnal_item.delete()
    return redirect('/jurnal')

@login_required(login_url='loginAuthPage')
def returns(request):
    borrowed_books = BorrowHistory.objects.filter(is_returned=False)  # Hanya buku yang belum dikembalikan
    return render(request, 'return.html', {'current_tab': 'returns', 'borrowed_books': borrowed_books})

@login_required(login_url='loginAuthPage')
def kembalikan_buku_admin(request, borrow_id):
    borrow_history = get_object_or_404(BorrowHistory, id=borrow_id)

    # Periksa apakah buku sudah dikembalikan
    if borrow_history.is_returned:
        messages.error(request, "Buku ini sudah dikembalikan.")
        return redirect('returns')

    # Tandai buku sebagai dikembalikan
    borrow_history.is_returned = True
    borrow_history.save()

    messages.success(request, f"Buku '{borrow_history.book.title}' berhasil dikembalikan.")
    return redirect('returns')


#INI PAGE USER
def loginPage(request):
    if request.method == 'POST':
        reference_id = request.POST.get('reference_id')
        password = request.POST.get('password')

        try:
            # Check if reference_id exists
            user = reader.objects.get(reference_id=reference_id)
            
            # Verify if the password matches
            if check_password(password, user.password):
                # Store user info in session
                request.session['reference_id'] = user.reference_id
                request.session['reader_name'] = user.reader_name 

                # Debugging
                print(f"Session created: {request.session['reference_id']} - {request.session['reader_name']}")
                messages.success(request, f'Welcome, {user.reader_name}!')
                return redirect('beranda')  # Redirect ke beranda
            else:
                messages.error(request, 'Password salah. Silakan coba lagi.')
        except reader.DoesNotExist:
            messages.error(request, 'Reference ID tidak ditemukan.')

    return render(request, "page/login.html")


def logoutPage(request):
    request.session.flush()  # Hapus semua data di session
    return redirect('beranda')

def beranda(request):
    reference_id = request.session.get('reference_id')
    current_user = None
    if reference_id:
        try:
            current_user = reader.objects.get(reference_id=reference_id)
        except reader.DoesNotExist:
            current_user = None
    jurnals = jurnal.objects.all()
    books = Book_lib.objects.all()
    readers = reader.objects.all()

    return render(request, "page/beranda.html", {
        'current_tab': 'beranda',
        'jurnals': jurnals,
        'books': books,
        'readers': readers,
        'current_user': current_user  # Tidak ada user login
    })



def jurnal_page(request):
    if request.method == "GET":
        jurnals = jurnal.objects.all()


    return render(request, "page/jurnal_page.html", {'current_tab': 'jurnal_page', 'jurnals': jurnals})

def buku(request):
    if not request.session.get('reference_id'):
        return redirect('login')

    # Ambil buku yang belum dipinjam
    reader_instance = get_object_or_404(reader, reference_id=request.session.get('reference_id'))
    borrowed_books = BorrowHistory.objects.filter(reader=reader_instance, is_returned=False).values_list('book', flat=True)
    available_books = Book_lib.objects.exclude(id__in=borrowed_books)

    return render(request, "page/buku.html", {'current_tab': 'buku', 'books': available_books})


def pinjam_buku(request, book_id):
    if not request.session.get('reference_id'):
        messages.error(request, "Anda harus login untuk meminjam buku.")
        return redirect('login')

    book = get_object_or_404(Book_lib, id=book_id)
    reader_instance = get_object_or_404(reader, reference_id=request.session.get('reference_id'))

    # Catat riwayat peminjaman
    BorrowHistory.objects.create(reader=reader_instance, book=book)

    # Anda tidak perlu menghapus buku dari database, cukup buat entri di BorrowHistory
    messages.success(request, f"Buku '{book.title}' berhasil dipinjam.")
    return redirect('buku')


def kembalikan_buku(request, borrow_id):
    if not request.session.get('reference_id'):
        messages.error(request, "Anda harus login untuk mengembalikan buku.")
        return redirect('login')

    borrow_history = get_object_or_404(BorrowHistory, id=borrow_id)
    
    # Periksa apakah buku sudah dikembalikan
    if borrow_history.is_returned:
        messages.error(request, "Buku ini sudah dikembalikan.")
        return redirect('riwayat')

    # Tandai buku sebagai dikembalikan
    borrow_history.is_returned = True
    borrow_history.save()

    # Buku tidak perlu ditambahkan lagi ke database karena sudah ada di Book_lib
    messages.success(request, f"Buku '{borrow_history.book.title}' berhasil dikembalikan.")
    return redirect('riwayat')


def riwayat(request):
    if not request.session.get('reference_id'):
        return redirect('login')

    reader_instance = get_object_or_404(reader, reference_id=request.session.get('reference_id'))
    riwayat_buku = BorrowHistory.objects.filter(reader=reader_instance)

    return render(request, "page/riwayat.html", {'current_tab': 'riwayat', 'riwayat_buku': riwayat_buku})

def profil(request):
    reference_id = request.session.get('reference_id', None)
    current_user = None
    if reference_id:
        try:
            current_user = reader.objects.get(reference_id=reference_id)
        except reader.DoesNotExist:
            current_user = None

    if not current_user:
        return HttpResponse("User tidak ditemukan di database.", status=404)

    return render(request, 'page/profile.html', {
        'current_user': current_user,
        'reader_id': current_user.id  # Make sure this is passed
    })

def ubah_password_tab(request, reader_id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if not new_password or len(new_password) < 8:
            messages.error(request, "Password harus memiliki minimal 8 karakter.")
            return redirect('password', reader_id=reader_id)

        try:
            pembaca = reader.objects.get(id=reader_id)
        except reader.DoesNotExist:
            messages.error(request, "Reader dengan ID tersebut tidak ditemukan.")
            return redirect('password', reader_id=reader_id)

        pembaca.set_password(new_password)
        pembaca.save()

        messages.success(request, "Password berhasil diperbarui!")
        return redirect('profil')

    return render(request, 'page/ubah_password.html', {'reader_id': reader_id})

