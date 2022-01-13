from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import BookForm, ReviewForm

from .models import Book, Review

# Create your views here.
def index(request):
    """This is the Home page for the Crazy Book Club"""
    return render(request, 'crazy_book_club_app/index.html')


def books(request):
    # Show all books that current user owns
    books = Book.objects.filter(owner=request.user).order_by('date_added')
    context = {'books': books}
    return render(request, 'crazy_book_club_app/books.html', context)


def reviews(request, book_id):
    # Show reviews for a book
    book = Book.objects.get(id=book_id)

    # Make sure the book belongs to the current user
    if book.owner != request.user:
        raise Http404


    reviews = book.review_set.order_by('-date_added')
    context = {'book': book, 'reviews': reviews}
    return render(request, 'crazy_book_club_app/reviews.html', context)

@login_required
def new_book(request):
    # Add new book
    if request.method != 'POST':
        form = BookForm()
    else:
        form = BookForm(data = request.POST)
        if form.is_valid():
            new_book = form.save(commit = False)
            new_book.owner = request.user
            new_book.save()
            return redirect('crazy_book_club_app:books')

    context = {'form': form}
    return render(request, 'crazy_book_club_app/new_book.html', context)

@login_required
def new_review(request, book_id):
    # Add new review of a particular book
    book = Book.objects.get(id = book_id)

    if request.method != 'POST':
        form = ReviewForm()
    else:
        form = ReviewForm(data = request.POST)
        if form.is_valid():
            new_review = form.save(commit = False)
            new_review.book = book
            new_review.save()
            return redirect('crazy_book_club_app:reviews', book_id = book_id)

    context = {'book': book, 'form': form}
    return render(request, 'crazy_book_club_app/new_review.html', context)

@login_required
def edit_review(request, review_id):
    # Edit an existing review
    review = Review.objects.get(id = review_id)
    book = review.book

    # Make sure the review belongs to the current user
    if book.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ReviewForm(instance = review)
    else:
        form = ReviewForm(instance = review, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('crazy_book_club_app:reviews', book_id = book.id)

    context = {'review': review, 'book': book, 'form': form}
    return render(request, 'crazy_book_club_app/edit_review.html', context)

