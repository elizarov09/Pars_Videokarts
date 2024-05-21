BOT_NAME = "videokartpars"

SPIDER_MODULES = ["videokartpars.spiders"]
NEWSPIDER_MODULE = "videokartpars.spiders"

# Настройки для экспорта данных в CSV файл
FEED_FORMAT = 'csv'
FEED_URI = 'output.csv'

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"