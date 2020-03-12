# -*- coding: utf-8 -*-
import json
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from quotes.items import QuotesItem
from quotes.spiders.qt import QtSpider


class TestIntegration(object):

    TEST_FEED_URI = "qt_teste.json"

    def setup(self):

        try:
            os.remove(self.TEST_FEED_URI)
        except OSError:
            pass

        self.settings = get_project_settings()
        self.settings.update({
            'CLOSESPIDER_ITEMCOUNT': 15,
            'FEED_URI': self.TEST_FEED_URI
        })

        process = CrawlerProcess(self.settings)
        process.crawl(QtSpider)
        # the script will block here until all crawling jobs are finished
        process.start()

        with open(self.TEST_FEED_URI, 'r') as quotes:
            self.items = json.load(quotes)

    def teardown(self):
        os.remove(self.TEST_FEED_URI)

    def test_scraped_items(self):
        # Check if all items have the right keys
        for item in self.items:
            assert set(item.keys()) == set(QuotesItem.fields.keys())

        expected = {
                "quote": "\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d",
                "author": "Albert Einstein", "author_url": "http://quotes.toscrape.com/",
                "tags": ["change", "deep-thoughts", "thinking", "world"]
            }

        assert expected in self.items
