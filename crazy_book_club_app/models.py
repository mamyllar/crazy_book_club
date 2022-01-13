from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User

from django.db.models.functions import Cast
from django.db.models import TextField

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=200) #Name of the book
    authors = models.JSONField(CharField(max_length=200)) #List of authors
    year_published = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add = True) #Automatically save the date when added
    date_modified = models.DateTimeField(auto_now = True) #Automatically save the date when modified

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    #authors_parsed = Cast("authors", TextField())

    def __str__(self):
        """Return a string representation of the model."""
        return self.name + ", " + str(self.year_published) #+ self.authors_parsed


class Review(models.Model):
    my_review = models.TextField(max_length=1000) #short review
    stars = models.IntegerField() #Given stars, TODO: figure out how to make them 0-5
    unfinished = models.BooleanField() #is the book read completely (False) or partially (True)?

    date_added = models.DateTimeField(auto_now_add = True) #Automatically save the date when added
    date_modified = models.DateTimeField(auto_now = True) #Automatically save the date when modified

    """Foreign key pointing to reviewed book
    on_delete=models.CASCADE is for when book is deleted then review is deleted too"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    def __str__(self):
        """Return a string representation of the model."""

        """If book is unfinished add a comment about it at the start"""
        unfin = "" 
        if self.unfinished == True:
            unfin = "Reviewing while book is unfinished. "

        """The whole return statement"""
        return unfin + str(self.stars) + " stars. Review: " + self.my_review

        #return self.my_review