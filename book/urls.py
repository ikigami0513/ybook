from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name="book_list"),
    path('<uuid:id>/', views.BookDetailView.as_view(), name="book_detail"),
    path('author/<uuid:id>/', views.AuthorDetailView.as_view(), name="author_detail")
]
