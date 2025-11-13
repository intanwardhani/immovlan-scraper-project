import scrapy
import pandas as pd
from tqdm import tqdm
from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.internet.interfaces import IReactorTime
from typing import cast
from src.items import ImmovlanItem
import random
import os
import re

class ImmovlanSpider(scrapy.Spider):
    name = 'immovlan'

    def __init__(self, limit=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = int(limit) if limit else None
        self.errors = []
        
        # Load project URLS
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(os.path.dirname(base_dir), "project_urls.csv")
        
        self.urls = pd.read_csv(csv_path)['url'].tolist()
        if self.limit:
            self.urls = self.urls[:self.limit]

        self.progress_bar = tqdm(total=len(self.urls), desc='Projects processed')

        # Error log
        self.error_file = 'output/error_output.csv'
        if not os.path.exists('output'):
            os.makedirs('output')

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse_project, errback=self.errback_handler, meta={'project_url': url})

    def sleep(self, delay, result=None):
        return deferLater(cast(IReactorTime, reactor), delay, lambda: result)

    def parse_project(self, response):
        project_url = response.meta['project_url']
        
        # Find principal properties links
        articles = response.css('div.recommendations-wrapper article.card')
        for article in articles:
            prop_url = article.css('a::attr(href)').get()
            if prop_url:
                yield scrapy.Request(
                    url=prop_url,
                    callback=self.parse_property,
                    errback=self.errback_handler,
                    meta={'project_url': project_url, 'property_url': prop_url}
                )
        
        self.progress_bar.update(1)
        
        # polite random delay without blocking
        delay = random.uniform(1, 3)
        yield self.sleep(delay)
    
    def parse_price(self, texts):
        price_raw = " ".join([t.strip() for t in texts if t.strip()])
        price_clean = (
            price_raw.replace('\u202f', '').replace('\xa0', '').replace('€', '').replace(',', '').strip()
        )
        match = re.search(r'\d+', price_clean.replace(' ', ''))
        return int(match.group()) if match else None

    def parse_property(self, response):
        item = ImmovlanItem()
        item['project_url'] = response.meta['project_url']
        item['property_url'] = response.url

        # Property type and property_id
        header_span = response.css('span.detail__header_title_main')
        header_text = header_span.xpath('text()').get()
        property_type = header_text.strip().split()[0] if header_text else None
        property_id = header_span.css('span.vlancode::text').get()
        property_id = property_id.strip() if property_id else None

        item['property_type'] = property_type
        item['property_id'] = property_id
        
        # Address, locality_name, postal_code
        address_block = response.css('div.detail__header_address div.d-lg-block.d-none')

        if address_block:
            # Get all non-empty text nodes (handles whitespace and newlines)
            texts = address_block.xpath('.//text()[normalize-space()]').getall()
            texts = [t.strip() for t in texts if t.strip()]

            address = postal_code = locality_name = None

            if len(texts) >= 2:
                # First line = address (e.g. "Rue de Bastogne 96")
                address = texts[0]

                # Last line = city line (e.g. "4920 Aywaille" or "1200 Saint-Lambert")
                city_line = texts[-1]

                import re
                match = re.match(r'(\d{4,})\s+([\w\s\-\']+)', city_line)
                if match:
                    postal_code = match.group(1)
                    locality_name = match.group(2).strip()

            item['address'] = address
            item['postal_code'] = postal_code
            item['locality_name'] = locality_name

        else:
            # If the selector didn't match anything
            item['address'] = item['postal_code'] = item['locality_name'] = None

        # Price
        price_texts = response.css('p.detail__header_price span.detail__header_price_data::text').getall()
        item['price'] = self.parse_price(price_texts)

        # General info table
        rows = response.css('div.general-info-wrapper div.data-row')
        for row in rows:
            # header = row.css('h3::text').get()
            for div in row.css('div.data-row-wrapper > div'):
                field_name = div.css('h4::text').get()
                value = div.css('p::text').get()
                if not field_name or not value:
                    continue
                field_name = field_name.strip().lower()
                value = value.strip()
                
                mapping = {
                    'state of the property': 'state',
                    'number of bedrooms': 'number_rooms',
                    'livable surface': 'living_surface',
                    'furnished': 'furnished',
                    'garage': 'garage',
                    'number of garages': 'number_garage',
                    'number of bathrooms': 'number_baths',
                    'floor heating': 'floor_heating',
                    'type of glazing': 'glazing',
                    'elevator': 'elevator',
                    'access for disabled': 'accessibility',
                    'number of facades': 'facade',
                    'number of floors': 'floor',
                    'garden': 'garden',
                    'terrace': 'terrace',
                    'swimming pool': 'swimming_pool'
                }
                
                if field_name in mapping:
                    item[mapping[field_name]] = value

        # Yield the scraped item
        yield item

        # polite random delay after processing this property
        delay = random.uniform(1, 3)
        yield self.sleep(delay)

    def errback_handler(self, failure):
        with open(self.error_file, 'a') as f:
            f.write(str(failure.request.url) + '\n')
    
    def closed(self, reason):
        if self.errors:
            import csv
            with open('output/error_output.csv','w',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['failed_url'])
                for e in self.errors:
                    writer.writerow([e])
