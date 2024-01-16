import os
import requests

URL = 'https://books.toscrape.com'

PATH_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PATH_DIR, 'data_doc')

SESSION = requests.session()
