import scrapy
from championgg.items import ChampionItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from selenium import webdriver


class ChampionGgSpider(CrawlSpider):
    name = 'championgg'
    allowed_domains = ['champion.gg']
    start_urls = ['http://champion.gg/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'/champion/\w*/\w*'),), callback='parse_item'),)

    def parse_item(self, response):
        driver = webdriver.PhantomJS()
        self.log('Hi, this is an item page! %s' % response.url)
        driver.set_window_size(1120, 550)
        driver.get(response.url)
        item = ChampionItem()
        champion_css_selector = 'body > div > div > div.page-content > div > div.champion-area.ng-scope > div > div > div.col-xs-12.col-sm-3.col-md-2.champion-profile > h1'
        role_css_selector = 'body > div > div > div.page-content > div > div.champion-area.ng-scope > div > div > div.col-xs-12.col-sm-3.col-md-2.champion-profile > ul > li.selected-role > a > h3'
        champions_that_counter_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div.col-xs-12.col-sm-12.col-md-6.counter-column > matchups > div > div > div.matchup-champion-info > a:nth-child(1) > h3'
        champions_that_this_counters_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div:nth-child(2) > matchups > div > div > div.matchup-champion-info > a:nth-child(1) > h3'
        item['champion'] = driver.find_element_by_css_selector(champion_css_selector).text
        item['role'] = driver.find_element_by_css_selector(role_css_selector).text
        champions_that_counter = [matchup.text for matchup in driver.find_elements_by_css_selector(champions_that_counter_css_selector)]
        champions_that_this_counters = [matchup.text for matchup in driver.find_elements_by_css_selector(champions_that_this_counters_css_selector)]
        if item['role'] == 'Support':
            item['champions_that_counter'] = champions_that_counter[:5]
            item['support_adcs_that_counter'] = champions_that_counter[5:10]
            item['support_adcs_that_synergize_poorly'] = champions_that_counter[10:]
            item['champions_that_this_counters'] = champions_that_this_counters[:5]
            item['support_adcs_that_this_counters'] = champions_that_this_counters[5:10]
            item['support_adcs_that_synergize_well'] = champions_that_this_counters[10:]
        elif item['role'] == 'ADC':
            item['champions_that_counter'] = champions_that_counter[:5]
            item['adc_supports_that_counter'] = champions_that_counter[5:10]
            item['adc_supports_that_synergize_poorly'] = champions_that_counter[10:]
            item['champions_that_this_counters'] = champions_that_this_counters[:5]
            item['adc_supports_that_this_counters'] = champions_that_this_counters[5:10]
            item['adc_supports_that_synergize_well'] = champions_that_this_counters[10:]
        else:
            item['champions_that_counter'] = champions_that_counter
            item['champions_that_this_counters'] = champions_that_this_counters
        driver.quit()
        return item
