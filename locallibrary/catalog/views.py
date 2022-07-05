import re
from telnetlib import LOGOUT
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin



# Для формы #######

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm, RenewBookModelForm
####################

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Если вы используете функциональные представления,
# самым простым способом ограничить доступ к вашим функциям является
# применение login_required декоратор к вашей функции просмотра
@login_required
def index(request):
    print(request)
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count() # objects.all() - созданных классов моделей
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    # num_v = ClassV1.objects.count()

    #del request.session['num_visits'] # удаляем значение из сессии
    num_visits = request.session.get('num_visits', 0) # если значения нет, то вернётся значение поумолчанию, т.е. 0
    request.session['num_visits'] = num_visits + 1 # обновляем значение сессии


    # Явное указание, что данные изменены.
    # Сессия будет сохранена, куки обновлены (если необходимо).
    #request.session.modified = True


    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    context = {  # словарь для замещения меток в шаблоне
      'num_books': num_books,
      'num_instances': num_instances,
      'num_instances_available': num_instances_available,
      'num_authors': num_authors,
      'num_visits': num_visits
    }
    return render(request, 'index.html', context)


# Аналогичным образом, самый простой способ ограничить доступ к зарегистрированным
# пользователям в ваших представлениях на основе классов - это производные от LoginRequiredMixin.
# Вы должны объявить этот mixin сначала в списке суперкласса, перед классом основного представления.
class AuthorListView(LoginRequiredMixin, generic.ListView):
    # login_url = 'Нахуй'
    # redirect_field_name = 'redirect_to' 
    model = Author


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list_number_seven'   # ваше собственное имя переменной контекста в шаблоне

    # queryset - атрибут для фильтровки или отбора отбираемых значений
    # queryset = Book.objects.filter(title__icontains='Аниме') # Получение 5 книг, содержащих слово 'love' в заголовке
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Определение имени вашего шаблона и его расположения
    # переопределение метода queryset
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='Аниме')  # Получить 5 книг, содержащих 'war' в заголовке

    # Тут мы переопределяем метод get_context_data у класса, который мы наследуем
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'I\'m fine. Thank you. This is just some data. Version number 12312837913'
        return context



    
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        # return BookInstance.objects.filter(borrower=self.request.user)
        
        
        
class BooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_user.html'
    paginate_by = 10


    def get_queryset(self):
        # return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        return BookInstance.objects.filter(borrower=self.request.user)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    # В отображении аргумент pk мы используем в функцииget_object_or_404() 
    # для получения текущего объекта типа BookInstance (если его не существует, то функция, 
    # а следом и наше отображение прервут своё выполнение, 
    book_inst = get_object_or_404(BookInstance, pk=pk)
    print(f'request: {request}\nprimarykey: {pk}\nbook_inst: {book_inst}')
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required 
            # (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        print(f'proposed_renewal_date: {proposed_renewal_date}')
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(
        request, 
        'catalog/book_renew_librarian.html', 
        {
            'form': form, 
            'bookinst': book_inst
        }
    )




class AuthorCreate(LoginRequiredMixin, CreateView):
    # permission_required = ('catalog.can_mark_returned',)
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12.10.2016',}


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('catalog.can_mark_returned',)
    model = Author
    a = 3
    fields = ['first_name','last_name','date_of_birth','date_of_death']


class AuthorDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('catalog.can_mark_returned',)
    model = Author
    
    success_url = reverse_lazy('authors')
    
# Отображения  "создать" и "обновить" используют  шаблоны с именем model_name_form.html, 
# по умолчанию: (вы можете поменять суффикс на что-нибудь другое, 
# при помощи поля template_name_suffix в вашем отображении, например, 
# template_name_suffix = '_other_suffix')

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    # permission_required = ('catalog.can_mark_returned',)
    # fields = '__all__'
    fields = ['author', 'title', 'summary', 'isbn', 'genre', 'language']
    template_name_suffix = '_forma4ka'
    # initial={'date_of_death':'12/10/2016',}
    
class BookUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('catalog.can_mark_returned',)
    model = Book
    fields = '__all__'



class BookDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('catalog.can_mark_returned',)
    model = Book
    success_url = reverse_lazy('books')















