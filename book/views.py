import uuid
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Author


class BookListView(View):
    template_name = "book/list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 24)
        query = request.GET.get("q", "")

        if query:
            books = Book.objects.filter(Q(title__icontains=query))
        else:
            books = Book.objects.all()

        paginator = Paginator(books, per_page)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If the page number is not an integer, display the first page
            page = paginator.page(1)
        except EmptyPage:
            # If the page number is out of range, display the last page
            page = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            "current_page": page_number,
            "max_page": paginator.num_pages,
            "per_page": per_page,
            "page": page,
            "query": query
        })
    

class BookDetailView(View):
    template_name = "book/detail.html"
    
    def get(self, request: HttpRequest, id: uuid.UUID) -> HttpRequest:
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return redirect("book_list")
        
        return render(request, self.template_name, {
            "book": book,
            "current_page": request.GET.get("page", 1),
            "per_page": request.GET.get("per_page", 24),
            "query": request.GET.get("q", "")
        })
    

class AuthorDetailView(View):
    template_name = "author/detail.html"

    def get(self, request: HttpRequest, id: uuid.UUID) -> HttpResponse:
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 24)
        query = request.GET.get("q", "")

        try:
            author = Author.objects.get(id=id)
        except Author.DoesNotExist:
            return redirect("book_list")
        
        return render(request, self.template_name, {
            "author": author,
            "books": author.books.all(),
            "current_page": page_number,
            "per_page": per_page,
            "query": query,
        })
    