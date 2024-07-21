from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout
from App_Librarian.models import *
from django.contrib.auth import authenticate, login
#from .forms import UserForm, BookForm, LoanForm, RecommendationForm
from django.contrib import messages
from django.conf import settings
from App_Member.models import *
import os
from datetime import datetime, timedelta

def librarian_home(request):
    username = 'Admin'
    password = 'I@am@admin'
    if not User.objects.filter(username='Admin').exists():
        # Create a new superuser if it doesn't exist
        User.objects.create_superuser(username='Admin', password='I@am@admin')
    return render(request, 'App_Librarian/librarian_home.html', {})


def logout_view(request):
    logout(request)
    return redirect('librarian_home')  

def Admin_Login(request):
    if request.method == "POST":
        A_username = request.POST['aname']
        A_password = request.POST['apass']
        
        # Authenticate user
        user = authenticate(username=A_username, password=A_password)
        
        if user is not None:
            # Login user
            login(request, user)
            messages.info(request, 'Admin login is successful')
            request.session['type_id'] = 'Admin'
            request.session['UserType'] = 'Admin'
            request.session['login'] = "Yes"
            return redirect('librarian_home')
        else:
            messages.error(request, 'Error: Invalid username/password')
            return render(request, 'App_Librarian/Admin_Login.html', {})
    else:
        return render(request, 'App_Librarian/Admin_Login.html', {})
def base(request):
	return render(request,'App_Librarian/base.html',{})

def Manage_Users_View(request):
    users = UserDetails.objects.all()  # Get all user accounts
    return render(request, 'App_Librarian/manage_users.html', {'users': users})



def Manage_Loans_View(request):
    loans = Loan.objects.all()  # Get all book loans
    print(loans)
    for loan in loans:
        if loan.submission_date + timedelta(days=loan.loan_period) < timezone.now():
            loan.loan_status = 'expired'
            loan.save()
    return render(request, 'App_Librarian/manage_loans.html', {'loans': loans})

def Configure_Recommendations_View(request):
    # Logic to retrieve and configure recommendation settings
    return render(request, 'App_Librarian/configure_recommendations.html')

def manage_categories(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, 'App_Librarian/manage_categories.html', {'categories': categories})




def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    categories = Category.objects.all()
    print(categories)
    return render(request, 'App_Librarian/manage_categories.html', {'categories': categories})


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            # Check if the category already exists
            existing_category = Category.objects.filter(category_name=category_name).exists()
            if not existing_category:
                Category.objects.create(category_name=category_name)
                # Redirect to manage_categories view to display the updated list of categories
                categories = Category.objects.all()
                return render(request, 'App_Librarian/manage_categories.html', {'categories': categories})
            else:
                # Category already exists, return an error message or handle it as needed
                error_message = "Category already exists."
                return render(request, 'App_Librarian/add_category.html', {'error_message': error_message})
        return render(request, 'App_Librarian/add_category.html')
    else:
        categories = Category.objects.all()
        print(categories)
        return render(request, 'App_Librarian/manage_categories.html', {'categories': categories})


def manage_publications(request):
    publications = Publication.objects.all()
    return render(request, 'App_Librarian/manage_publications.html', {'publications': publications})

def add_publication(request):
    if request.method == 'POST':
        publication_name = request.POST.get('publication_name')
        if publication_name:
            existing_publication = Publication.objects.filter(publication_name=publication_name).exists()
            if not existing_publication:
                Publication.objects.create(publication_name=publication_name)
                return redirect('manage_publications')
            else:
                error_message = "Publication already exists."
                return render(request, 'App_Librarian/add_publication.html', {'error_message': error_message})
        return render(request, 'App_Librarian/add_publication.html')
    else:
        return render(request, 'App_Librarian/add_publication.html')

def delete_publication(request, publication_id):
    Publication.objects.filter(publication_id=publication_id).delete()
    return redirect('manage_publications')

def manage_authors(request):
    authors = Author.objects.all()
    return render(request, 'App_Librarian/manage_authors.html', {'authors': authors})

def add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        if author_name:
            existing_author = Author.objects.filter(author_name=author_name).exists()
            if not existing_author:
                Author.objects.create(author_name=author_name)
                return redirect('manage_authors')
            else:
                error_message = "Author already exists."
                return render(request, 'App_Librarian/add_author.html', {'error_message': error_message})
        return render(request, 'App_Librarian/add_author.html')
    else:
        return render(request, 'App_Librarian/add_author.html')

def delete_author(request, author_id):
    Author.objects.filter(author_id=author_id).delete()
    return redirect('manage_authors')


def Manage_Books_View(request):
    categories = Category.objects.all()
    publications = Publication.objects.all()
    books = Book_Data.objects.all()  # Get all books
    authors = Author.objects.all()
    return render(request, 'App_Librarian/manage_books.html', {'authors':authors,'books': books, 'categories': categories, 'publications': publications})

def add_book(request):
    if request.method == 'POST':
        # Retrieve data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        publication_year = request.POST.get('publication_year')
        language = request.POST.get('language')
        category = request.POST.get('category')
        publication = request.POST.get('publication')
        authors = request.POST.getlist('authors[]')  # Retrieve multiple selected authors
        authors_string = ', '.join(authors)
        no_of_copies_actual = request.POST.get('no_of_copies_actual')
        no_of_copies_current = request.POST.get('no_of_copies_current')
        pdf_file = request.FILES.get('pdf_file')  # Get uploaded PDF file
        cover_image = request.FILES.get('cover_image')  # Get uploaded cover image
        
        # Save PDF file and cover image to the appropriate directory based on the app
        #pdf_path = os.path.join(settings.MEDIA_ROOT_APP_LIBRARIAN, 'pdfs', pdf_file.name)
        #cover_image_path = os.path.join(settings.MEDIA_ROOT_APP_LIBRARIAN, 'coverimages', cover_image.name)
        
        # with open(pdf_path, 'wb') as pdf_destination:
        #     for chunk in pdf_file.chunks():
        #         pdf_destination.write(chunk)

        # with open(cover_image_path, 'wb') as cover_image_destination:
        #     for chunk in cover_image.chunks():
        #         cover_image_destination.write(chunk)
        
        # Create a new book object
        new_book = Book_Data(
            title=title,
            authors=authors_string,
            description=description,
            publication_year=publication_year,
            language=language,
            genre=category,
            publisher=publication,
            no_of_copies_actual=no_of_copies_actual,
            no_of_copies_current=no_of_copies_current,
            pdf_file=pdf_file,
            cover_image=cover_image
        )
        new_book.save()

        # Redirect to manage_book_details page after adding book
        return redirect('manage_books')
    
    # If not a POST request, render the add book page
    return render(request, 'App_Librarian/add_book.html')

from django.core.files.uploadedfile import InMemoryUploadedFile

def update_book(request, id):
    book = get_object_or_404(Book_Data, pk=id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.authors = request.POST.get('authors')
        book.genre = request.POST.get('genre')
        book.language = request.POST.get('language')
        book.publication_year = request.POST.get('publication_year')
        book.publisher = request.POST.get('publisher')
        book.quantity = request.POST.get('quantity')
        book.description = request.POST.get('description')
        
        # Check if cover image is uploaded
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']
        
        # Check if PDF file is uploaded
        if 'pdf_file' in request.FILES:
            book.pdf_file = request.FILES['pdf_file']
        
        book.no_of_copies_actual = request.POST.get('no_of_copies_actual')
        book.no_of_copies_current = request.POST.get('no_of_copies_current')
        
        book.save()
        return redirect('manage_books')
    
    return render(request, 'App_Librarian/update_book.html', {'book': book})



def delete_book(request, id):
    # Fetch the book to be deleted based on ISBN
    book = Book_Data.objects.get(id=id)
    # Delete the book
    book.delete()
    # Redirect to manage_book_details page after deleting book
    return redirect('manage_books')

def view_books(request, id):
    # Retrieve the book objects from the database using the filter method
    books = Book_Data.objects.all().filter(id=id)
    for book in books:
        print(book.id)
        print(book.cover_image)
    
    # Render the book details template with the books queryset
    return render(request, 'App_Librarian/view_books.html', {'books': books})
from django.contrib import messages

def CreateUserView(request):
    if request.method == 'POST':
        # Extract form data from the request
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        notification_preferences = request.POST.get('notification_preferences')  # Assuming this is a checkbox
        profile_picture = request.FILES.get('profile_picture')  # Assuming profile_picture is an image file
        
        # Additional fields
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        bio = request.POST.get('bio')

        # Check if a user with the same email or username already exists
        if UserDetails.objects.filter(Email=email).exists() or UserDetails.objects.filter(Username=username).exists():
            messages.error(request, 'A user with the same email or username already exists.')
            return render(request, 'App_Librarian/create_user.html')
        
        # Create a new UserDetails object
        user = UserDetails(
            Name=name,
            Phone=phone,
            Email=email,
            Username=username,
            Password=password,
            Address=address,
            City=city,
            State=state,
            Country=country,
            NotificationPreferences=bool(notification_preferences),  # Convert to boolean
            ProfilePicture=profile_picture,
            DateOfBirth=date_of_birth,
            Gender=gender,
            Occupation=occupation,
            Bio=bio,
            MemberSince=datetime.now()
        )

        # Save the user object to the database
        user.save()

        # Redirect to a success page or another view
        return redirect('manage_users')  # Replace 'success_page' with the actual URL name for the success page
    else:
        return render(request, 'App_Librarian/create_user.html')

def EditUserView(request, user_id):
    user = get_object_or_404(UserDetails, pk=user_id)
    if request.method == 'POST':
        # Process form submission
        user.Name = request.POST['name']
        user.Email = request.POST['email']
        user.Phone = request.POST['phone']
        # Update other fields as needed
        user.save()
        # Redirect to a success page or back to the user profile
        return redirect('manage_users')  # Replace 'user_profile' with the actual URL name for user profile
    else:
        return render(request, 'App_Librarian/edit_user.html', {'user': user})

def DeactivateUserView(request, user_id):
    user = get_object_or_404(UserDetails, pk=user_id)
    # Implement your logic for deactivating user account here
    if request.method == 'POST':
        # Process deactivation logic
        pass  # Replace this with your actual logic
    else:
        # Render the confirmation page for deactivating the user account
        return render(request, 'App_Librarian/deactivate_user.html', {'user': user})


def approve_loan(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    # Update loan status to 'issued' or any appropriate status
    loan.loan_status = 'issued'
    loan.save()
    return redirect('manage_loans')

def mark_returned(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    # Update loan status to 'returned'
    loan.loan_status = 'returned'
    loan.save()
    return redirect('manage_loans')

def extend_loan(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    # Logic to extend loan period
    # Example: loan.extended_submission_date = new_date
    # Example: loan.extended_loan_period = new_period
    loan.loan_status = 'extended'
    loan.save()
    return redirect('manage_loans')