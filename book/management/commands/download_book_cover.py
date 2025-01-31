import uuid
import requests
from difflib import SequenceMatcher
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from book.models import Book
import time


class Command(BaseCommand):
    help = "Download book cover from Google Book"

    def handle(self, *args, **options):
        books = Book.objects.all()
        book_instance = Book.objects.get(seq_no=621010)
        books = list(books)
        index = books.index(book_instance)
        books = books[index+1:]

        for book in books:
            status_code = 0
            trying = 0
            while status_code != 200 and trying < 10:
                try:
                    if not book.cover:
                        print(f"Try download cover for book {book.title}")
                        base_url = f"https://www.googleapis.com/books/v1/volumes?q={book.title}+intitle&maxResults=10"

                        response = requests.get(base_url)
                        status_code = response.status_code
                        trying += 1

                        if response.status_code == 200:
                            data = response.json()
                            items = data.get("items", [])

                            for item in items:
                                title = item.get("volumeInfo", {}).get("title", "").lower()
                                if self.string_similar(book.title.lower(), title):
                                    image_url = item.get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail", "")
                                    if image_url != "":
                                        image_data = requests.get(image_url)
                                        if image_data.status_code == 200:
                                            image_file = ContentFile(image_data.content, name=f"{str(uuid.uuid4())}.png")
                                            book.cover = image_file
                                            book.save()
                                            self.stdout.write(self.style.SUCCESS(f"Cover downloaded for book {book.title}"))
                                        else:
                                            self.stdout.write(self.style.ERROR(f"Error while downloading cover for book {book.title}"))
                                        break
                            self.stdout.write(self.style.ERROR(f"No cover founded for book {book.title}"))
                        
                        time.sleep(1)
                    else:
                        status_code = 200
                        trying = 10
                except:
                    self.stdout.write(self.style.WARNING(f"[Connection Error] Connection aborted, reset by peer"))
                    trying += 1

    def string_similar(self, one: str, two: str, threshold: float = 0.7) -> bool:
        ratio = SequenceMatcher(None, one, two).ratio()
        return ratio >= threshold
