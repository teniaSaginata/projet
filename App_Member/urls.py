# urls.py in App_Member

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name = 'home'),
    path('base/',views.base,name = 'base'),
    path('Registeration/', views.Registeration, name='Registeration'),
    path('login/', views.login, name='login'),
    path('User_Profile/', views.User_Profile, name='User_Profile'),
    path('Book_Details/<int:id>', views.Book_Details, name='Book_Details'),
    path('Catalog_Browsing/', views.Catalog_Browsing, name='Catalog_Browsing'),
    #path('search/', views.search_books, name='search_books'),
    path('loan_request/', views.loan_request, name='loan_request'),
    path('browse_category/<int:category_id>', views.browse_category, name='browse_category'),
    path('browse_author/<int:author_id>', views.browse_author, name='browse_author'),
    path('rate_review_book/<int:loan_id>/', views.rate_review_book, name='rate_review_book'),
    path('search_results/',views.search_results, name='search_results'),
    path('request_extension/<int:loan_id>/', views.request_extension, name='request_extension'),
    path('preferences/', views.preferences, name='preferences'),
    path('browse_publisher/<int:publication_id>', views.browse_publisher, name='browse_publisher'),
    path('wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlisted-books/', views.wishlisted_books, name='wishlisted_books'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    