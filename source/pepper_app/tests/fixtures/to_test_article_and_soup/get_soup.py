from selenium import webdriver


driver = webdriver.Chrome()
driver.set_window_size(1400,1000)
driver.get("https://www.pepper.pl/nowe")
time.sleep(0.7)
page = driver.page_source
soup = BeautifulSoup(page, "html5lib")