# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from gadTo_ryans.items import GadtoRyansItem
from w3lib.html import remove_tags


class RyansSpider(scrapy.Spider):
    name = 'ryans'
    allowed_domains = ['ryanscomputers.com']
    start_urls = [
        'https://ryanscomputers.com/desktop/all-in-one-pc.html',
        'https://ryanscomputers.com/laptop-notebook.html',
        'https://ryanscomputers.com/monitor.html',
        'https://ryanscomputers.com/accessories/keyboard.html',
        'https://ryanscomputers.com/photography/slr-camera.html',
        'https://ryanscomputers.com/network/router.html',
        'https://ryanscomputers.com/smartwatch.html'
    ]

    rules = (
        Rule(LxmlLinkExtractor(allow_domains=allowed_domains)),
    )

    def parse(self, response):
        category_name = response.xpath(".//div[@class='page-title category-title']/h1/text()").extract_first()
        item_links = response.xpath(".//h2[@class='product-name']/a/@href").extract()

        print("=================================================================================")
        print(item_links)
        print("=================================================================================")
        for item_link in item_links:
            yield response.follow(item_link, callback=self.parse_details, meta={'category_name': category_name})
        next_page = response.xpath(".//a[@class='next i-next']/@href").extract_first()
        print("Next Page: ")
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        item = GadtoRyansItem()
        item['website'] = 'Ryans'
        item['gadget_name'] = response.xpath(".//div[@class='product-name']/h2/text()").extract_first().replace('\n', ' ').replace('\r', '')
        item['category_name'] = response.meta.get('category_name')
        item['brand_name'] = response.xpath(
            ".//*[@id='product-attribute-specs-table']/tbody/tr[1]/td/text()").extract_first()
        item['price'] = response.xpath(".//p[@class='special-price']/span/span/text()").extract_first()
        item['image_url'] = response.xpath("//*[@id='image-main']/@src").extract_first()
        item['gadget_url'] = response.request.url
        item['specification'] = remove_tags(response.xpath('//*[@id="product-attribute-specs-table"]').extract_first())
        yield item
