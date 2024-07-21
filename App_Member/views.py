from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *
from App_Librarian.models import *
from datetime import timedelta
from django.shortcuts import get_object_or_404
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Q

def home(request):
    
    return render(request, 'App_Member/home.html', {})
  
def base(request):
    return render(request, 'App_Member/base.html')


def rate_review_book(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    user_id = request.session['UserId']
    user = get_object_or_404(UserDetails, id=user_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('reviewText')
        
        # Create or update the RatingReview object
        RatingReview.objects.update_or_create(
            user=user,
            book=loan.book,
            defaults={'rating': rating, 'review_text': review_text}
        )
        
        # Assuming the loan status changes after submitting the review
        loan.status = 'returned'
        loan.save()
        
        return redirect('home')  # Redirect to the home page after submission

    return render(request, 'rating_review_modal.html', {'loan': loan})

def Registeration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        phone = request.POST.get('Phone')
        date_of_birth = request.POST.get('DateOfBirth')
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        address = request.POST.get('Address')
        city = request.POST.get('City')
        state = request.POST.get('State')
        country = request.POST.get('Country')
        Gender = request.POST.get('gender')

        # Create an instance of the UserProfile model and save it to the database
        user_profile = UserDetails(
            Name=name,
            Email=email,
            Phone=phone,
            Gender = Gender,
            DateOfBirth=date_of_birth,
            Username=username,
            Password=password,
            Address=address,
            City=city,
            State=state,
            Country=country
        )
        user_profile.save()

        # Return a success message (you can customize this)
        return redirect('login')

    # If the request method is not POST, render the registration form template
    return render(request, 'App_Member/Registeration.html')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('aname')
        password = request.POST.get('apass')
        print(username, password)
        
        if UserDetails.objects.filter(Username=username, Password=password).exists():
            user = UserDetails.objects.get(Username=username, Password=password)
            messages.info(request, f"{username} logged in")
            request.session['UserId'] = user.id
            request.session['type_id'] = 'User'
            request.session['UserType'] = username

            request.session['login'] = "Yes"
            messages.info(request, 'Logged In Successfully')
            return redirect('Catalog_Browsing')
        else:
            messages.error(request, 'Please Register')
            return redirect('Registeration')
    else:
        return render(request, 'App_Member/login.html') # Replace 'your_app/login.html' with the actual path to your login HTML template


def User_Profile(request):
    # Your user profile logiApp_Member/c goes here
    return render(request, 'App_Member/User_Profile.html')


def Catalog_Browsing(request):
    # Fetch all categories, genres, authors, and books
    categories = Category.objects.all()
    authors = Author.objects.all()
    books = Book_Data.objects.all()
    publications = Publication.objects.all()

    # Get user ID from session
    user_id = request.session.get('UserId')
    print(user_id)
    recommended_books = []
    if user_id:
        recommended_books = get_user_recommendations(user_id)
        print(recommended_books)

    return render(request, 'App_Member/Catalog_Browsing.html', {
        'publications': publications,
        'categories': categories,
        'authors': authors,
        'books': books,
        'recommended_books': recommended_books
    })

def manage_categories(request):
    # Your manage categories logic goes here
    return render(request, 'App_Member/manage_categories.html')

def Book_Details(request, id):
    # Retrieve the book object from the database using the filter method
    book = get_object_or_404(Book_Data, id=id)
    
    # Check if 'UserId' exists in the session
    if 'UserId' in request.session:
        user_id = request.session['UserId']
        user = get_object_or_404(UserDetails, id=user_id)
        in_wishlist = Wishlist.objects.filter(user=user, book=book).exists()
        print(in_wishlist)
    else:
        in_wishlist = False
    
    # Render the book details template with the book object and in_wishlist flag
    return render(request, 'App_Member/Book_Details.html', {'book': book, 'in_wishlist': in_wishlist})

def loan_request(request):
    if request.method == 'POST':
        # Get data from the loan request form
        book_id = request.POST.get('book_id')
        user_id = request.session['UserId']
        loan_period = int(request.POST.get('loan_period'))

        loan_start_date = datetime.now()  # Example loan start date (replace this with actual loan start date)
        last_date_of_loan = loan_start_date + timedelta(days=loan_period)

        # Check if the book is available for loan
        try:
            book = Book_Data.objects.get(id=book_id)
            if book.no_of_copies_current > 0:
                # Create a loan request entry
                loan = Loan.objects.create(book=book, user_id=user_id, loan_period=loan_period,submission_date = last_date_of_loan)
                # Update the availability status of the book
                book.no_of_copies_current -= 1
                book.save()
                print('success')
                # Send a confirmation message to the user
                messages.success(request, f"Loan request for {book.title} has been successfully submitted.")

                user_id = request.session['UserId']
                user_loans = Loan.objects.all().filter(user_id = user_id)
                # Render the loan request form
                return render(request, 'App_Member/loan_request.html',{'user_loans':user_loans})
                #return render(request, 'App_Member/loan_request.html')  # Redirect to success page
            else:
                # Notify the user that the book is not available
                messages.error(request, "Sorry, the book is not available for loan at the moment.")
                return redirect('home')  # Redirect to failure page
        except Book_Data.DoesNotExist:
            # Handle case where the book does not exist
            messages.error(request, "Sorry, the requested book does not exist.")
            return redirect('Catalog_Browsing')  # Redirect to an error page
    else:
        user_id = request.session['UserId']
        user_loans = Loan.objects.all().filter(user_id = user_id)
        # Render the loan request form
        return render(request, 'App_Member/loan_request.html',{'user_loans':user_loans})


def User_Profile(request):
    user_id = request.session['UserId']
    
    if request.method == 'POST':
        if user_id:
            # Retrieve user details from the form
            name = request.POST.get('Name')
            phone = request.POST.get('Phone')
            email = request.POST.get('Email')
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            address = request.POST.get('Address')
            city = request.POST.get('City')
            state = request.POST.get('State')
            country = request.POST.get('Country')
            date_of_birth = request.POST.get('DateOfBirth')
            gender = request.POST.get('Gender')

            # Retrieve the user object to update
            user = get_object_or_404(UserDetails, id=user_id)
            
            # Update user profile with the new data
            user.Name = name
            user.Phone = phone
            user.Email = email
            user.Username = username
            user.Password = password
            user.Address = address
            user.City = city
            user.State = state
            user.Country = country
            user.DateOfBirth = date_of_birth
            user.Gender = gender
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('User_Profile')
        else:
            messages.error(request, 'User session ID not found.')
            return redirect('login')  # Redirect to login page if user ID not found
    else:
        if user_id:
            print(user_id)
            # Retrieve user details to pre-fill the form
            user = UserDetails.objects.filter(id=user_id)
            return render(request, 'App_Member/User_Profile.html', {'user': user})
        else:
            messages.error(request, 'User session ID not found.')
            return redirect('login')  # Redirect to login page if user ID not found

def browse_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    books = Book_Data.objects.filter(genre=category.category_name)
    if not books:
        return HttpResponse("No data available for this category", status=404)
    
    user_id = request.session['UserId']  # Assuming you store user_id in the session
    if user_id:
        Preference.objects.get_or_create(user_id=user_id, category='Genre', value=category.category_name)
    
    return render(request, 'App_Member/browse_category.html', {'category': category, 'books': books})

def browse_author(request, author_id):
    author = get_object_or_404(Author, author_id=author_id)
    books = Book_Data.objects.filter(authors=author.author_name)
    if not books:
        return HttpResponse("No data available for this author", status=404)
    
    user_id = request.session['UserId']  # Assuming you store user_id in the session
    if user_id:
        Preference.objects.get_or_create(user_id=user_id, category='Author', value=author.author_name)
    
    return render(request, 'App_Member/browse_author.html', {'author': author, 'books': books})

def browse_publisher(request, publication_id):
    publisher = get_object_or_404(Publication, publication_id=publication_id)
    books = Book_Data.objects.filter(publisher=publisher.publication_name)
    if not books:
        return HttpResponse("No data available for this publisher", status=404)
    
    user_id = request.session['UserId']  # Assuming you store user_id in the session
    if user_id:
        for book in books:
            Preference.objects.get_or_create(user_id=user_id, category='Publisher', value=publisher.publication_name)
    
    return render(request, 'App_Member/browse_publisher.html', {'publisher': publisher, 'books': books})

def search_results(request):
    query = request.POST.get('query')
    print(query)
    if query:
        # Retrieve titles and descriptions of all books
        books = Book_Data.objects.all()
        titles = [book.title for book in books]
        descriptions = [book.description for book in books]
        
        # Concatenate titles and descriptions
        all_text = [title + ' ' + desc for title, desc in zip(titles, descriptions)]
        
        # Tokenize and preprocess the query
        query_tokens = word_tokenize(query)
        query_tokens = [word.lower() for word in query_tokens if word.isalnum()]
        query = ' '.join(query_tokens)
        
        # Preprocess concatenated text
        all_text_tokens = [word_tokenize(text) for text in all_text]
        all_text_tokens = [' '.join([word.lower() for word in tokens if word.isalnum()]) for tokens in all_text_tokens]
        
        # Calculate TF-IDF vectors for query and concatenated text
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([query] + all_text_tokens)
        query_vector = tfidf_matrix[0]
        text_vectors = tfidf_matrix[1:]
        
        # Calculate cosine similarity between query and concatenated text
        similarity_scores = cosine_similarity(query_vector, text_vectors)[0]
        
        # Sort books by similarity score
        books = sorted(zip(books, similarity_scores), key=lambda x: x[1], reverse=True)
        books = [book[0] for book in books if book[1] > 0]  # Filter out books with similarity score of 0
        
        return render(request, 'App_Member/search_results.html', {'books': books})
        
    else:
        books = Book_Data.objects.all()
        return render(request, 'App_Member/search_results.html', {'books': books})
def get_user_recommendations(user_id):
    # Get the user's rated books
    rated_books = RatingReview.objects.filter(user_id=user_id)

    # Get the books currently loaned by the user
    loaned_books = Loan.objects.filter(user_id=user_id, loan_status='issued')

    # Get the user's wishlist
    wishlist_books = Wishlist.objects.filter(user_id=user_id)

    # Get user's preferences
    user_preferences = Preference.objects.filter(user_id=user_id)

    # Combine all book IDs from the above sources and remove duplicates
    excluded_book_ids = set(
        list(rated_books.values_list('book_id', flat=True)) +
        list(wishlist_books.values_list('book_id', flat=True)) +
        list(loaned_books.values_list('book_id', flat=True))
    )
    print(excluded_book_ids)

    # Get recommended books based on user preferences
    recommended_books = Book_Data.objects.exclude(id__in=excluded_book_ids)
    print(recommended_books)
    for preference in user_preferences:
        recommended_books = recommended_books.filter(Q(genre=preference.value) | Q(authors=preference.value))

    return recommended_books

def request_extension(request, loan_id):
    # Retrieve the loan object
    print(loan_id)
    loan = get_object_or_404(Loan, pk=loan_id)

    if request.method == 'POST':
        # Process the extension request form submission
        extension_days = int(request.POST.get('extension_days'))
        
        # Update the loan details
        loan.extended_loan_period = extension_days
        loan.extended_submission_date = datetime.now()
        loan.loan_status = 'extended'  # Update loan status
        loan.save()

        # Notify the user that the extension request has been submitted
        messages.success(request, "Extension request submitted successfully.")
        
        # Redirect to a success page or another view
        return redirect('home')  # Replace 'home' with the actual URL name
        
    # Render the extension request form
    return render(request, 'extension_request.html', {'loan': loan})


def preferences(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        selection = request.POST.get('selection')

        # Save user preferences to the database
        preference = Preference(category=category, selection=selection)
        preference.save()

        # You can also associate preferences with the current user if you have user authentication
        # preference.user = request.user
        # preference.save()

        # Redirect to a success page or render another template
        return redirect('home')
    else:
        authors = Author.objects.all()
        publisher = Publication.objects.all()
        genre = Category.objects.all()
        return render(request, 'App_Member/preferences.html',{'authors':authors,'publisher':publisher,'genre':genre})



def fetch_selections(request):
    category = request.GET.get('category')
    selections = []

    if category == 'Author':
        selections = [author.name for author in Author.objects.all()]
    elif category == 'Publisher':
        selections = [publisher.name for publisher in Publication.objects.all()]
    elif category == 'Genre':
        selections = [genre.name for genre in Category.objects.all()]

    return JsonResponse(selections, safe=False)



def add_to_wishlist(request, book_id):
    user_id = request.session['UserId']
    if user_id:
        user = get_object_or_404(UserDetails, pk=user_id)
        book = get_object_or_404(Book_Data, pk=book_id)
        Wishlist.objects.get_or_create(user=user, book=book)
        return redirect('Book_Details', id=book_id)
    else:
        # Handle the case where user_id is not found in the session
        # For example, redirect the user to the login page or show an error message
        return redirect('login')  # Redirect to the login page

def remove_from_wishlist(request, book_id):
    try:
        # Get the user ID from the session
        user_id = request.session['UserId']
        
        # Check if the user is authenticated
        if user_id:
            # Get the user and book objects
            user = get_object_or_404(UserDetails, pk=user_id)
            book = get_object_or_404(Book_Data, pk=book_id)
            
            # Get the wishlist item
            wishlist_item = Wishlist.objects.filter(user=user, book=book).first()
            
            # Check if the wishlist item exists
            if wishlist_item:
                # Delete the wishlist item
                wishlist_item.delete()
                
            # Redirect to the book details page
            return redirect('Book_Details', id=book_id)
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect('login')
    except KeyError:
        # Handle the case where the 'UserId' key is not found in the session
        # Redirect to an appropriate page or show an error message
        return redirect('login')

def wishlisted_books(request):
    user_id = request.session.get('UserId')
    if user_id:
        wishlisted_books = Wishlist.objects.filter(user_id=user_id).select_related('book')
        return render(request, 'App_Member/wishlisted_books.html', {'wishlisted_books': wishlisted_books})
    else:
        # Handle the scenario where the user is not authenticated or the user ID is not in the session
        return render(request, 'App_Member/wishlisted_books.html', {'wishlisted_books': []})

