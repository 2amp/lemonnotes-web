from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import json
import time


def parse_item(link, driver):
    print 'Parsing ' + link
    item = {}
    driver.get(link)
    champion_css_selector = 'body > div > div > div.page-content > div > div.champion-area.ng-scope > div > div > div.col-xs-12.col-sm-3.col-md-2.champion-profile > h1'
    role_css_selector = 'body > div > div > div.page-content > div > div.champion-area.ng-scope > div > div > div.col-xs-12.col-sm-3.col-md-2.champion-profile > ul > li.selected-role > a > h3'
    champions_that_counter_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div.col-xs-12.col-sm-12.col-md-6.counter-column > matchups > div > div > div.matchup-champion-info > a:nth-child(1) > h3'
    champions_that_this_counters_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div:nth-child(2) > matchups > div > div > div.matchup-champion-info > a:nth-child(1) > h3'
    champions_that_counter_win_rates_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div.col-xs-12.col-sm-12.col-md-6.counter-column > matchups > div > div > div.winrating-area > strong'
    champions_that_this_counters_win_rates_css_selector = 'body > div > div > div.page-content > div > div.matchups > div > div.row.counter-row > div:nth-child(2) > matchups > div > div > div.winrating-area > strong'
    item['champion'] = driver.find_element_by_css_selector(champion_css_selector).text
    item['role'] = driver.find_element_by_css_selector(role_css_selector).text
    champions_that_counter = [matchup.text for matchup in driver.find_elements_by_css_selector(champions_that_counter_css_selector)]
    champions_that_this_counters = [matchup.text for matchup in driver.find_elements_by_css_selector(champions_that_this_counters_css_selector)]
    champions_that_counter_win_rates = [float(matchup.text.strip('%')) for matchup in driver.find_elements_by_css_selector(champions_that_counter_win_rates_css_selector)]
    champions_that_this_counters_win_rates = [float(matchup.text.strip('%')) for matchup in driver.find_elements_by_css_selector(champions_that_this_counters_win_rates_css_selector)]
    if item['role'] == 'Support':
        item['champions_that_counter'] = [list(a) for a in zip(champions_that_counter[:5], champions_that_counter_win_rates[:5])]
        item['support_adcs_that_counter'] = [list(a) for a in zip(champions_that_counter[5:10], champions_that_counter_win_rates[5:10])]
        item['support_adcs_that_synergize_poorly'] = [list(a) for a in zip(champions_that_counter[10:], champions_that_counter_win_rates[10:])]
        item['champions_that_this_counters'] = [list(a) for a in zip(champions_that_this_counters[:5], champions_that_this_counters_win_rates[:5])]
        item['support_adcs_that_this_counters'] = [list(a) for a in zip(champions_that_this_counters[5:10], champions_that_this_counters_win_rates[5:10])]
        item['support_adcs_that_synergize_well'] = [list(a) for a in zip(champions_that_this_counters[10:], champions_that_this_counters_win_rates[10:])]
    elif item['role'] == 'ADC':
        item['champions_that_counter'] = [list(a) for a in zip(champions_that_counter[:5], champions_that_counter_win_rates[:5])]
        item['adc_supports_that_counter'] = [list(a) for a in zip(champions_that_counter[5:10], champions_that_counter_win_rates[5:10])]
        item['adc_supports_that_synergize_poorly'] = [list(a) for a in zip(champions_that_counter[10:], champions_that_counter_win_rates[10:])]
        item['champions_that_this_counters'] = [list(a) for a in zip(champions_that_this_counters[:5], champions_that_this_counters_win_rates[:5])]
        item['adc_supports_that_this_counters'] = [list(a) for a in zip(champions_that_this_counters[5:10], champions_that_this_counters_win_rates[5:10])]
        item['adc_supports_that_synergize_well'] = [list(a) for a in zip(champions_that_this_counters[10:], champions_that_this_counters_win_rates[10:])]
    else:
        item['champions_that_counter'] = [list(a) for a in zip(champions_that_counter, champions_that_counter_win_rates)]
        item['champions_that_this_counters'] = [list(a) for a in zip(champions_that_this_counters, champions_that_this_counters_win_rates)]
    return item


def scrape():
    start_time = time.time()
    p = re.compile(r'/champion/\w+/\w+')
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    r = requests.get('http://champion.gg')
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text)
        links = list(set(['http://champion.gg' + link.get('href') for link in soup.find_all('a') if p.match(link.get('href'))]))
        items = [parse_item(link, driver) for link in links]
        with open('championgg.json', 'w') as f:
            f.write(json.dumps(items))
    driver.quit()
    time_taken = time.time() - start_time
    print 'Scraped ' + str(len(items)) + ' items in ' + str(time_taken) + ' s (' + str(len(items) / time_taken) + 'items/s)'

if __name__ == '__main__':
    scrape()
