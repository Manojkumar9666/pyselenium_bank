import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def approval_status_check(driver):

    try:
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="divPendingRecords"]/div[2]')))
        if driver.find_element_by_xpath('//*[@id="divPendingRecords"]/div[2]').text == "No records found for approval.":
            print("No records found for approval.")
            approval_status = False
        else:
            approval_status = True
    except:
        approval_status = True

    print("approval status is : ", approval_status)
    time.sleep(10)
    return approval_status
