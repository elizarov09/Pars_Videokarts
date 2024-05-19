import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from shutil import which

class VideokartparsSpider(scrapy.Spider):
    name = "videokartpars"
    allowed_domains = ["citilink.ru"]
    start_urls = ['https://www.citilink.ru/catalog/videokarty/']

    def start_requests(self):
        chrome_options = Options()
        for arg in self.settings.get('SELENIUM_DRIVER_ARGUMENTS'):
            chrome_options.add_argument(arg)
        chrome_service = ChromeService(executable_path=which('chromedriver'))

        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                driver_options=chrome_options,
                driver_service=chrome_service  # Здесь добавляем сервис
            )

    def parse(self, response):
        videokarts = response.css('div.e1ex4k9s0.app-catalog-1bqgmvw.e1loosed0')
        for videokart in videokarts:
            yield {
                'name': videokart.css('div.app-catalog-oacxam a.app-catalog-9gnskf::text').get(),
                'link': response.urljoin(videokart.css('div.app-catalog-oacxam a.app-catalog-9gnskf::attr(href)').get()),
                'price': videokart.css('span.app-catalog-56qww8.e1j9birj0::text').get(),
                'image': videokart.css('div.ep5h2on0 img.is-selected::attr(src)').get(),
            }
