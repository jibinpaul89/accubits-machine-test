# Generated by Django 3.1 on 2020-09-27 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Library_books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=250)),
                ('author', models.CharField(max_length=250)),
                ('Book_count', models.IntegerField()),
            ],
        ),
    ]
