import scrapy
import logging

class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    allowed_domains = ['cbr.ru']  # Замените на ваш домен
    start_urls = ['https://www.cbr.ru/dkp/']  # Замените на ваш стартовый URL

    # Инициализируем логгер
    logger = logging.getLogger('LinkSpider')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('links.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    def parse(self, response):
        # Извлекаем все ссылки на странице и следуем по ним
        for href in response.css('a::attr(href)').extract():
            self.logger.info(f'Найдена ссылка: {href}')
            yield response.follow(href, callback=self.parse_link)

    def parse_link(self, response):
        # При необходимости, здесь можно обработать информацию о странице, например, сохранить ссылки или что-то еще
        pass
