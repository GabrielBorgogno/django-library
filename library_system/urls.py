from django.contrib import admin
from django.urls import include, path
from  library.views import *
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import re_path



 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('home'), name='root'),
    path('/', home, name='home'),
    path('books/', book_list, name='book_list'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),
    path('authors/', authors_view, name='authors'),
    path('books/books/', invalid_url_view_books, name='invalid_url_books'),
    path('books/authors', invalid_url_authors, name='invalid_url_authors'),
    path('accounts/login/authors', invalid_url_authors, name='invalid_url_authors'),
    path('accounts/login/books', invalid_url_view_books, name='invalid_url_view_book'),
    path('authors/authors', invalid_url_authors, name='invalid_url_authors'),
    path('authors/books/', invalid_url_view_books, name='invalid_url_books'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/register/authors', invalid_url_authors, name='invalid_url_authors'),
    path('accounts/register/books',  invalid_url_view_books, name='invalid_url_view_book'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('books/rental_list/', rental_list, name='rental_list'),
    path('rental_list/', rental_list, name='rental_list'),
    path('books/rental_list/books' , invalid_url_view_books, name='invalid_url_authors'),
    path('books/rental_list/authors', invalid_url_authors, name='invalid_url_authors'),
    path('books/rental_form/<int:book_id>/', rental_form, name='rental_form'),
    path('process_rental/', process_rental, name='process_rental'),
    path('rental_confirmation/', rental_confirmation, name='rental_confirmation'),








] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
