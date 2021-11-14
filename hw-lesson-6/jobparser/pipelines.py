# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    #def process_item(self, item, spider):
    #    return item

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies_hw6']

    def process_item(self, item, spider):
        if item['salary']:
            item['salary'] = self.edit_salary(item['salary'])

        name = ''.join(item['name'])
        salary_min = item['salary'][0]
        salary_max = item['salary'][1]
        salary_currency = item['salary'][2]
        link = item['url']
        site = item['site']

        vacancy_item = {
            'vacancy_name': name,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': salary_currency,
            'vacancy_link': link,
            'site_scraping': site,
        }

        collection = self.mongo_base[spider.name]
        collection.update_one({'vacancy_link': vacancy_item['vacancy_link']}, {'$set': vacancy_item}, upsert=True)

        return vacancy_item

        #collection.insert_one(item)
        #return item

    #def process_salary(self, salary):
    #    return 1,2,3

    def edit_salary(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        # HHru    Or    SuperJobRu
        if salary[0] == "з/п не указана" or salary[0] == "По договорённости":
            salary_min = "По договорённости" #з/п не указана
            salary_max = None
            salary_currency = None

        elif salary[0] == "до":
            salary_min = None
            salary_max = salary[2]
            salary_currency = salary[-1]

        elif salary[0] == "от" or salary[0] == "от ":
            salary_min = salary[1]
            salary_max = None
            salary_currency = salary[-1]

        elif len(salary) == 3 and salary[0].isdigit():
            salary_min = None
            salary_max = salary[0]
            salary_currency = salary[-1]

        elif len(salary) > 3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]
            salary_currency = salary[-1]

        result = [salary_min, salary_max, salary_currency]
        return result
