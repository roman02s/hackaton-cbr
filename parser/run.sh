#!/bin/bash


scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 \
website_parser/website_parser/spiders/cbr_spider.py \
-O "All.json"


# -O "О Банке России.json"
# -O "Деятельность.json"
# -O "Финансовые рынки.json"
# -O "Вопросы и ответы.json"
# -O "Сервисы.json"
# -O "Решения Банка России, Контактная информация.json"