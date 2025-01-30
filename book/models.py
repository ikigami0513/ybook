import uuid
from django.db import models


class PublishingHouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["name"]


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    death = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"

    class Meta:
        ordering = ["first_name", "last_name"]


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seq_no = models.IntegerField()
    title = models.CharField(max_length=512)
    publishing_date = models.CharField(max_length=20, null=True, blank=True)
    reservation_number = models.IntegerField()
    average_age = models.IntegerField(null=True, blank=True)
    female_percent = models.IntegerField(null=True, blank=True)
    male_percent = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True, blank=True)
