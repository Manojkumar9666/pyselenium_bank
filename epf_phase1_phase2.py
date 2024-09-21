# =====================================================================================================================>
# Project   : EPFO Automation                                                          Last code changes : 08-07-2021
# Manager   : Shankara Giri G
# Team Leads : Sahil R Kulkarni
# Developer : manojkumar ramisetty
# Email     : manoj.ramisetty@quesscorp.com
# Mobile No : +91 9148146647
# Tools/Tech Used: Python, Selenium, UiPath, Database(mssql)-SP-XML, Regex, Fuzzy, Data Scraping, Excel, .bat files, Firefox
# --------------------------------------------------------------------------------------------------------------------->
# Project Status : Phase 2 - Bug fixes & Optimization
# =====================================================================================================================>
# import pre defined modules
import time
import os
import subprocess
import re


from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import FirefoxProfile
from webdriver_manager.chrome import ChromeDriverManager

from aadhar_pan_approval import aadhar_pan_approval
from selenium.webdriver.support.select import Select
# from tkinter import messagebox
# import developed modules
from config import get_credentials,get_Other_PF_Details
from mailer import send_mail
from alertbox_handler import alert_box
from selenium import webdriver
from call_uirobot import call_uirobot
import pandas as pd
from approval_status_check import approval_status_check
from get_Kill_process import get_kill_process
from db_connect import file_creation
# Code to be executed
rejected= open("C:\\Users\\Bot01\\Desktop\\Bank_rejected_records.csv", 'r+')
rejected.truncate(0)
df = pd.read_excel("D:\PySelenium_bank\PFCodeDetails.xlsx", sheet_name='Sheet1')
print(len(df.index)) #get the rows count of data frame to loop through all the pf codes and do phase1 and phase2


def navigate_to_bank_approvals():

    try:
        options = webdriver.ChromeOptions()
        options.add_extension("C:\\Users\\Bot01\\AppData\\Local\\Programs\\UiPath\\Studio\\UiPath\\BrowserExtension\\uipath_extension_for_chrome.crx")
        service = Service("D:\\PySelenium_bank\\Drivers\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as ex:
        print(ex)
    print("-------------------------------")
    driver.get(r"https://unifiedportal-emp.epfindia.gov.in/epfo")  # Navigating to the URL
    driver.maximize_window()  # Maximizing the window
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="btnCloseModal"]').click()
    process_service_status = False
    driver.implicitly_wait(10)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/h1')))
        if driver.find_element(By.XPATH,'/html/body/h1').text == "503 Service Unavailable":
            print(
                "<<<---------------------------------------503 Service Unavailable---------------------------------------->>>")
            process_service_status = True
            raise Exception(
                "<<<-----------------------503 Service Unavailable, portal is down.------------------------------>>>")
        else:
            process_service_status = False
    except:
        if process_service_status == True:
            raise Exception(
                "<<<---------------------------------503 Service Unavailable, portal is down.---------------------------->>>")
        else:
            print("<<<--------------------------Continuing to login---------------------------------->>>")
            
    driver.implicitly_wait(15)
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(get_Other_PF_Details(login_iter)[0].strip())  # Type into Username get_credentials()[0]
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(str(get_Other_PF_Details(login_iter)[1]).strip())  # Type into Password get_credentials()[1]
    driver.find_element(By.XPATH,'//*[@id="AuthenticationForm"]/div[4]/div[1]/button/span').click()  # Type into Sign In --> Usually time.sleep(1)
    try:  # alert Pop up in case of Failure to load Claims
        # WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' +
        #                              'confirmation popup to appear.')
        # // switch_to.alert
        # for switching to alert and accept
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="alertButtton"]/a')))
        alert_found = True
        print("Alert found")
        if alert_found:
            driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]').click()
    except:
        print("alert does not Exist in page")
    time.sleep(5)# implicit wait is used to wait till all the elements are loaded within the given time
    return driver

# <<<<<----------------------this is defined as function to retry when session expired issue is encountered in the portal
for login_iter in range(0,len(df.index)):
    os.system("taskkill /im firefox.exe /f") #Kill all firefox browsers
    # os.system("taskkill /im chrome.exe /f")  #Kill all chrome browsers
    get_kill_process()  #Kill UiPath processes
    print("Killed all process.")
    try:
        driver = navigate_to_bank_approvals()
        # doc_types = ["Bank", "PAN", "AADHAAR", "Passport", "Driving License", "Election Card", "Ration Card", "National Population Register", "AADHAAR Enrolment Number"]
        doc_types = ["Bank", "PAN", "AADHAAR", "Passport", "Driving License", "Election Card", "Ration Card", "National Population Register", "AADHAAR Enrolment Number"]
        # doc_types = []  # Enable it if you dont want to run phase 2.
        for item in doc_types:
            try:
                if item == doc_types[0]:
                    nav_status = True
                else:
                    nav_status = False
                # The above condition makesures to navigate to the KYC seeded by memeber page only once.
                # try:
                #   if item == "PAN":
                #     driver.find_element(By.XPATH,'//*[@id="gs_uan"]').clear()
                # except:
                #     print("Failed in removing the uan number filter")
                username = str(get_Other_PF_Details(login_iter)[0])
                aadhar_pan_approval(driver=driver, type_text=item, navigation=nav_status, loop_counter_value=10, username=username,limit=20)
                time.sleep(1)
                send_mail("EPFO Digital Signature process - Bulk Approval Status-"+username,
                                                  "Hi Team,\n Process got executed on "+item+" approval.\n\nThanks & Regards \nTeam Automation",
                          admin_status=False)
            except Exception as doc_type_exception:
                send_mail("EPFO Digital Signature process - Bulk Approval Status", "Process got failed due to : " + str(doc_type_exception))

        print("Document types were executed.")

        driver.find_element(By.XPATH,'//*[@id="menu"]/li[2]/a').click()  # Select Member
        driver.find_element(By.XPATH,
            '//*[@id="menu"]/li[2]/ul/li[6]/a').click()  # Select Approvals --> Usually time.sleep(12)

        # time.sleep(1)
        alert_box(driver, explicit_timeout=3, driver_timeout=0.5, max_retry_count=3, uipath_run= True)  # alert handler

        if approval_status_check(driver=driver) == True:
            while re.match(r"View (\d+ - \d+) of",
                           driver.find_element(By.XPATH,'//*[@id="viewMemActivityPager_right"]/div').text) is None:
                time.sleep(0.10)
            # alert_box(driver, explicit_timeout=5, driver_timeout=0.25, max_retry_count=1)  # alert handler
            print("Total rows are: ", len(driver.find_element(By.XPATH,'*//table/tbody/tr')))
            activity_ids = []
            process_status = True
            while process_status is True:
                for i in driver.find_element(By.XPATH,'*//table/tbody/tr'):
                    process_status = False
                    row_id = i.get_attribute('id')
                    activity_selector = f'*//table/tbody/tr[@id={row_id}]/td[1]'
                    type_selector = f'*//table/tbody/tr[@id={row_id}]/td[2]'
                    button_selector = f'*//table/tbody/tr[@id={row_id}]/td[5]/input[1]'
                    if i.get_attribute('id') == "":
                        pass
                        # print("Not a proper row")
                    elif str(i.get_attribute('id')).isnumeric():
                        activity_selector_value = driver.find_element(By.XPATH,activity_selector).get_attribute('title')
                        type_selector_value = driver.find_element(By.XPATH,type_selector).get_attribute('title')
                        button_selector_value = driver.find_element(By.XPATH,button_selector).get_attribute('value')

                        if (str(type_selector_value).lower() == "kyc individual registration" or str(
                                type_selector_value).lower() == "kyc bulk registration" or str(type_selector_value).lower() == "member individual kyc") and str(
                            button_selector_value).lower() == "ds kyc":
                            print("Match Found: Class ID: ", i.get_attribute('id'), " Activity Id: ",
                                  activity_selector_value,
                                  " Type Value: ", type_selector_value, " Button Value: ", button_selector_value)
                            print("Type Selector: ", type_selector, " Button Selector: ", button_selector, end="\n\n")
                            driver.find_element(By.XPATH,button_selector).click()
                            alert_box(driver, explicit_timeout=3, driver_timeout=0.10, max_retry_count=1, uipath_run= False)  # alert handler
                            driver.switch_to.alert.accept()
                            activity_ids.append(activity_selector_value)
                            # driver.switch_to.alert.dismiss()
                            if call_uirobot() == True:
                                pass
                            else:
                                activity_ids.append("<-- Failed : Not able to find 'OK' button of File Uploaded Sucesfully")

                            time.sleep(5)
                            WebDriverWait(driver, 12).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="viewMemActivityPager_right"]/div')))
                            while re.match(r"View (\d+ - \d+) of",
                                           driver.find_element(By.XPATH,
                                               '//*[@id="viewMemActivityPager_right"]/div').text) is None:
                                time.sleep(0.10)
                            if approval_status_check(driver=driver) == True:
                                process_status = True  # Records are found
                                break
                            else:
                                process_status = False
                                break  # (doubt) -> No records to execute.

                        else:
                            pass
                            # print("Row values are not matched: Class ID: ", i.get_attribute('id'))

                    else:
                        pass
                        # print("Class ID is not an integer _ Class ID: ", i.get_attribute('id'))
        else:
            print("No records found for approval (main.py).")
            activity_ids = []

        print("Operation executed on activity id's are ", activity_ids)
        if len(activity_ids) == 0:
            activity_ids.append("'0' --> No records or 0 records found for 'DS KYC'")
        else:
            pass
        send_mail("EPFO Digital Signature process-"+get_credentials(login_iter)[0],
                  "Hi Team,\n Process got executed on the activity ids: " + "-".join(
                      activity_ids) + " which includes both bulk, individual registration.\n\nThanks & Regards \nTeam Automation", admin_status=False)


    except Exception as process_exception:
        send_mail("EPFO Digital Signature process", "Process got failed due to : " + str(process_exception), admin_status= True)
        print("Process got failed due to : ", str(process_exception))





