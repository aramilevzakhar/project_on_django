from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, ClassV1

# Register your models here.


# Тут идёт регистрация созаднных моделей
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


@admin.register(ClassV1)
class ClassV1(admin.ModelAdmin):
    list_display = ('p1', 'p2', 'p3', 'p4')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# Добавили поле borrower
# Это сделает поле видимым в разделе Admin, так что мы можем при необходимости назначить User в BookInstance.
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ("anime anime", {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
