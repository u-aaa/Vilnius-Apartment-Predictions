import pytest
import os
from scraper import AruodasScraper
from requests_html import HTML

parent_dir = os.path.dirname(__file__)
landing_file_path = os.path.join(parent_dir, 'local_sites', 'aruodas_landing_page.html')
apartment_path = os.path.join(parent_dir, 'local_sites', 'apartment_page.html')

with open(landing_file_path, 'r', encoding='utf-8') as landing_file:
    landing_content = landing_file.read()
    aruodas_site = HTML(html=landing_content)

with open(apartment_path, 'r', encoding='utf-8') as apartment_file:
    apartment_content = apartment_file.read()
    apartment_site = HTML(html=apartment_content)


def test_search_url_default():
    """tests the url used to laod apartments when room_min, room_max is None"""
    a = AruodasScraper()
    assert a._search_url() == "https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/1/"


def test_search_url_no_room():
    a = AruodasScraper()
    url = a._search_url(no_room=3)
    assert url == "https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/1/?FRoomNumMin=3&FRoomNumMax=3"


def test_search_url_room_min():
    a = AruodasScraper()
    url = a._search_url(room_min=2)
    assert url == "https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/1/?FRoomNumMin=2&FRoomNumMax=50"


def test_search_url_room_max():
    a = AruodasScraper()
    url = a._search_url(room_max=5)
    assert url == "https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/1/?FRoomNumMin=1&FRoomNumMax=5"


def test_get_links():
    links = AruodasScraper._get_links(aruodas_site)
    assert links == ['https://en.aruodas.lt/butai-vilniuje-pasilaiciuose-laisves-pr-4-27818898/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-kalvariju-g-jaukus-ir-pilnai-irengtas-butas-du-atskiri-4-1109887/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-naujamiestyje-savanoriu-pr-isnuomojamas-2-kambariu-butas-su-vilniaus-4-1093623/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-naujamiestyje-kauno-g-isnuomojamas-naujai-irengtas-butas-puikioje-4-1113679/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-konstitucijos-pr-nuo-birzelio-menesio-isnuomojamas-naujas-4-1076045/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-atsilaisvina-nuo-sausio-men-3-d-4-1006667/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-kernaves-g-isnuomojamas-butas-ka-tik-baigtame-statyti-4-1113385/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-atsilaisvina-nuo-sausio-3d-kvieciame-4-1006675/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-atsilaisvina-nuo-gruodzio-7-d-kvieciame-4-1006673/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-laisvas-nuo-gruodzio-7-d-kvieciame-4-1006679/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-pilies-g-ilgalaikei-nuomai-nuomojamas-butas-pilies-4-1101473/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-sv-stepono-g-nuomojamas-butas-vilniaus-senamiescio-4-1111789/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-atsilaisvina-nuo-sausio-3-kvieciame-4-1006665/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-juozo-balcikonio-g-atsilaisvina-nuo-lapkricio-16-d-4-1006669/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-karoliniskese-algimanto-petro-kavoliuko-g-isnuomojamas-naujai-suremontuotas-3-kambariu-4-1109835/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-naujamiestyje-zemaites-g-nuomojamame-bute-yra-visi-baldai-buitine-4-1113269/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-totoriu-g-nuomojamas-itin-erdvus-butas-pacioje-vilniaus-4-1112677/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-snipiskese-slucko-g-chapters-co-living-naujas-busto-nuomos-4-1089669/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-sodu-g-kompaktiskas-gerai-irengtas-studio-butukas-4-928511/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-zveryne-latviu-g-buto-isplanavimas-erdvi-svetaine-sujungta-4-1109771/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-gedimino-pr-isnuomojamas-ka-tik-naujai-irengtas-nuostabus-4-1110711/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-zygimantu-g-last-2-apartments-for-september-april-4-1017813/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-naugarduko-g-jaukus-naujas-butas-naujame-pastate-vilniaus-4-982095/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-universiteto-g-jaukus-naujas-studio-butas-naujai-4-982131/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-universiteto-g-jaukus-naujas-dvieju-kambariu-butas-naujai-4-982139/',
                     'https://en.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-liejyklos-g-isnuomoju-naujai-suremontuota-4-kambariu-3-4-688899/']


def test_load_apartment():
    apartment_details = AruodasScraper._load_apartment(apartment_site)
    assert apartment_details == {'city': 'Vilnius', 'division': 'Šnipiškės',
                                'description': 'Vilnius, Šnipiškės, Konstitucijos pr., 2 rooms flat for rent',
                                'link': 'https://example.org/', 'House No.': '15', 'Area': '64 m²',
                                'Price per month': '1 050 €', 'Number of rooms ': '2', 'Floor': '5',
                                'No. of floors': '29', 'Build year': '2019', 'Building type': 'Monolithic',
                                'Heating system': 'Central thermostat', 'Equipment': 'Fully equipped'}
