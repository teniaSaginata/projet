from django.db import models
#from django.contrib.auth.models import User as DjangoUser  # Rename to avoid conflicts
from datetime import datetime
from App_Librarian.models import Book_Data  # Import Book_Data from the member app
from django.utils import timezone




class UserDetails(models.Model):
    Name = models.CharField(max_length=300, default=None)
    Phone = models.CharField(max_length=100, default=None)
    Email = models.CharField(max_length=100, default=None)
    Username = models.CharField(max_length=100, default=None)
    Password = models.CharField(max_length=100, default=None)
    Address = models.CharField(max_length=100, default=None)
    City = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)
    Country = models.CharField(max_length=100, null=True, blank=True)
    DateOfBirth = models.DateField(null=True, blank=True)
    Gender = models.CharField(max_length=20, null=True, blank=True)
    
class Loan(models.Model):
    # Define choices for loan status
    LOAN_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('extended', 'Extended'),
    ]

    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_Data, on_delete=models.CASCADE)
    loan_period = models.PositiveIntegerField()  # Duration of the loan in days
    pickup_location = models.CharField(max_length=100)  # Pickup location for the book
    submission_date = models.DateTimeField(default=timezone.now)  # Date and time when the loan was submitted
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='requested')  # Status of the loan
    extended_submission_date = models.DateTimeField(null=True, blank=True)  # Date and time when the loan was extended
    extended_loan_period = models.PositiveIntegerField(default=0)  # Duration of the extended loan period in days


class Notification(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class RatingReview(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_Data, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True)
    review_text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Preference(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)  # Category of preference (e.g., genre, author)
    value = models.CharField(max_length=200)


class Wishlist(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_Data, on_delete=models.CASCADE)