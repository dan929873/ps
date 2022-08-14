import scrapy

class ToysSpider(scrapy.Spider):
    name = 'IgroGrad3'
    start_urls = ['https://igro-grad.ru/catalog/']

    def parse(self,response):

         for i in range(11):
            catalog = response.css(f'div.item_block:nth-child({i}) a::attr(href)').get()
            # Здесь мы находимся на странице каталога - но далее команда думает что мы уже на одной из страниц каталога, как перейти на другую страницу ? похоже как в последнем цикле

            mm = response.css('div.item-title a::attr(href)').getall()

            for link in mm:
                yield response.follow(link, callback=self.parse_toys)

            for i in range(1, int(response.css('div.nums a::text')[-1].get())+1): #количество страниц
                next_page = f'https://igro-grad.ru/{catalog}/?PAGEN_1={i}'
                yield response.follow(next_page, callback=self.parse)


    def parse_toys(self, response):
        # table description
        res = response.css('div.char_block')
        if len(res)>0:
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
            'name':response.css('div.element-share-title h1::text').get().strip(),
            'detail_text':detail_text,
            # table description
            'description':par_dict,
            'number':response.css('div.article span::text')[1].get(),
            'price':response.css('span.price_value::text').get(),
            'count_toys':count_toys,
        }