# Generated by Django 3.1 on 2020-09-27 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library_books',
            old_name='Book_count',
            new_name='book_count',
        ),
    ]