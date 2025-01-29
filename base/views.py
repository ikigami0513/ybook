from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse


class IndexView(View):
    template_name = "index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)
    