import os
import re
import requests
import file_csv

from bs4 import BeautifulSoup
from constants import URL, DATA_DIR


def parser_html_content(url: str) -> BeautifulSoup | str:
    """Vérifie si l'URL renvoie une réponse avec le code statut 200 et Returne l'ensemble du contenu de la page HTML"""

    try:
        response_url = requests.get(url)
        if response_url.status_code == 200:
            return BeautifulSoup(response_url.content, 'html.parser')
        else:
            return f"ERROR: Code de statut reçu {response_url.status_code}"
    except Exception as e:
        return f"ERREUR : Problème avec l'URL: {e}"


def extract_book_information(url: str) -> dict:
    """Extration des information d'un livre """

    tags_html = parser_html_content(url)
    data = {
        'category': tags_html.find("a", attrs={"href": re.compile("/category/books/")}).string,
        'title': tags_html.find('div', class_='product_main').find_next('h1').string,
        'price': tags_html.find('p', class_='price_color').string,
        'stock': tags_html.find('p', class_='instock').text.strip(),
        'rating': tags_html.find('p', attrs={'class': 'star-rating'})['class'][-1].strip(),
        'images': tags_html.find('div', attrs={'id': 'product_gallery'}).find('img')['src'].replace('../../', f'{URL}/')
    }
    # assigné tags_html.find(string='Product Description') a la variables description
    if description := tags_html.find(string='Product Description'):
        data['description'] = description.find_next('p').string
    else:
        data['description'] = ''

    product_information = tags_html.find(string='Product Information')
    tables = product_information.find_next('table').find_all('tr')
    for table in tables:
        th, td = [col.text.strip() for col in table.find_all(['th', 'td'])]
        if th and td:
            data[th] = td

    return data


def get_the_page_number(page: str) -> int:
    """Récupérer le nombre de page d'une catégorie"""

    parser_html = parser_html_content(page)
    tags_page = parser_html.find("li", class_="current")
    try:
        if tags_page:
            page_number = int(tags_page.text.split()[-1])
        else:
            page_number = 1
    except Exception as e:
        print(f"ERREUR: lors de l'extraction du nombre de pages - {e}")
        page_number = 1

    return page_number


def get_books_of_category(category_url: str) -> list[dict]:
    """Récupérer tous les livres d'une categorie"""

    books = []

    page_number = get_the_page_number(category_url)
    for page in range(1, page_number + 1):
        if page_number == 1:
            url = category_url
        else:
            url = category_url.replace('index.html', f'page-{page}.html')
        tags_html = parser_html_content(url)
        if isinstance(tags_html, BeautifulSoup):  # isinstance(objeto, informações de classe) return TRUE
            scrape_books_title = tags_html.find_all('h3')
            for book_title in scrape_books_title:
                href = book_title.find_next('a')['href'].strip('../../../')  # récupérer le lien de chaque livre
                book_url_a = f'{URL}/catalogue/{href}'  # chemin pour chaque livre
                books.append(extract_book_information(book_url_a))
    #
    #     # file_csv.save_books_csv(books)
    #
    return books


def get_categories_url(categories_url: str) -> list[str]:
    """Récupérer tous les urls de chaque catégorie"""

    tags_html = parser_html_content(categories_url)
    caterogories_tags_url = tags_html.find('div', {'class': 'side_categories'}).ul.find_all('a')[1:]
    categories = []
    for category_url in caterogories_tags_url:
        href = category_url['href']
        categories.append(f'{URL}/{href}')

    for category in categories:
        file_csv.save_books_csv(get_books_of_category(category))

    return categories


def download_images(url: str) -> bool:
    """ Télécharger tous les images e sauvegarder dans un fichiers localement"""

    categorie_urls = get_categories_url(url)

    for category_url in categorie_urls:
        category_infos = get_books_of_category(category_url)

        for category_info in category_infos:
            category_name = category_info['category']
            csv_file_path = os.path.join(DATA_DIR, category_name, 'images', f"{category_info['title']}.jpg")
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)  # si le fichier n'existe pas on le crée

            all_images = category_info['images']
            pprint(all_images)
            response = requests.get(all_images)  # télécharger l'image

            # Enregistrer l'image dans un fichier binaire
            with open(csv_file_path, 'wb') as image_file:
                image_file.write(response.content)

    return True

