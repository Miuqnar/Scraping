import datetime
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
    """ Saisi de l'utilisateur """

    while True:
        choices = "1, 2, 3"
        choice_input = input("What's your choice ?: ")

        if choice_input not in choices:
            print("S'il vous plaît saisissez un numéro valide entre (1) et (3)")
        else:
            choice = int(choice_input)
            match choice:
                case 1:
                    return get_categories_url(url)
                case 2:
                    return download_images(url)
                case 3:
                    print('Bye')
                    return sys.exit()
                case _:  # default
                    return 'ERREUR'
    # else:
    #     print('Sorry! try again ')


if __name__ == '__main__':
    main(URL)
