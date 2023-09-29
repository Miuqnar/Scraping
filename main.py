import sys

from constants import URL
from scrapping import get_categories_url, download_images


print("""
    Data extraction programme:
        options:
            1 - extract information from books
            2 - download images 
            3 - exit 
    """)


def main(url: str):

    choices = (1, 2, 3)
    choice_input = input("What's your choice ?: ")
    if choice_input.isdigit():
        choice = int(choice_input)
        while choice in choices:
            match choice:
                case 1:
                    return get_categories_url(url)
                case 2:
                    return download_images(url)
                case 3:
                    return f'Bye {sys.exit()}'
                case _:  # default
                    return 'ERREUR'
    else:
        print('Sorry! try again ')


if __name__ == '__main__':
    main(URL)
