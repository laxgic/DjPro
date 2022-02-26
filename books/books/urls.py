from django.urls import path

from . import views



urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<uuid:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
]