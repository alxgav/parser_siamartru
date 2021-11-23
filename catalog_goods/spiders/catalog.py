import scrapy

from bs4 import BeautifulSoup

from ..items import CatalogGoodsItem


def get_content_html(text):
    return BeautifulSoup(text, 'lxml')


def get_links(response, callback):
    for href in response.css('li.one_section a::attr("href")').extract():
        url = response.urljoin(href)
        yield scrapy.Request(url, callback=callback)


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    # allowed_domains = ['siamart.ru/catalog']
    start_urls = ['http://siamart.ru']

    link_url = ('http://siamart.ru/catalog/avtochekhly/',
                'http://siamart.ru/catalog/aksessuary/',
                'http://siamart.ru/catalog/kovry_v_salon_i_bagazhnik/',
                'http://siamart.ru/catalog/mekhovye_nakidki/',
                'http://siamart.ru/catalog/nakidki_na_sideniya/',
                'http://siamart.ru/catalog/opletki_na_rul/',
                'http://siamart.ru/catalog/universalnye_avtochekhly/')

    def start_requests(self):
        link_url = ('http://siamart.ru/catalog/avtochekhly/',)
        for url in link_url:
            yield scrapy.Request(url, callback=self.car_page)

    def car_page(self, response):
        for href in response.css('li.one_section a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.car_page_name)

    def car_page_name(self, response):
        for href in response.css('li.one_section a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.car_page_name2)

    def car_page_name2(self, response):
        for href in response.css('li.one_section a::attr("href")').extract():
            url = response.urljoin(href) + '?SHOWALL_1=1'
            yield scrapy.Request(url, callback=self.get_goods)

    def get_goods(self, response):
        for href in response.css('div.name_product a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = CatalogGoodsItem()
        items['url'] = response.request.url
        items['category'] = get_content_html(response.xpath('/html/body/div[3]/div/div/ul').get()).select_one('ul.breadcrumb-navigation').text.strip().replace('Главная\xa0/\xa0Каталог\xa0/', '')
        items['name'] = response.css('h1.header_grey::text').extract_first('').strip()
        items['description'] = get_content_html(response.xpath('//*[@id="tabs-1"]/div').get()).select_one('div.bx_item_description').text.strip()
        items['price'] = response.css('div.item_current_price::text').extract_first('').strip()
        items['setting'] = get_content_html(response.xpath('//*[@id="tabs-2"]').get()).select_one('div#tabs-2').text.strip().replace('\n\n\n','')
        items['url_image'] = response.css('div.big_img a::attr("href")').extract()
        yield items
