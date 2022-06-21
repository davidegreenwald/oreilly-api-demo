from django.db import models

class Book(models.Model):

    # watch out for long author and title names
    authors = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    description = models.TextField()
    
    # ISBN numbers are always 13 digits
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title

