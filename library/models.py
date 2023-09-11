from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

class Author(models.Model):
    name = models.CharField(max_length=100)
    min_estimated_sales = models.CharField(max_length=50,default='')
    max_estimated_sales = models.CharField(max_length=50, default='')
    original_language = models.CharField(max_length=50,default='')
    genre_or_major_works = models.CharField(max_length=200, default='')
    number_of_books = models.IntegerField(default='0')
    nationality = models.CharField(max_length=50,default='')







from django.db import models
from django.contrib.auth.models import User
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_image = models.ImageField(upload_to='book_images/', default='blank.png')
    launch_year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000)

    def author_name(self):
        return self.author.name

    def get_available_count(self):
        return Rental.objects.filter(book_code=self.pk, returned='0').count()

    class Meta:
        app_label = 'library'


class Rental(models.Model):
    rental_id = models.IntegerField(primary_key=True)
    book_code = models.IntegerField()
    book_description = models.CharField(max_length=50)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_date = models.DateField()
    rental_duration = models.IntegerField(default=0)
    due_date = models.DateField(default=datetime.date.today)
    returned = models.CharField(max_length=1)


    
    def save(self, *args, **kwargs):
        # Calculate due date based on rental date and duration
        if self.rental_date and self.rental_duration:
            self.due_date = self.rental_date + datetime.timedelta(days=self.rental_duration)
        super(Rental, self).save(*args, **kwargs)