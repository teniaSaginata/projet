from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'    

class Publication(models.Model):
    publication_id = models.AutoField(primary_key=True)
    publication_name = models.CharField(max_length=100)

    def __str__(self):
        return self.publication_name
    
class Book_Data(models.Model):
    title = models.CharField(max_length=255, default=None)
    authors = models.CharField(max_length=255, default=None, null=True)
    genre = models.CharField(max_length=100, default='Unknown')
    language = models.CharField(max_length=255, default=None)
    publication_year = models.PositiveIntegerField(default=2022)
    publisher = models.CharField(max_length=255, default='Unknown Publisher')
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(default='')
    cover_image = models.ImageField(upload_to='coverimages/')

    # For other types of files
    pdf_file = models.FileField(upload_to='pdfs/')
    no_of_copies_actual = models.IntegerField(default=None)
    no_of_copies_current = models.IntegerField(default=None)

    class Meta:
        db_table = 'Book_Data'


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'Author'

    