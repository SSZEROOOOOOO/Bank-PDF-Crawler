import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = 'none'	
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "C:\\Users\\Administrator\\Downloads\\gypdf", #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True
 #It will not show PDF directly in chrome
})	

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)


def openPage(driver):
	driver.get("https://mybank.icbc.com.cn/icbc/newperbank/perbank3/frame/frame_index.jsp?serviceId=PBL201131")

def frameJump(driver):
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'perbank-content-frame')))
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'content-frame')))

def resultJump(driver):
#	wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/h6/a"))).click()	#查看全部产品
#	wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[1]/ul/div/div/div[4]/span[2]/span/input")))
	time.sleep(5)
	search_box = driver.find_element_by_xpath("//*[@id='keywords-input']")
	search_box.clear()
	search_box.send_keys("工银理财")
	driver.find_element_by_xpath("//*[@id='keywords']/div/span").click()
	time.sleep(5)

def locatePage(driver):
	global all_pages
	global current_pages
	all_pages = int(driver.find_element_by_xpath('//*[@id="pageturn"]/ul/li[3]/span[2]/b').text)
	current_pages = int(driver.find_element_by_xpath('//*[@id="pageturn"]/ul/li[3]/span[1]/i').text)


def switchPage(driver):
	driver.find_element_by_xpath('//*[@id="pageturn"]/ul/li[4]').click()
	time.sleep(5)

def downloadPdf(driver):
	pdfs=driver.find_elements_by_class_name("ebdp-pc4promote-circularcontainer-title-ellipsis")	
	for pdf in pdfs:
		if '工银理财' in pdf.text and pdf.text not in passed_pdf:
			pdf.click()
			print('downloading',pdf.text)
			passed_pdf.insert(0,pdf.text)
			time.sleep(5)
			current_window = driver.window_handles
			#print(current_window)
			driver.switch_to.window(current_window[1])	
			wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'pdf_iframe_1')))
			wait.until(EC.element_to_be_clickable((By.ID, "open-button"))).click()
			driver.close()
			time.sleep(3)
			driver.switch_to.window(current_window[0])
			frameJump(driver)						

		else:
			continue

	pdfs.clear()

if __name__ == '__main__':
	openPage(driver)
	frameJump(driver)
	resultJump(driver)

	all_pages = int(driver.find_element_by_xpath('//*[@id="pageturn"]/ul/li[3]/span[2]/b').text)
	current_pages = int(driver.find_element_by_xpath('//*[@id="pageturn"]/ul/li[3]/span[1]/i').text)
	passed_pdf = pd.read_excel('../historical_fund/ICBC.xlsx', sheet_name='ALL', index_col=None, header=None)[0].values.tolist()

	locatePage(driver)
	while current_pages < all_pages:
		print('pages:',current_pages,'/',all_pages)
		downloadPdf(driver)
		switchPage(driver)
		#需要时间加载
		locatePage(driver)
	print()
	driver.quit()

	#passed_pdf= []
	dfh = pd.DataFrame(passed_pdf)
	dfh.to_excel('../historical_fund/ICBC.xlsx', sheet_name='ALL', header=False, index=False)