import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time


class CitilinkSpider(scrapy.Spider):
    name = "videokartpars"
    allowed_domains = ["citilink.ru"]
    start_urls = ["https://www.citilink.ru/catalog/videokarty/"]

    def __init__(self, *args, **kwargs):
        super(CitilinkSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)

        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

        products = response.css('div[data-meta-name="ProductVerticalSnippet"]')
        self.log(f"Found {len(products)} products")

        for product in products:
            title_element = product.css('a[data-meta-name="Snippet__title"]')
            title = title_element.css('::attr(title)').get()
            link = title_element.css('::attr(href)').get()
            price = product.css('span[data-meta-is-total="notTotal"] span.app-catalog-56qww8::text').get()

            self.log(f"Title: {title}, Link: {link}, Price: {price}")

            if title and price and link:
                yield {
                    'title': title.strip(),
                    'price': price.replace('\u00a0', '').strip(),
                    'link': response.urljoin(link),
                }

        # Переход на следующую страницу, если она существует
        next_page = response.css('a[data-meta-name="NextPageButton"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def closed(self, reason):
        self.driver.quit()