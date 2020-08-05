# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class TeacherPipeline:
    def __init__(self):
        self.refer_dict={
            "经济学院":"economics",
            "信息学院":"information",
            "商学院":"business",
            "财政金融学院":"finance",
            "法学院":"legislature",
            "新闻学院":"news"
        }

    def process_item(self, item, spider):
        with open('teachers_{}.json'.format(self.refer_dict[item['department']]),'a',encoding='utf-8') as f:
            line = json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(line)
        return item
            
            
