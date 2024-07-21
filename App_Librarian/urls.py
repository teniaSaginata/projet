from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.librarian_home,name = 'librarian_home'),
    path('base/',views.base,name = 'base'),
    path('users/', views.Manage_Users_View, name='manage_users'),
    path('books/', views.Manage_Books_View, name='manage_books'),
    path('loans/', views.Manage_Loans_View, name='manage_loans'),
    path('Admin_Login/', views.Admin_Login, name='Admin_Login'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('add_category/', views.add_category, name='add_category'),

    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    path('manage_publications/', views.manage_publications, name='manage_publications'),
    path('add_publication/', views.add_publication, name='add_publication'),
    path('delete_publication/<int:publication_id>/', views.delete_publication, name='delete_publication'),
    path('manage_authors/', views.manage_authors, name='manage_authors'),
    path('add_author/', views.add_author, name='add_author'),
    path('delete_author/<int:author_id>/', views.delete_author, name='delete_author'),


    path('recommendations/', views.Configure_Recommendations_View, name='configure_recommendations'),
    path('logout/', views.logout_view, name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    path('view_books/<int:id>/', views.view_books, name='view_books'),
    path('update_book/<int:id>/', views.update_book, name='update_book'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('create-user/', views.CreateUserView, name='create_user'),
    path('edit-user/<int:user_id>/', views.EditUserView, name='edit_user'),
    path('deactivate-user/<int:user_id>/', views.DeactivateUserView, name='deactivate_user'),
    path('approve_loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('mark_returned/<int:loan_id>/', views.mark_returned, name='mark_returned'),
    path('extend_loan/<int:loan_id>/',views.extend_loan, name='extend_loan'),
    # Other URL patterns for Librarian/Administrator modules...
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

