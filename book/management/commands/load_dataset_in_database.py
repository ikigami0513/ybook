import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from typing import Optional

from book.models import PublishingHouse, Author, Book


class Command(BaseCommand):
    help = "Loads data from json file into database"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent
        with open(os.path.join(base_dir, "..", "..", "..", "dataset", "reservations_enregistrees_dans_les_mediatheques.json"), "r") as f:
            data = json.load(f)

        # keys :
        #     - numberMatched
        #     - numberReturned
        #     - records
        #     - links
        rows = data['records']
        for i in range(len(rows)):
            seq_no = rows[i]["seq_no"]
            title = rows[i]["titre"]
            publishing_date = rows[i]["date_publication"]
            reservation_number = rows[i]["nb_reservations"]
            average_age = rows[i]["moyenne_age"]
            publishing_house_set = self.parse_publishing_house(rows[i]["adresse"])
            gender_set = self.parse_gender(rows[i]["repartition_sexes"])
            author_set = self.parse_author(rows[i]["auteur"])

            publishing_house = PublishingHouse.objects.get_or_create(
                name=publishing_house_set
            )[0] if publishing_house_set else None

            male_percent = gender_set["M"] if gender_set else None
            female_percent = gender_set["F"] if gender_set else None

            try:
                author = Author.objects.get_or_create(**author_set)[0] if author_set else None
            except Author.MultipleObjectsReturned:
                author = None

            try:
                existing_book = Book.objects.get(seq_no=seq_no, title=title)
                print(f"Book {title} already exists")
            except Book.DoesNotExist:
                book = Book.objects.create(
                    seq_no=seq_no,
                    title=title,
                    publishing_date=publishing_date,
                    reservation_number=reservation_number,
                    average_age=average_age,
                    female_percent=female_percent,
                    male_percent=male_percent,
                    author=author,
                    publishing_house=publishing_house
                )
                print(f"Book {title} created.")

    def parse_publishing_house(self, publishing_house: Optional[str]) -> Optional[str]:
        if publishing_house is None:
            return None
        
        publishing_house = publishing_house.split(" : ")
        if len(publishing_house) > 1:
            publishing_house = publishing_house[1].split(",")[0]
        else:
            return None

    def parse_gender(self, gender: Optional[str]) -> dict[str, int]:
        if gender is None:
            return None
        
        gender = gender.split(", ")
        gender_set = {}
        for i in range(len(gender)):
            data = gender[i].split(" ")
            gender_set[data[0]] = data[1].split("(")[1].split("%)")[0]

        if "F" not in gender_set:
            gender_set["F"] = 0
        if "M" not in gender_set:
            gender_set["M"] = 0

        return gender_set


    def parse_author(self, author: Optional[str]) -> dict[str, Optional[str]]:
        if author is None:
            return None 
        
        print(author)
        
        data = author.split(" ")
        author_set = {}
        if len(data) > 1:
            data[0] = data[0][:-1]

        author_set['last_name'] = data[0]

        if len(data) == 2:
            data2 = data[1].split("-")
            if len(data2) == 1:  # first name
                author_set['first_name'] = data2[0]
            elif len(data2) == 2 and data2[0][0].isdigit() and data2[0][2].isdigit():  # birth date and death date
                author_set['birth'] = data2[0].replace("?", "")
                author_set['death'] = data2[1] if data2[1].replace("?", "") != "...." else None
            elif len(data2) == 2:
                author_set['first_name'] = f"{data2[0]}-{data2[1]}"
            else:
                pass

        elif len(data) >= 3:
            author_set['first_name'] = data[1]
            date = data[2].split("-")
            if len(date) > 1:
                author_set["birth"] = date[0].replace("?", "")

            if len(date) > 2:
                author_set["death"] = date[1] if date[1].replace("?", "") != "...." else None

        return author_set
