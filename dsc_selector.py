import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def dsc_selector(driver):

    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="approvingmember"]/tbody/tr[1]/td[2]')))

    table_xpath = '//*[@id="approvingmember"]'
    table = driver.find_element(By.XPATH, table_xpath)
    trCount = table.find_elements(By.XPATH, ".//tr")
    print(len(trCount))

    for row_index, row in enumerate(trCount):
        try:
            dsc = driver.find_element(By.XPATH, f'//*[@id="approvingmember"]/tbody/tr[{row_index+1}]/td[2]').text
            if dsc == 'JULIET MOHAN RAYAN':
                driver.find_element(By.XPATH,f'//*[@id="approvingmember"]/tbody/tr[{row_index+1}]/td[1]').click()
                driver.find_element(By.XPATH,f'//*[@id="getCertificates"]').click()
                try:
                    WebDriverWait(driver, 20).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                    status =  False
                except:
                    status = True
                break     
        except Exception as ex:
            pass
    return status
        



        




