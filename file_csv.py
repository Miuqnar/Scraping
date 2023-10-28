import csv
import os

from constants import DATA_DIR


def save_books_csv(books_category: list[dict]) -> str:
    """Enregistrer toutes les données dans un fichier csv par categorie"""

    if not books_category:
        return "Si la liste[dict] est vide, ne faites rien"

    category_name = books_category[0]['category']  # Récupérer la categorie du premiere livre
    csv_file_path = os.path.join(DATA_DIR, category_name, f"{category_name}.csv")
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)  # si le fichier n'existe pas, on le crée

    book_data_key = [key_boock for dict_boock in books_category for key_boock in dict_boock.keys()]

    with open(csv_file_path, 'w', encoding='UTF8', newline="") as file_csv:
        file = csv.writer(file_csv)
        file.writerow(book_data_key)
        for book in books_category:
            row_data = [book[i] for i in book_data_key]  # en extrair les valeurs des attributs du livre
            file.writerow(row_data)

    return 'Données enregistrées avec succès'
