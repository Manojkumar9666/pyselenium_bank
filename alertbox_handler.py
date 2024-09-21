from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import subprocess


def alert_box(driver, explicit_timeout, driver_timeout, max_retry_count, uipath_run=False):
    process_status = True
    counter = 1
    uipath_run = False  # remove this later

    print("Alert Exception Block")

    if uipath_run == True:
        subprocess.call([r"D:\PySelenium\UiPath_Alert_Handler.bat"])
        driver.refresh()

    else:
        while process_status is True:
            try:

                # WebDriverWait(driver, explicit_timeout).until(EC.alert_is_present())
                # Note that despite the name switch_to_alert also handles prompt:
                #   - http://selenium-python.readthedocs.io/navigating.html#popup-dialogs
                # alert = driver.switch_to_alert()
                # text = alert.text
                # print("Alert handler2 is ", text)

                print("Alert box test2 is :", driver.switch_to.alert.text)
                # messagebox.showinfo("showinfo", driver.switch_to.alert.text)
                if ("object" or "session is expired" or "DSC Token") in str(driver.switch_to.alert.text).lower():
                    driver.switch_to.alert.accept()
                    print("Clicked on the alert")

            except Exception as alert_error:
                print("Error2 is :", str(alert_error))

            if counter <= max_retry_count:
                if counter % 2 == 0:
                    time.sleep(driver_timeout)
                else:
                    pass
            else:
                process_status = False

            counter += 1



