# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChampionItem(scrapy.Item):
    champion = scrapy.Field()
    role = scrapy.Field()
    champions_that_counter = scrapy.Field()
    champions_that_this_counters = scrapy.Field()
    support_adcs_that_counter = scrapy.Field()
    support_adcs_that_synergize_poorly = scrapy.Field()
    support_adcs_that_this_counters = scrapy.Field()
    support_adcs_that_synergize_well = scrapy.Field()
    adc_supports_that_counter = scrapy.Field()
    adc_supports_that_synergize_poorly = scrapy.Field()
    adc_supports_that_this_counters = scrapy.Field()
    adc_supports_that_synergize_well = scrapy.Field()
