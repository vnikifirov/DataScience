from selenium import webdriver

PATH = "C:\ Program Files (X86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.google.com/")