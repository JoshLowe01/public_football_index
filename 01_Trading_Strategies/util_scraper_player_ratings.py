from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

''' 
Web driver to scrape player ratings data

Data will be in the downloads folder and called 'Table Data.csv'

'''

def web_driver_scrapper():
    # Data Pull from FI edge
    driver = webdriver.Chrome()
    driver.get('https://members.footballindexedge.com/member/sign_in')

    ## Give time for iframe to load ##
    time.sleep(3)

    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("password")

    username.clear()
    username.send_keys("Avi.sethi01@gmail.com")
    password.clear()
    password.send_keys("DollarsForTheBoys")

    driver.find_element_by_name("commit").click()

    driver.get("https://www.footballindexedge.com/price-master-q3-2019")
    time.sleep(20)
    # driver.find_element_by_css_selector('div.button.downloadCsv btn-warning downloadButton').click()
    driver.find_element_by_xpath("//*[@id='block-yui_3_17_2_1_1562137191774_3739']/div/div[1]/button[1]").click()
    time.sleep(20)