# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    department = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    phone = scrapy.Field()
    office = scrapy.Field()
    major = scrapy.Field()
    wax = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()
    
