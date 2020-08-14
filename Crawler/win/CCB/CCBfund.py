import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities#

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = 'none'	
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "C:\\Users\\Administrator\\Downloads\\gypdf", #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True
 #It will not show PDF directly in chrome
})	#
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

def openPage(driver):
	link = "http://finance.ccb.com/cn/finance/product.html"
	loading_table = "//*[@id='list1']/table/tbody/tr/td[1]/div/div/a"
	fund_tab = "/html/body/div[9]/div[1]/a[2]"
	status = "//*[@id='status']"
	all_status = "/html/body/div[7]/div/div[2]/ul/div[2]/ul/li[1]/a"
	driver.get(link)
	wait.until(EC.element_to_be_clickable((By.XPATH, loading_table)))
	driver.refresh()
	wait.until(EC.element_to_be_clickable((By.XPATH, loading_table)))
	wait.until(EC.element_to_be_clickable((By.XPATH, fund_tab))).click()
#	wait.until(EC.element_to_be_clickable((By.XPATH, status))).click()
#	wait.until(EC.element_to_be_clickable((By.XPATH, all_status))).click()
#	time.sleep(2)

def locatePage(driver):
	page = "//*[@id='pageNum']"
	global all_pages
	global current_page
	wait.until(EC.element_to_be_clickable((By.XPATH, page)))
	pageN = driver.find_element_by_xpath(page).text
	all_pages = int(re.match("(\d).(\d)",pageN).group(2))
	current_page = int(re.match("(\d).(\d)", pageN).group(1))
	#print(current_page, '/' , all_pages)

def switchPage(driver):
	next_page = "//*[@id='next']"
	wait.until(EC.element_to_be_clickable((By.XPATH, next_page))).click()
	time.sleep(3)

def downloadCondition(current_page, all_pages):
	while current_page <= all_pages:
		print(current_page, ' /', all_pages)
		downloadPdf(driver)
		current_page = current_page +1
		if current_page > all_pages:
			break
		switchPage(driver)

def switchCity(driver):
	sale_city = "//*[@id='saleCitys']/li/a"
	sale_city_selector = "/html/body/div[7]/div/div[2]/ul/div[1]/div"
	city_switch = driver.find_elements_by_xpath(sale_city)
	for city in city_switch:
		downloadCondition(current_page, all_pages)
		wait.until(EC.element_to_be_clickable((By.XPATH, sale_city_selector))).click()
		print('now switch to ',city.get_attribute('textContent'))
		city.click()
		time.sleep(3)

def downloadPdf(driver):
	table = "//*[@id='list6']/table/tbody/tr/td[1]/div/div/a"
	product_info = "/html/body/div[8]/div[3]/div[1]/ul/li[2]/a[2]"
	download_link = "//*[@id='instructionUrl']/p/a"

	pdfs = driver.find_elements_by_xpath(table)
	for pdf in pdfs:
		pdf.click()
		print('downloading', pdf.text)
		time.sleep(5)
		current_window = driver.window_handles
		#print(current_window)
		driver.switch_to.window(current_window[1])
		wait.until(EC.element_to_be_clickable((By.XPATH, product_info))).click()
		wait.until(EC.element_to_be_clickable((By.XPATH, download_link))).click()
		driver.close()
		time.sleep(3)
		print(len(current_window))
		driver.switch_to.window(current_window[0])

	pdfs.clear()


if __name__ == '__main__':
	openPage(driver)
	locatePage(driver)
	switchCity(driver)
	driver.quit()