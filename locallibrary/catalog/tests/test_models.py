from unittest.util import _MAX_LENGTH
from django.test import TestCase
from catalog.models import Author, Book

# setUpTestData() вызывается каждый раз перед запуском теста на уровне настройки 
# всего класса. Вы должны использовать данный метод для создания объектов, 
# которые не будут модифицироваться/изменяться в каком-либо из тестовых методов.


# setUp() вызывается перед каждой тестовой функцией для настройки объектов, 
# которые могут изменяться во время тестов (каждая функция тестирования будет 
# получать "свежую" версию данных объектов).

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'Имя')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'День смерти')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')
        
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Book.objects.create(title='Red book', summary='Author')


    # test max length
    def test_title_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
        
    def test_summary_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)
        
    def test_isbn_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)
        
    # test field labels
    def test_title_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'Заглавие')

    def test_summary_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEquals(field_label,'Резюме')
        
    def test_isbn_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    # test __str_
    def test_object_name_is_title(self):
        book=Book.objects.get(id=1)
        expected_object_name = '%s' % (book.title)
        self.assertEquals(expected_object_name, str(book))

    # test somewhat method
    def test_get_absolute_url(self):
        book=Book.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(book.get_absolute_url(),'/catalog/book/1')
        

        