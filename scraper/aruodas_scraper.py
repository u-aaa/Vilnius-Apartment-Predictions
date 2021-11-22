from requests_html import HTMLSession
import pandas as pd


class AruodasScraper:
    """
    AroudasScraper - scrapes house data from aroudas and returns a dataframe or csv file.

    Methods
    --------
    _num_results(num_houses:int):
        gets the maximum number of pages for the scraper to scrape
    scrape(num_houses, room_min, room_max):
        Loops through webpages and scrapes data off the aroudas website
    to_csv(df):
        used to save the dataframe to csv
    """

    def __init__(self):
        self.page_number = 1
        self.results = []
        self.url = None

    def search_url(self, no_room: int = None, room_min: int = None, room_max: int = None):
        if no_room is None and room_min is None and room_max is None:
            return f"https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/{self.page_number}/"
        if no_room is not None:
            room_min = no_room
            room_max = no_room
        elif room_min is None:
            room_min = 1
        elif room_max is None:
            room_max = 50
        return f"https://en.aruodas.lt/butu-nuoma/vilniuje/puslapis/{self.page_number}/?FRoomNumMin={room_min}&FRoomNumMax={room_max}"

    @staticmethod
    def load_page(url, **kwargs):
        session = HTMLSession()
        page = session.get(url)
        page_html = page.html
        page_html.render(**kwargs)
        return page_html

    @staticmethod
    def get_links(page_html):
        links = []
        link_container = page_html.find('td.list-adress')
        for item in link_container:
            links.extend(item.absolute_links)
        return links

    @staticmethod
    def load_apartment(page_html):
        page_data = {}
        name_tag = page_html.find("h1.obj-header-text", first=True)
        if name_tag is not None and name_tag.html:
            name = name_tag.text.strip().replace('\n', '').replace(':', '')
            addr = name.split(', ')
            page_data['city'] = addr[0]
            page_data['division'] = addr[1]
            page_data['description'] = name
            page_data['link'] = page_html.url
            table = page_html.find('dl.obj-details', first=True)
            raw = table.text.replace(':', '')
            other_attrs = raw.split('\n')
            for i in range(0, len(other_attrs), 2):
                page_data[other_attrs[i]] = other_attrs[i + 1]

            energy = page_html.find('span.energy-class-tooltip', first=True)
            if energy is not None:
                page_data['energy_class'] = energy.text

            divs = page_html.find('div.statistic-info-cell-main')
            if len(divs) != 0:
                for div in divs:
                    feature = div.text
                    attr = feature.split("\n~ ")
                    page_data[attr[0]] = attr[1]
            return page_data
        return None

    def scrape(self, no_room: int = None, room_min: int = None, room_max: int = None, num_houses: int = 10):
        while len(self.results) < num_houses:
            url = self.search_url(no_room=no_room, room_min=room_min, room_max=room_max)
            landing_page = self.load_page(url)
            if self.page_number == 1 or landing_page.url == url:
                apartment_links = self.get_links(landing_page)
                for link in apartment_links:
                    if len(self.results) < num_houses:
                        page_html = self.load_page(link, scrolldown=6, timeout=80)
                        page_data = self.load_apartment(page_html)
                        if page_data is not None:
                            self.results.append(page_data)
                print(f'Scraped {self.page_number} page(s)')
            self.page_number += 1
        df = pd.DataFrame(self.results, columns=['city', 'division', 'description', 'link', 'House No.', 'Flat No.',
                                                 'Area', 'Price per month', 'Number of rooms ', 'Floor',
                                                 'No. of floors', 'Build year', 'Building type', 'Heating system',
                                                 'energy_class', 'Nearest kindergarten',
                                                 'Nearest educational institution', 'Nearest shop',
                                                 'Public transport stop'])
        print(f'{len(self.results)} results scarped!')
        return df
