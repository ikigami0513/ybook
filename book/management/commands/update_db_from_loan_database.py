import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from book.models import Book


class Command(BaseCommand):
    help = "Update database from loan database"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent
        with open(os.path.join(base_dir, "..", "..", "..", "dataset", "prets_enregistres_dans_les_mediatheques.json"), "r") as f:
            data = json.load(f)

        rows = data['records']
        for i in range(len(rows)):
            seq_no = rows[i]["seq_no"]
            try:
                book = Book.objects.get(seq_no=seq_no)
            except Book.DoesNotExist:
                print(f"Book {seq_no} does not exists")
                continue

            # On update seulement si l'une des valeurs est différente que celle stockée en base de données
            if book.loans_number != rows[i]["nb_prets"] or rows[i]["duree_moyenne_pret"]:
                book.loans_number = rows[i]["nb_prets"]
                book.average_loan_duration = rows[i]["duree_moyenne_pret"]
                book.save()
            print(f"book {book.title} updated")
            