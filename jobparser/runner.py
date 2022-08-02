from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

# from spiders.hhru import HhruSpider
from spiders.labirint import LabirintSpider
# from pipelines import JobparserPipeline

if __name__ == '__main__':
    # jbfd = JobparserPipeline()
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    # runner.crawl(HhruSpider)
    runner.crawl(LabirintSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
