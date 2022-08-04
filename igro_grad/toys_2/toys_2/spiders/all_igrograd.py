import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IgroGradSpider(CrawlSpider):
    name = 'all_toys'
    allowed_domains = ['igro-grad.ru']
    start_urls = ['https://igro-grad.ru/catalog']

    rules = (
        # Rule(LinkExtractor(allow='catalog'), follow=True),
        # Rule(LinkExtractor(allow='igrushki'), callback='parse_items'),
        # Rule(LinkExtractor(allow='otdykh_i_sport'), callback='parse_items'),
        # Rule(LinkExtractor(allow='odezhda_i_obuv'), callback='parse_items'),
        # Rule(LinkExtractor(allow='tovary_dlya_detey'), callback='parse_items'),
        # Rule(LinkExtractor(allow='tvorchestvo_i_razvitie'), callback='parse_items'),
        Rule(LinkExtractor(allow=r'detskiy_transport', deny=('odezhda_i_obuv', 'filter', 'velosipedy', 'giroskutery', 'mashiny_katalki_pedalnye_mashiny','elektromobili','samokaty_skutery', 'twitter', 'whatsapp', 'toystown', 'mail', 'vk.com', 'ok.ru', 'facebook', 'skype', 't.me')), callback='parse_items', follow=True),
        # Rule(LinkExtractor(allow='1000_melochey'), callback='parse_items'),
        # Rule(LinkExtractor(allow='prazdniki'), callback='parse_items'),
        # Rule(LinkExtractor(allow='torgovoe_oborudovanie'), callback='parse_items'),
        # Rule(LinkExtractor(allow='letnie_tovary'), callback='parse_items'),
    )

    def parse_items(self, response):
        # table description
        res = response.css('div.char_block')
        par_dict = {}
        if len(res) > 0:

            for r in res.css('tr'):
                w0 = r.css('span::text')[0].get().strip()
                w1 = r.css('span::text')[1].get().strip()
                par_dict.update({w0: w1})

        # count product in site
        count_toys = response.css('span.plus::attr(data-max)').get()
        if str(type(count_toys)) == "<class 'NoneType'>":
            my_str = response.css('div.sku_props script::text').get()
            count_toys = ""
            for m in range(my_str.find('MAX_QUANTITY'), my_str.find('MAX_QUANTITY') + 30):
                if my_str[m].isdigit():
                    count_toys = count_toys + my_str[m]
        # detal text about product
        detail_text = response.css('div.detail_text::text').getall()
        for i in range(len(detail_text)):
            detail_text[i] = str(detail_text[i]).replace('\n', '')

        yield {
            'name': response.css('div.element-share-title h1::text').get().strip(),
            'detail_text': detail_text,
            # table description
            'description': par_dict,
            'number': response.css('div.article span::text')[1].get(),
            'price': response.css('span.price_value::text').get(),
            'count_toys': count_toys
        }
