from pyexpat import model
from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date



# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField('Заглавие', max_length=200)
    author = models.ForeignKey('Author', verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField('Резюме', max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        print(self.id, [genre.name for genre in self.genre.all()][:3])
        return ', '.join([genre.name for genre in self.genre.all()][:3])

    display_genre.short_description = 'Genre'

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
    
    
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, blank=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # title = models.CharField('adfaf', null=True, blank=True, max_length=10)
    LOAN_STATUS = ( ('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved'), )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    # Определение разрешений выполняется в разделе моделей "class Meta", используется permissions поле
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.book.title)


class ClassV1(models.Model):
    p1 = models.CharField(verbose_name='s22', max_length=100)
    p2 = models.CharField(verbose_name='S22', max_length=100)
    p3 = models.DateField(verbose_name='s33', max_length=100)
    p4 = models.DateField(verbose_name='s44', max_length=100)
    def __eq__():
        return 3
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s, %s, %s' % (self.p1, self.p2, self.p3, self.p4)
print(ClassV1 == 3)

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('День рожденья', null=True, blank=True)
    date_of_death = models.DateField('День смерти', null=True, blank=True)

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        b = reverse('author-detail', args=[str(self.id)])
        print(f"print: {b}")
        return b

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)

# class MyModelName(models.Model):
# """
# A typical class defining a model, derived from the Model class.
# """
# Fields
# my_field_name = models.CharField(max_length=20, help_text="Enter field documentation")
# ...
# # Metadata
# class Meta:
# ordering = ["-my_field_name"]
# Methods
# def get_absolute_url(self):
# """
# Returns the url to access a particular instance of MyModelName.
# """
# return reverse('model-detail-view', args=[str(self.id)])
# def __str__(self):
# """
# String for representing the MyModelName object (in Admin site etc.)
# """
# return self.field_name
# # create a new record using the model's constructor.
# a_record = mymodelname(my_field_name="instance #1")
# print(a_record.id) #should return 1 for the first record.
# print(a_record.my_field_name) # should print 'instance #1'
# # save the object into the database.
# a_record.save()
# all_books = book.objects.all()
# wild_books = book.objects.filter(title__contains='wild')
# number_wild_books = book.objects.filter(title__contains='wild').count()
