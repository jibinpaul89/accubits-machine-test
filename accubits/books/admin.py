from django.contrib import admin

from books.models import Library_books,Library_users,Book_borrowers

admin.site.register(Library_books)
admin.site.register(Library_users)
admin.site.register(Book_borrowers)
