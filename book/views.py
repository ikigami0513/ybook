from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Author


class BookListView(View):
    template_name = "book/list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 25)

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
            "page": page
        })
    