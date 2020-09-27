from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from .serializers import Library_usersSerializer, Book_borrowersSerializer, Library_booksSerializer
from .models import Library_users,Book_borrowers,Library_books


class Library_usersViewSet(viewsets.ModelViewSet):
    queryset = Library_users.objects.all().order_by('name')
    print('===================')
    print(queryset)
    serializer_class = Library_usersSerializer


class Book_borrowersViewSet(viewsets.ModelViewSet):
    queryset = Book_borrowers.objects.all().order_by('user_id')
    print('===================')
    print(queryset)
    serializer_class = Book_borrowersSerializer


class Library_booksViewSet(viewsets.ModelViewSet):
    queryset = Library_books.objects.all().order_by('id')
    print('===================')
    print(queryset)
    serializer_class = Library_booksSerializer