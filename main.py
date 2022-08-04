# import scrapy
# from scrapy.utils import response
# from scrapy.selector import Selector
#
# class BooksSpider(scrapy.Spider):
#     name = 'books'
#     allowed_domains = ['toscrape.com']
#     start_urls = ['https://igro-grad.ru/catalog/detskiy_transport/10120073/?oid=580201']
#
#     def parse(self, response):
#         table = response.css('table')
#         result = {}
#         for tr in table.css('tr'):
#             row_header = tr.css('th::text').get()
#             row_value = tr.css('td::text').get()
#             result[row_header] = row_value
#         yield result
#
# def main():
#     start_urls = ['https://igro-grad.ru/catalog/detskiy_transport/10120073/?oid=580201']
#     result = {}
#
#     def parse(self, response):
#         table = response.css('table')
#
#         for tr in table.css('tr'):
#             row_header = tr.css('th::text').get()
#             row_value = tr.css('td::text').get()
#             result[row_header] = row_value
#         yield result
#     parse(start_urls)
#     print(result)
#
# # fetch('https://igro-grad.ru/catalog/detskiy_transport/10120073/?oid=580201')
# # name
# response.css('div.element-share-title h1::text').get().strip()
# # detail_text
# response.css('div.detail_text::text').get()
#
# # table description
# res = response.css('div.char_block')
# my_dict2 = {}
# for r in res.css('tr'):
#     w0 = r.css('span::text')[0].get().strip()
#     w1 = r.css('span::text')[1].get().strip()
#     print(w0)
#     print(w1)
#     my_dict2.update({w0: w1})
#
# # Арктикул
# response.css('div.article span::text')[1].get()
# # opt price
# response.css('span.price_value.opt_price::text').get()
# #price
# response.css('span.price_value::text').get()
#
#
# if __name__ == '__main__':
#     main()
#
#
#
#
# [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' detail_text ')]" data='<div class="detail_text"><b>Складной ...'>]
#
# [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' offer_buy_block ') " \
#                  "and (@class and contains(concat(' ', normalize-space(@class), ' '), ' buys_wrapp '))]" data='<div class="offer_buy_block buys_wrap...'>]
# >
#
# # работает не везде
# response.css('span.plus::attr(data-max)').get()
# # response.xpath('//div[@class="counter_block big_basket"]/span/@data-max').get()
#
# # find in massive
# my_str = response.css('div.sku_props script::text').get()
# count_toys = ""
# for m in range(my_str.find('MAX_QUANTITY'), my_str.find('MAX_QUANTITY')+30):
#     if my_str[m].isdigit():
#         count_toys = count_toys + my_str[m]
# print("count_toys",count_toys)

