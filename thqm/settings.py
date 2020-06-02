from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape


BASE_DIR = Path(__file__).absolute().parent

JINJA_ENV = Environment(
    loader=PackageLoader('thqm', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
    )
