import time
import os
import subprocess
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import FirefoxProfile
from aadhar_pan_approval import aadhar_pan_approval
from selenium.webdriver.support.select import Select
# from tkinter import messagebox
# import developed modules
from config import get_credentials
from mailer import send_mail, send_mail_with_attachment
from alertbox_handler import alert_box
from selenium import webdriver
from call_uirobot import call_uirobot
from approval_status_check import approval_status_check
from get_Kill_process import get_kill_process
from db_connect import file_creation
import pandas as pd
import shutil
from datetime import datetime



# Code to be executed

# os.system("taskkill /im firefox.exe /f") #Kill all firefox browsers
# os.system("taskkill /im chrome.exe /f")  #Kill all chrome browsers
get_kill_process()  #Kill UiPath processes
print("Killed all process.")
directory = r"D:\PySelenium\Errors"
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : directory}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=r'D:\PySelenium\Drivers\Test\chromedriver.exe',chrome_options=chromeOptions)

#
try:
      send_mail("EPFO Digital Signature process KYC Upload", "Process has started.", admin_status= True)
      driver.implicitly_wait(15)
      driver.get(r"https://unifiedportal-emp.epfindia.gov.in/epfo/")
      driver.implicitly_wait(15)
      driver.maximize_window()
      process_service_status = False

      try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/h1')))
        if driver.find_element_by_xpath('/html/body/h1').text == "503 Service Unavailable":
            print("503 Service Unavailable")
            process_service_status = True
            raise Exception("503 Service Unavailable, portal is down.")
        else:
            process_service_status = False

      except:

        if process_service_status == True:
            raise Exception("503 Service Unavailable, portal is down.")
        else:
            print("Continuing to login")

      driver.implicitly_wait(15)
      driver.find_element_by_xpath('//*[@id="username"]').send_keys(get_credentials()[0])  # Type into Username
      driver.find_element_by_xpath('//*[@id="password"]').send_keys(get_credentials()[1])  # Type into Password
      driver.find_element_by_xpath(
        '//*[@id="AuthenticationForm"]/div[4]/div[1]/button/span').click() # Type into Sign In --> Usually time.sleep(1)
      driver.find_element_by_xpath('//*[@id="ABRYModal"]/div/div/div[1]/button/span').click()


      def delete_files():
          for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                print("File is : ", f)
                # print(os.path.isfile(f))  Check whether the specified path is an existing regular file or not
                if os.path.exists(f):
                    os.remove(f)
                    print("File : ", f, "is deleted.")
                else:
                    print("The file does not exist")


      delete_files()
      x = file_creation()  # Enable it later
      # last_file_name = r"C:\Users\RPA Testing\Desktop\Success_Cases_Phase3.txt"  # DISABLE IT LATER
      last_file_name = x[0][0]  # ENABLE IT LATER
      last_date = x[1]
      print("Last file name i s ", last_file_name, "Last Date is ", last_date, sep="---")


      def kyc_bulk():
          # https://www.tutorialspoint.com/how-to-upload-file-with-selenium-python
          driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()  # Select Member
          time.sleep(2.5)  # A delay of 2 seconds, danger element
          driver.find_element_by_xpath(
              '//*[@id="menu"]/li[2]/ul/li[4]/a').click()  # KYC Bulk --> Usually time.sleep(12)
          time.sleep(2)
          # alert_box(driver, explicit_timeout=2, driver_timeout=0.25, max_retry_count=4,
          #           uipath_run=False)  # alert handler
          time.sleep(5)
          driver.find_element_by_xpath('//*[@id="kycFile"]').send_keys(last_file_name)
          print("Clicked----------------------------------------")
          driver.find_element_by_xpath('//*[@id="aadhaarConsent"]').click()
          time.sleep(3)
          driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
          driver.switch_to.alert.accept()
          loop_counter_value = 20
          with open(last_file_name, mode="r") as file:
              total_records_count = file.readlines()
              rows = []
              total_records_for_kyc_upload = total_records_count.__len__()
          time.sleep(100)
          driver.implicitly_wait(100)

          print("Page is loaded.")

          loop_counter = 0
          last_file_name_new = last_file_name.split("\\")[-1].replace(".txt", "")
          while not str.__contains__((driver.find_element_by_xpath('//*[@id="1"]/td[2]').get_attribute('title')),last_file_name_new):
              loop_counter = loop_counter + 1
              time.sleep(3)
              if loop_counter <= 5:
                  print("Not matched")
              else:
                  raise Exception("Portal is not able to load the page for KYC Bulk.")
                  break

          print("Page is loaded.")
          kyc_sno = driver.find_element_by_xpath('//*[@id="1"]/td[1]').get_attribute('title')
          kyc_filetitle = driver.find_element_by_xpath('//*[@id="1"]/td[2]').get_attribute('title')
          kyc_filestatus = driver.find_element_by_xpath('//*[@id="1"]/td[5]').get_attribute('title')
          print(kyc_sno, kyc_filetitle, kyc_filestatus, sep="---")
          while str(driver.find_element_by_xpath('//*[@id="1"]/td[5]').get_attribute('title')).strip() == "Processing...":
              loop_counter = loop_counter + 1
              time.sleep(3)
              if loop_counter <= 50:
                  print("Not matched")
              else:
                  raise Exception("Portal is not able to load the page for KYC Bulk.")

          if str(driver.find_element_by_xpath('//*[@id="1"]/td[5]').get_attribute('title')).strip() == "Process completed with validation errors.":
                  print("File contains errors.")
                  driver.find_element_by_xpath('//*[@id="1"]/td[5]/a').click()
                  time.sleep(10)
                  column_names = ["UAN NUMBER", "REMARKS"]
                  with open(os.path.join(directory, os.listdir(directory)[0]), mode="r") as file:
                     error_file_upload = file.readlines()
                     rows = []
                     failed_lines=[]
                     df = pd.read_excel(r'C:\Users\RPA Testing\Desktop\DB_Data.xlsx')
                     for line in error_file_upload:
                             if line.__contains__("Please check blank lines in"):
                                    send_mail("EPFO Digital Signature process - Phase 3",
                                              "Hi Team, \n Process got failed in successfully uploading the files due to the blank lines in the file.\nPlease check the send_mail_attachment_code part.",
                                              admin_status=True)
                                    break

                             else:
                                  line_no = re.findall(r'((?<=Line No\s).*?(?=\s)|(?<=\[Line no.\s).*?(?=\s))', line)[0]  # this regular expression is to fetch between Line No and the first space it encountered
                                  # push records which are failed to upload in KYC Bulk upload
                                  # fetch UAN number from file_creation function calling from db_connect.py file
                                  if line_no.isnumeric():
                                   failed_lines.append(line_no)
                                  uanNumber = re.findall(r'(?<=).*?(?=#~#)', x[0][1][int(line_no)])[0]
                                  line = re.sub(r'(no.)', 'No', line)
                                  line = re.sub('[\[\]]', '', line)
                                  reason_for_failure = re.findall(r'(?<=Line No\s\d).*?(?=(.*|$))',line)
                                  rows.append([uanNumber,reason_for_failure])
                  uploaded_df = df[df['SNo'].isin(failed_lines) == False].filter(["Employee_Name","Employee_Code","UAN_Number"])
                  uploaded_df.to_excel("D:\\PySelenium\\Errors\\uploaded_cases.xlsx", sheet_name="Sheet1",index=False)
                  error_df = pd.DataFrame(rows,columns=["UAN NUMBER", "REMARKS"])
                  error_df.to_excel("D:\\PySelenium\\Errors\\error_cases.xlsx", sheet_name="Sheet1",index=False)
                  print("Different Case.")
                  success_count = (total_records_for_kyc_upload)-(rows.__len__())
                  response = send_mail_with_attachment("EPFO Digital Signature process - KYC Bulk Upload",
                                                       f"Hi Team,\n\nProcess got executed and file has been successfully uploaded with {success_count} records.\nPlease find the attached file for the failure cases with reasons.\n\nThanks & Regards \nTeam Automation",
                                                       r'D:\PySelenium\Errors\error_cases.xlsx',r'D:\PySelenium\Errors\uploaded_cases.xlsx', admin_status=False)
                  if response == "Failure":
                      send_mail("EPFO Digital Signature process - Phase 3",
                                "Hi Team, \n Process got failed in sending the error attachment.\nPlease check the send_mail_attachment_code part.",
                                admin_status=True)

          elif str(driver.find_element_by_xpath('//*[@id="1"]/td[5]').get_attribute('title')).strip() == "Process completed":
              df = pd.read_excel(r'C:\Users\RPA Testing\Desktop\DB_Data.xlsx') # if process is completed without validation errors, you can directly send the uploaded excel file
              success_count = len(df.index)
              response = send_mail_with_attachment("EPFO Digital Signature process - PKYC Bulk Upload",
                                                   f"Hi Team,\n\nProcess got executed and file has been successfully uploaded with {success_count} records.\nPlease find the attached file for the success cases.\n\nThanks & Regards \nTeam Automation",
                                                   "", r'C:\Users\RPA Testing\Desktop\DB_Data.xlsx', admin_status=False)
              if response == "Failure":
                  send_mail("EPFO Digital Signature process - KYC Bulk Upload",
                            "Hi Team, \n Process got failed in sending the error attachment.\nPlease check the send_mail_attachment_code part.",
                            admin_status=True)

      try:
       kyc_bulk()
       with open(r"D:\PySelenium\DB_Datetime.txt", mode="w") as file:
           file.write("Last_Date=" +str(datetime.now()).split(".")[0].strip())
       os.system("taskkill /im chrome.exe /f")
      except:
          os.system("taskkill /im chrome.exe /f")


except:
     pass