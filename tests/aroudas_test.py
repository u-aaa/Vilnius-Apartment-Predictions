import pytest
from scraper.aroudas_scraper import AroudasScraper

def test_num_pages_to_scrape():
    """tests the number of pages to be scraped"""
    a = AroudasScraper()
    assert a._num_result(30) == 2

def test_scraper():
    """tests the aroudas scraper function"""
    a = AroudasScraper()
    scrape = a.scrape(num_houses=2, room_min=1)
    assert scrape.shape == (26, 19)
