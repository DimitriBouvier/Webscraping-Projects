# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:32:32 2022

@author: dimit
"""


import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from pandas import ExcelWriter
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import sys
import re

os.environ["PATH"] = r"C:\Users\dimit\anaconda3\Library\bin"

writer = ExcelWriter(r'C:/Users/dimit/Downloads/LinkedInJobListing{0}.xlsx'.format(datetime.today().strftime('%m%d%y%H%M')))


list_of_jobs = ['data scientist','data analyst','data engineer','machine learning engineer','python developper','data science']
# list_of_jobs = ['french speaking']
list_of_locations = ['new york']#,'san francisco'

mapping_dic = {'data scientist':'DSt',
               'data science':'DSe',
               'data analyst':'DA',
               'data engineer':'DE',
               'machine learning engineer':'MLE',
               'python developper':'PD',
               'new york':'NYC',
               'san francisco':'SF',
               'french speaking':'FP',
               'paris':'prs'}
# print(mapping_dic[city_rol])

for job_rol in list_of_jobs:
    for city_rol in list_of_locations:
        print('looking for {0} positions in {1}'.format(job_rol,city_rol))
        job_df = pd.DataFrame(columns = ['datePosted','title','company','location','link'])
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x4000')
        driver = webdriver.Chrome('chromedriver',options=options)
        # driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        
        driver.get('https://www.linkedin.com/')
        
        driver.find_element_by_xpath("//input[@id='session_key']").send_keys()
        driver.find_element_by_xpath("//input[@id='session_password']").send_keys()
        driver.find_element_by_xpath("//button[@class='sign-in-form__submit-button']").click()
        
        driver.find_element_by_xpath("//a[@id='ember20']").click()
        time.sleep(10)        
        
        
        driver.find_element_by_xpath("//input[@aria-label='Search by title, skill, or company'][1]").send_keys(job_rol)#list_of_jobs[0]
        time.sleep(2)
        driver.find_element_by_xpath("//input[@aria-label='City, state, or zip code'][1]").click()
        driver.find_element_by_xpath("//input[@aria-label='City, state, or zip code'][1]").send_keys(city_rol)#list_of_locations[0]
        time.sleep(2)
        # sys.exit('asc')
        driver.find_element_by_xpath("//input[@aria-label='City, state, or zip code'][1]").send_keys(Keys.ENTER)
        
        # driver.find_element_by_xpath("//button[@type='button' and text() = 'Search']").click()
        # driver.find_element_by_xpath("//button[@type='button' and text() = 'Search']").click()
        time.sleep(10)
        
        #-----addding filters here
        driver.find_element_by_xpath("//button[@aria-label='Job Type filter. Clicking this button displays all Job Type filter options.']").click()
        time.sleep(1)
        # driver.find_element_by_xpath("//span[text()='Part-time']").click()
        
        driver.find_element_by_xpath("//span[text()='Contract']").click()
        
        # driver.find_element_by_xpath("//label[@for='jobType-I']/p/span[text()='Internship']").click()
        # sys.exit('esc')
        driver.find_element_by_xpath("//div[@id='hoverable-outlet-job-type-filter-value']/div/div/div/form/fieldset/div[2]/button[2]").click()
        
        time.sleep(5)
        

        #-----end of adding filters
        
        
        # sys.exit('well well well')

        
        driver.save_screenshot(r'C:\Users\dimit\Downloads\Duηe 2021 1080p WEB-DL x264 6CH-Pahe\ss.png')
        # screenshot = Image.open(‘ss.png’)
        # screenshot.show()
        # try:
        number = len(driver.find_elements_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li"))
        # number_of_pages = int(driver.find_element_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[{0}]".format(number)).get_attribute("data-test-pagination-page-btn"))
        number_of_pages = 40
        current_page_num = 1
        # except NoSuchElementException:
        #     driver.find_element_by_xpath("//button[@type='button' and text() = 'Search']").click()
        #     time.sleep(10)
        #     number = len(driver.find_elements_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li"))
        #     number_of_pages = int(driver.find_element_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[{0}]".format(number)).get_attribute("data-test-pagination-page-btn"))
        #     number_of_pages = 40
        #     current_page_num = 1

        
        for job_tile in driver.find_elements_by_xpath("//ul[@class='jobs-search-results__list list-style-none']/li/div/div"):
            try:
                date_posted = job_tile.find_element_by_xpath(".//ul/li[1]/time").text
                if 'hours' in date_posted:
                    date_posted = 0
                elif 'day' in date_posted:
                    date_posted = int(re.sub('[a-zA-z]','',date_posted))
                elif 'week' in date_posted:
                    date_posted = int(re.sub('[a-zA-z]','',date_posted))*7
                elif 'month' in date_posted:
                    date_posted = int(re.sub('[a-zA-z]','',date_posted))*30
        
            except NoSuchElementException:
                date_posted = ''
            try:
                company = job_tile.find_element_by_xpath(".//div/div[2]/div[2]/a").text
            except NoSuchElementException:
                company = ''
            job_df = job_df.append({'link':job_tile.find_element_by_xpath(".//div/div[2]/div[1]/a").get_attribute("href"),
                                    'title':job_tile.find_element_by_xpath(".//div/div[2]/div[1]/a").text,
                                    'company':company,
                                    'location':job_tile.find_element_by_xpath(".//div/div[2]/div[3]/ul/li[1]").text,
                                    'datePosted':date_posted
                                    }
                                    ,ignore_index=True)
        
        
        
        for page_number in range(2,number_of_pages):
            if page_number != 9:
                try:
                    driver.find_element_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[@data-test-pagination-page-btn='{0}']".format(page_number)).click()
                    time.sleep(15)
                    # driver.save_screenshot(r'C:\Users\dimit\Downloads\Duηe 2021 1080p WEB-DL x264 6CH-Pahe\ss{0}.png'.format(page_number))
                    print(page_number)
                except NoSuchElementException:
                    break
            else:
                driver.find_element_by_xpath("//button[@aria-label='Page 9']").click()
                time.sleep(15)
                # driver.save_screenshot(r'C:\Users\dimit\Downloads\Duηe 2021 1080p WEB-DL x264 6CH-Pahe\ss{0}.png'.format(page_number))
                print(page_number)
            
            for job_tile in driver.find_elements_by_xpath("//ul[@class='jobs-search-results__list list-style-none']/li/div/div"):
                try:
                    date_posted = job_tile.find_element_by_xpath(".//ul/li[1]/time").text
                    if 'hours' in date_posted:
                        date_posted = 0
                    elif 'day' in date_posted:
                        date_posted = int(re.sub('[a-zA-z]','',date_posted))
                    elif 'week' in date_posted:
                        date_posted = int(re.sub('[a-zA-z]','',date_posted))*7
                    elif 'month' in date_posted:
                        date_posted = int(re.sub('[a-zA-z]','',date_posted))*30
                except NoSuchElementException:
                    date_posted = ''
                try:
                    company = job_tile.find_element_by_xpath(".//div/div[2]/div[2]/a").text
                except NoSuchElementException:
                    company = ''
                job_df = job_df.append({'link':job_tile.find_element_by_xpath(".//div/div[2]/div[1]/a").get_attribute("href"),
                                        'title':job_tile.find_element_by_xpath(".//div/div[2]/div[1]/a").text,
                                        'company':company,
                                        'location':job_tile.find_element_by_xpath(".//div/div[2]/div[3]/ul/li[1]").text,
                                        'datePosted':date_posted
                                        }
                                        ,ignore_index=True)
        job_df.to_excel(writer,mapping_dic[job_rol]+'_'+mapping_dic[city_rol], index=False)#list_of_jobs[0]+'_'+list_of_locations[0]
        driver.close()
writer.save()