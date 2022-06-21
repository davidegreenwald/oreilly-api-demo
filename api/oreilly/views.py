import json
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

# TODO: Should be a POST request, under auth
@api_view(['GET'])
def refresh_book_database(request):

    api_endpoint = 'https://learning.oreilly.com/api/v2/search'

    query_args = {'query':'python', 'limit':'150', 'field':'title',
      'formats': 'book', 'fields':['title', 'isbn', 'description', 'authors']}
    
    request = requests.get(api_endpoint, params = query_args)
    
    books = request.json()
    
    book_count = len(books['results'])

    for num in range(book_count):
    
        # skip entries with missing fields
        if not 'isbn' in books['results'][num]:
            continue
        elif not 'description' in books['results'][num]:
            continue
        elif not 'authors' in books['results'][num]:
            continue
        elif not 'title' in books['results'][num]:
            continue

        book_title = books['results'][num]['title']
        book_isbn = books['results'][num]['isbn']
        book_desc = books['results'][num]['description']
        book_authors = ', '.join(books['results'][num]['authors'])
        # TODO: handle authors better so they can be individually sorted

        # Check if the ISBN is already in the database before adding it to avoid
        # duplicate data
        book_check = Book.objects.filter(isbn=book_isbn).first()
        if book_check:
            continue

        # Save the API data to the database and continue the loop
        new_book_entry = Book(title=book_title, isbn=book_isbn, 
                              authors=book_authors, description=book_desc)
        new_book_entry.save()

    # return response after the loop completes
    return Response("Searched " + str(book_count) + " entries from the O'Reilly API. New entries have been added to the local database.")

@api_view(['GET'])
def get_all_books(request):

    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_python_books(request):

    books = Book.objects.filter(title__contains='Python')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def get_python_data_science_books(request):

    books = Book.objects.filter(title__contains='Python',
                               title__icontains='data science')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book_by_isbn(request, isbn_num):

    # return a 404 early if the ISBN number isn't 13 digits
    if len(str(isbn_num)) != 13:
        return Response('Not a valid ISBN number', 
                         status=status.HTTP_404_NOT_FOUND)

    # condition passed, continue with the request
    book = Book.objects.filter(isbn=isbn_num).first()
    serializer = BookSerializer(book, many=False)

    if book:
        return Response(serializer.data)
    else:
        return Response('No book found with this ISBN',
                         status=status.HTTP_404_NOT_FOUND)

# TODO - validation and error handling
@api_view(['POST'])
def add_book(request):

    serializer = BookSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
