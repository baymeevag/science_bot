FILE_POSTFIX = '-articles'
FILE_FORMAT = 'csv'
HOST = 'https://cyberleninka.ru/article/c'
DB_LOCATION = 'db'
COLUMNS = ['topic', 'page', 'article_name']
TOPIC = "mathematics"
INTERVAL = 1
PROXIES = [
    "62.210.83.241:8080",
    "163.172.47.182:8080",
    "51.158.123.35:9999",
    "163.172.47.182:3128",
    "51.158.186.242:8761"
]
TERMS = [
    'гомотопии', 
    'диффуры', 
    'дифференциальные уравнения', 
    'теория групп', 
    'гомологии', 
    'изоморфизм'
]
START_TOKEN = '<SOS>'
END_TOKEN = '<EOS>'
