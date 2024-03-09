import scrapy
# import logging
import requests
from bs4 import BeautifulSoup

# Инициализируем логгер
# logger = logging.getLogger('LinkSpider')
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler(f"{__name__.split('.')[-1]}.log", mode='w')
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


def parse_page(url, title):
    _response = requests.get(url)
    soup = BeautifulSoup(_response.text, 'html.parser')
    text_without_markup = soup.get_text(strip=True).replace('\xa0', ' ').replace("\r\n", ' ')
    start_index = text_without_markup.find(title) + len(title)
    text_without_markup = text_without_markup[start_index:]
    start_index = text_without_markup.find(title) + len(title)
    end_index = text_without_markup.find('Страница была полезной?')
    text_without_markup = text_without_markup[start_index:end_index]
    # logger.info(f'{url=}, {title=}, {text_without_markup=}')
    return text_without_markup



class CBRBankSpider(scrapy.Spider):
    name = f"{__name__.split('.')[-1]}_parser"
    domain = 'https://cbr.ru'
    start_urls = [
        ## Деятельность
        # 'https://cbr.ru/dkp/',
        # 'https://cbr.ru/finstab/',
        # 'https://cbr.ru/PSystem/',
        # 'https://cbr.ru/cash_circulation/',
        # 'https://cbr.ru/develop/',
        # 'https://cbr.ru/fintech/',
        # 'https://cbr.ru/protection_rights/',
        # 'https://cbr.ru/information_security/',
        # 'https://cbr.ru/inside/',
        # 'https://cbr.ru/counteraction_m_ter/',
        # 'https://cbr.ru/admissionfinmarket/',
        # 'https://cbr.ru/business_reputation/',
        # 'https://cbr.ru/ec_research/',
        # 'https://cbr.ru/oper_br/',

        ## Финансовые рынки
        'https://cbr.ru/banking_sector/',
        'https://cbr.ru/RSCI/',
        'https://cbr.ru/insurance/',
        'https://cbr.ru/securities_market/',
        'https://cbr.ru/issuers_corporate/',
        'https://cbr.ru/microfinance/',
        'https://cbr.ru/finm_infrastructure/',
        'https://cbr.ru/ckki/',

        ## О Банке России
        # 'https://cbr.ru/about_br/',
        # 'https://cbr.ru/about_br/ip/',
        # 'https://cbr.ru/about_br/publ/',
        ]
    # logger.info(f'{name=}')
    # logger.info(f'{start_urls=}')

    def parse(self, response):
        title = response.css('main#content h1 span.referenceable::text').get()
        text = parse_page(response.url, title)

        yield {'url': response.url,'title': title,'text': text,}

        links = response.css('.page-nav_item')
        for link in links:
            href = link.css('a::attr(href)').get()
            text = link.css('a::text').get().strip().replace('\xa0', ' ')
            
            _url = self.domain + href
            _title = text
            text_without_markup = parse_page(_url, _title)


            yield {'url': _url,'title': _title,'text': text_without_markup}

