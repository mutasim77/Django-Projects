# Generated by Django 4.1.6 on 2023-04-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_book_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(help_text='The genre of the book.', max_length=70, null=True),
        ),
    ]
