from django.urls import path
from . import views

urlpatterns = [
    path('refresh/', views.refresh_book_database),
    path('', views.get_all_books),
    path('python/', views.get_python_books),
    path('python/data-science/', views.get_python_data_science_books),
    path('isbn/<int:isbn_num>',
    views.get_book_by_isbn),
    path('add-book/', views.add_book),
]