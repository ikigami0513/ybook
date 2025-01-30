from django.contrib import admin
from .models import *


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [BookInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "birth", "death"]
    inlines = [BookInline]
    search_fields = ["last_name", "first_name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "seq_no"]
