import scrapy

# scrapy shell "https://igro-grad.ru/catalog/aktsii/"
# scrapy crawl IgroGradtestURL -O IgroGradtestURL.csv

class ToysSpider(scrapy.Spider):
    name = 'IgroGradtestURL'
    allowed_domains = ['igro-grad.ru']
    start_urls = ['https://igro-grad.ru/catalog/kantstovary/',
                  'https://igro-grad.ru/catalog/igrushki/',
                  'https://igro-grad.ru/catalog/otdykh_i_sport/',
                  'https://igro-grad.ru/catalog/odezhda_i_obuv/',
                  'https://igro-grad.ru/catalog/tovary_dlya_detey/',
                  'https://igro-grad.ru/catalog/tvorchestvo_i_razvitie/',
                  'https://igro-grad.ru/catalog/detskiy_transport/',
                  'https://igro-grad.ru/catalog/1000_melochey/',
                  'https://igro-grad.ru/catalog/prazdniki/',
                  'https://igro-grad.ru/catalog/torgovoe_oborudovanie/',
                  'https://igro-grad.ru/catalog/novoe_postuplenie/']
    # start_urls = ['https://igro-grad.ru/catalog/kantstovary/',]

    def parse(self,response):

        mm = response.css('div.item-title a::attr(href)').getall()

        for link in mm:
            yield response.follow(link, callback=self.parse_toys)

        for i in range(1, int(response.css('div.nums a::text')[-1].get())+1):
            # нужно сделать строку с категорией и страницей
            next_page = (f'{str(response)[5:str(response).find("/", 35)]}/?PAGEN_1={i}')
            print("----------", next_page)
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

        way = str(response)[str(response).find("catalog") + len("catalog/"):]

        yield {
            'category':way[:way.find("/")],
            'name':response.css('div.element-share-title h1::text').get().strip(),
            'detail_text':detail_text,
            # table description
            'description':par_dict,
            'number':response.css('div.article span::text')[1].get(),
            'price':response.css('span.price_value::text').get(),
            'count_toys':count_toys,
        }


