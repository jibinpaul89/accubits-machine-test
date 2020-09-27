from rest_framework import serializers

from .models import Library_users, Book_borrowers, Library_books


class Library_usersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_users
        fields = ('name', 'email','password','status')


class Library_booksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_books
        fields = ('book_name','author','book_count')

class Book_borrowersSerializer(serializers.HyperlinkedModelSerializer):
    Library_books = Library_booksSerializer(many=True, read_only=True)
    Library_users = Library_usersSerializer(many=True, read_only=True)
    class Meta:
        model = Book_borrowers
        fields = '__all__'


