from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Library_books(models.Model):
    book_name=models.CharField(max_length=250,null=False)
    author=models.CharField(max_length=250,null=False)
    book_count = models.IntegerField(null=False)
    def __str__(self):
        return self.book_name


class Library_users(models.Model):
    name=models.CharField(max_length=250,null=False)
    email=models.CharField(max_length=250,null=False)
    password = models.CharField(max_length=250,null=False)
    #status = models.IntegerField(null=False)
    INACTIVE = 0
    ACTIVE = 1
    STATUS = (
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
    )
    status = models.IntegerField(default=0, choices=STATUS)
    def __str__(self):
        return self.name


class Book_borrowers(models.Model):
    book_id=models.ForeignKey('Library_books',on_delete=models.CASCADE)
    user_id=models.ForeignKey('Library_users',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.book_id)



