from datetime import datetime, timedelta
import scrapy
from scrapy.loader import ItemLoader
from guardian.items import GuardianItem


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    start_urls = ["https://www.theguardian.com/au"]

    def __init__(self, num_of_days=2, *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)
        self.num_of_days = self.crawl_day_count = int(num_of_days)

    def parse(self, response):
        primary_tabs = response.xpath(
            '//ul[@class="menu-group menu-group--primary"]/li[@class="menu-item js-navigation-item"]')

        for index, tab in enumerate(primary_tabs):
            # The second tab contains opinions, rather than news, so it's skipped.
            if index != 1:
                category = tab.xpath('./@data-section-name').extract_first()
                for secondary_tab in tab.xpath('ul/li/a'):
                    sub_category = secondary_tab.xpath('./text()').extract_first()
                    sub_category_url = secondary_tab.xpath('./@href').extract_first()
                    date_to_process = datetime.today().date()
                    while self.num_of_days:
                        formatted_date = date_to_process.strftime('%Y/%b/%d').lower()
                        news_url = "{}/{}/all".format(sub_category_url, formatted_date)
                        yield scrapy.Request(
                            response.urljoin(news_url),
                            callback=self.fetch_news_url,
                            meta={
                                'category': category,
                                'sub_category': sub_category,
                                'date': date_to_process
                            }
                        )
                        self.num_of_days -= 1
                        date_to_process = date_to_process - timedelta(days=1)

                    else:
                        self.num_of_days = self.crawl_day_count

    def fetch_news_url(self, response):
        news_links = response.xpath('//div[@class="fc-item__container"]/a/@href').extract()
        for news_link in news_links:
            yield scrapy.Request(
                response.urljoin(news_link),
                callback=self.fetch_news_attributes,
                meta=response.meta
            )

    def fetch_news_attributes(self, response):
        category = response.meta.get('category','')
        sub_category = response.meta.get('sub_category', '')
        creation_date = response.meta.get('date', '')

        item_loader = ItemLoader(item=GuardianItem(), response=response)

        item_loader.add_xpath('headline', '//h1[contains(@class, "content__headline")]//text()')
        item_loader.add_xpath('author', '//a[@rel="author"]/span/text()')
        item_loader.add_xpath('content', '//div[contains(@class, "content__article-body")]//p')
        item_loader.add_value('category', category)
        item_loader.add_value('sub_category', sub_category)
        item_loader.add_value('url', response.url)
        item_loader.add_value('creation_date', creation_date)

        yield item_loader.load_item()

        '''
        yield {
            'headline': response.xpath('//h1[@class="content__headline "]//text()').extract_first().strip(),
            'author': response.xpath('//a[@rel="author"]/span/text()').extract_first().strip(),
            'category': category.strip(),
            'sub_category': sub_category.strip(),
            'url': response.url,
            'creation_date': creation_date.strftime('%Y-%m-%d')
        }
        '''
