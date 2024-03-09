import scrapy
import logging
from bs4 import BeautifulSoup

# Инициализируем логгер
logger = logging.getLogger('LinkSpider')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(f"{__name__.split('.')[-1]}.log", mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



class CBRBankSpider(scrapy.Spider):
    name = f"{__name__.split('.')[-1]}_parser"
    start_urls = ['https://cbr.ru/dkp/']
    logger.info(f'{name=}')
    logger.info(f'{start_urls=}')

    def parse(self, response):
        title = response.css('main#content h1 span.referenceable::text').get()
        logger.info(f'{title=}')

        links = response.css('.page-nav_item')
        for link in links:
            href = link.css('a::attr(href)').get()
            text = link.css('a::text').get().strip().replace('\xa0', ' ')

            logger.info(f'{href=}, {text=}')
        
        
        
        
