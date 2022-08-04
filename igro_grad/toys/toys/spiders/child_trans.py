import scrapy

class ToysSpider(scrapy.Spider):
    name = 'IgroGrad'
    start_urls = ['https://igro-grad.ru']

    def parse(self,response):
        all_link = response.css('div.like_icons a::attr(href)').get()
        link_next = ""
        for m in range(all_link.find('/catalog'), all_link.find('&title')):
            link_next = link_next + all_link[m]
        for link in link_next:
            yield response.foloow(link, callback=self.parse_toys)

            for i in range(1, response.css('div.nums a::text')[-1].get()):
                next_page = f'https://igro-grad.ru/catalog/detskiy_transport/?PAGEN_1={i}'
                yield response.follow(next_page, callback=self.parse)


    def parse_toys(self, response):
        # table description
        res = response.css('div.char_block')
        par_dict = {}
        for r in res.css('tr'):
            w0 = r.css('span::text')[0].get().strip()
            w1 = r.css('span::text')[1].get().strip()
            par_dict.update({w0: w1})

        # count in site
        count_toys = response.css('span.plus::attr(data-max)').get()
        if len(count_toys) == 0:
            my_str = response.css('div.sku_props script::text').get()
            count_toys = ""
            for m in range(my_str.find('MAX_QUANTITY'), my_str.find('MAX_QUANTITY') + 30):
                if my_str[m].isdigit():
                    count_toys = count_toys + my_str[m]
            # print("count_toys: ", count_toys)

        yield {
            'name':response.css('div.element-share-title h1::text').get().strip(),
            'detail_text':response.css('div.detail_text::text').get(),
            # table description
            'description':par_dict,
            'number':response.css('div.article span::text')[1].get(),
            'price':response.css('span.price_value::text').get(),
            'count_toys':count_toys
        }