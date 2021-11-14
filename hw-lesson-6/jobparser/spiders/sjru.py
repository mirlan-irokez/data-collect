import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru2'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    #def parse(self, response):
    #    pass

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ bs_sM _3ze9n _3xVQu f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[contains(@class,'f-test-vacancy-item')]//a[@target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _185V- _1_rZy dXrZh Ml4Nx']/text()").getall()
        url = response.url
        site = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, url=url, site=site)
