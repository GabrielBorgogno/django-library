import datetime
import re
import base64
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, RentalForm
from django.views.generic import ListView
from .models import Book, Rental, Author
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def book_list(request):
    books = Book.objects.all()
    rentals = Rental.objects.filter(student=request.user) if request.user.is_authenticated else None
    for rental in rentals:
        rental.days_remaining = (rental.due_date - date.today()).days
    context = {
        'books': books,
        'rentals': rentals,
    }
    return render(request, 'library/book_list.html', context)

@login_required
def rental_details(request, rental_id):
    rental = get_object_or_404(Rental, rental_id=rental_id)
    remaining_days = rental.due_date - date.today() if rental.due_date else None
    context = {
        'rental': rental,
        'remaining_days': remaining_days,
    }
    return render(request, 'library/rental_details.html', context)

@login_required
def process_rental(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rental_days = request.POST.get('rental_days')
        book = Book.objects.get(id=book_id)
        student = request.user

        rental = Rental(
            book_code=book.id,
            book_description=book.title,
            student=student,
            rental_date=date.today(),
            due_date=date.today() + datetime.timedelta(days=int(rental_days)),
            returned='N',
        )
        rental.save()

        return redirect('rental_confirmation')
    else:
        return redirect('book_list')

@login_required
def rental_form(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'library/rental_form.html', context)

@login_required
def rental_list(request):
    rentals = Rental.objects.filter(student=request.user)
    return render(request, 'library/rental_list.html', {'rentals': rentals})

def rental_confirmation(request):
    return render(request, 'library/rent_success.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def invalid_url_view_books(request):
    return redirect('book_list')

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    image_data = book.book_image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return render(request, 'book_detail.html', {'book': book, 'image_base64': image_base64})

def invalid_url_authors(request):
    return redirect('authors')

def invalid_url_rentallist(request):
    return redirect('rental_list')

def home(request):
    return render(request, 'library/home.html')

def switch_page(request):
    base_path = re.sub(r'/[^/]+/$', '/', request.path)  # Remove the last part of the path
    return redirect(base_path)

def authors_view(request):
    category = request.GET.get('category')

    if category == 'authors':
        return switch_page(request)  # Call the switch_page function to handle the redirect

    authors = Author.objects.all()
    context = {'authors': authors}

    return render(request, 'library/authors.html', context)

class RegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
