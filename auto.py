from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://youtube.com')

searchBox = driver.find_element_by_xpath('//*[@id="search"]')

searchBox.send_keys('Java tutorial')

searchButton = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')

searchButton.click()