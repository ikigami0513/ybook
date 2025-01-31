import uuid
import os
from django.db import models
from django.templatetags.static import static


class PublishingHouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["name"]


def author_picture_file_path(instance: 'Book', filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return os.path.join("authors", "pictures", f"{instance.id}.{uuid.uuid4()}{extension}")



class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    death = models.CharField(max_length=20, null=True, blank=True)
    picture = models.ImageField(upload_to=author_picture_file_path, null=True, blank=True)

    @property
    def get_picture(self) -> str:
        if self.picture:
            return self.picture.url
        return static("author.jpg")

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name"]



def cover_picture_file_path(instance: 'Book', filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return os.path.join("books", "covers", f"{instance.id}.{uuid.uuid4()}{extension}")


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seq_no = models.IntegerField()
    title = models.CharField(max_length=512)
    publishing_date = models.CharField(max_length=20, null=True, blank=True)
    reservation_number = models.IntegerField()
    loans_number = models.IntegerField(default=0)
    average_loan_duration = models.IntegerField(default=0, null=True, blank=True)
    average_age = models.IntegerField(null=True, blank=True)
    female_percent = models.IntegerField(null=True, blank=True)
    male_percent = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True, blank=True)
    cover = models.ImageField(upload_to=cover_picture_file_path, null=True, blank=True)


    def get_cover(self) -> str:
        if self.cover:
            return self.cover.url
        return static("placeholder.webp")
    
    @classmethod
    def random(cls) -> 'Book':
        return cls.objects.order_by("?").first()
