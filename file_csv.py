import csv
import os

from constants import DATA_DIR


def save_books_csv(books_category: list[dict]) -> str:
    """Enregistrer tous les données dans un fichier csv par categorie"""

    if not books_category:
        return "Si la liste[dict] est vide, ne faites rien"

    category_name = books_category[0]['category']  # Récupérer la categorie du premiere livre
    csv_file_path = os.path.join(DATA_DIR, category_name, f"{category_name}.csv")
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)  # si le fichier n'existe pas on le crée
    #
    book_data = ['title', 'price', 'stock', 'rating', 'images',
                 'description', 'category', 'UPC', 'Product Type',
                 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']

    with open(csv_file_path, 'w', encoding='UTF8', newline="") as file_csv:
        file = csv.writer(file_csv)
        file.writerow(book_data)
        for book in books_category:
            row_data = [book[key] for key in book_data]  # en extrair les valeurs des attributs du livre
            file.writerow(row_data)

    return 'Données enregistrées avec succès'


# if __name__ == '__main__':
#     categor_books = scrapping.get_books_of_category(CATEGORIE_URL)
#     pprint(save_books_csv(categor_books))


