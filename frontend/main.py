from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("yourapp"), autoescape=select_autoescape())
