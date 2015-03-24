# -*- coding: utf-8 -*-

# Scrapy settings for championgg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = 'championgg'

SPIDER_MODULES = ['championgg.spiders']
NEWSPIDER_MODULE = 'championgg.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'championgg (+http://www.yourdomain.com)'

FEED_URI = os.path.join(os.getcwd(), 'championgg.json')
FEED_FORMAT = 'json'

LOG_STDOUT = True
LOG_FILE = 'championgg.log'
