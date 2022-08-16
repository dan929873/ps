import scrapy


class ToysSpider(scrapy.Spider):
    name = 'IgroGrad3'
    start_urls = ['https://igro-grad.ru/catalog/']

    def parse(self, response):

        # по темам
        for i in range(1, 11):
            link = response.css(f'div.item_block:nth-child({i}) a::attr(href)').get()
            print(link, "   00000000000000")
            yield response.follow(link, callback=self.parse_list)

    def parse_list(self, response):
        mm = response.css('div.item-title a::attr(href)').getall()
        # ссылки по странице на товары
        for link in mm:
            yield response.follow(link, callback=self.parse_toys)

        # по страницам категории
        for i in range(1, int(response.css('div.nums a::text')[-1].get()) + 1):  # количество страниц
            next_page = f'?PAGEN_1={i}'
            print("999999999999  ", next_page)
            yield response.follow(next_page, callback=self.parse_list)

    def parse_toys(self, response):
        # table description
        res = response.css('div.char_block')
        if len(res) > 0:
            par_dict = {}
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
            'count_toys': count_toys,
        }
