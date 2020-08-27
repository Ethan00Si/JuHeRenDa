# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import Compose,Join,MapCompose

def removeNull(value):
    if value and value!='无':
        return value
    else:
        return None

def cleanSpace(string):
    if string:
        return re.sub('\s','',string)
    else:
        return None

class TeacherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    department = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(cleanSpace),
        output_processor=MapCompose(removeNull)
    )
    email = scrapy.Field()
    homepage = scrapy.Field()
    phone = scrapy.Field()
    office = scrapy.Field()
    major = scrapy.Field(
        input_processor=MapCompose(cleanSpace),
        output_processor=MapCompose(removeNull)
    )
    wax = scrapy.Field()
    position = scrapy.Field(
        input_processor=MapCompose(cleanSpace),
        output_processor=MapCompose(removeNull)
    )
    url = scrapy.Field()
    members = scrapy.Field(
        input_processor=MapCompose(cleanSpace)
    )
    lab = scrapy.Field()
    entity = scrapy.Field()