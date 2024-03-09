#!/bin/bash


scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 \
website_parser/website_parser/spiders/cbr_spider.py \
-O "Финансовые рынки.json"


# -O "О Банке России.json"
# -O "Деятельность.json"
