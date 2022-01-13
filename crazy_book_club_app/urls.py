"""Defines URL patterns for crazy_book_club_app."""

from django.urls import path
from .import views


app_name = 'crazy_book_club_app'

urlpatterns = [
    # Home page
    path('', views.index, name = 'index'),

    # List all books
    path('books/', views.books, name = 'books'),

    # Reviews for a book
    path('books/<int:book_id>', views.reviews, name='reviews'),

    # Page to add new book
    path('new_book/', views.new_book, name='new_book'),

    # Page to add new review
    path('new_review/<int:book_id>', views.new_review, name='new_review'),

    # Page for editing a review
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review')
]

