import uuid
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from book.models import Author
import time


class Command(BaseCommand):
    help = "Download author picture from Wikimedia API"

    def handle(self, *args, **options):
        authors = Author.objects.filter(last_name__isnull=False, first_name__isnull=False)

        for author in authors:
            if author.last_name and author.first_name:
                status_code = 0
                trying = 0
                while status_code != 200 and trying < 10:
                    try:
                        print(f"Try download picture for author {author.full_name}")
                        url = "https://en.wikipedia.org/w/api.php"
                        params = {
                            "action": "query",
                            "format": "json",
                            "prop": "pageimages",
                            "piprop": "original",
                            "generator": "search",
                            "gsrsearch": author.full_name,
                            "gsrlimit": 1
                        }

                        response = requests.get(url, params=params)
                        status_code = response.status_code
                        trying += 1
                        if response.status_code == 200:
                            data = response.json()
                            pages = data.get("query", {}).get("pages", {})

                            for page in pages.values():
                                if "original" in page:
                                    picture_url = page["original"]["source"]
                                    picture_data = requests.get(picture_url)
                                    content_type = picture_data.headers.get("Content-Type", "")

                                    if content_type.startswith("image/"):
                                        picture_file = ContentFile(picture_data.content, name=f"{str(uuid.uuid4())}.png")
                                        author.picture = picture_file
                                        author.save()
                                        self.stdout.write(self.style.SUCCESS(f"Picture downloaded for author {author.full_name}"))
                                    else:
                                        self.stdout.write(self.style.ERROR(f"Picture not found for author {author.full_name}"))
                                else:
                                    self.stdout.write(self.style.ERROR(f"Picture not found for author {author.full_name}"))
                    except:
                        self.stdout.write(self.style.WARNING(f"Error for author {author.full_name}"))
                        trying += 1

                    time.sleep(1)
