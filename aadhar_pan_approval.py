import os
import time
import pandas as pd
import requests
import datetime
from test import insertion

from alertbox_handler import alert_box
from call_uirobot import call_uirobot
from get_Kill_process import get_kill_process
import re
# from selenium import webdriver
import subprocess
from mailer import send_mail
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
# from db_connect import qpay_dbconnect
from get_UAN_values import get_uan_values
from execute_SP import execute_SP
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from Report_bank_code import bank_report, error_report



# from requests.structures import CaseInsensitiveDict
file_path_bank = f"C:\\Users\\Bot01\\Desktop\\Bank_approvals_csv.csv"
rejected_records_bank = f"C:\\Users\\Bot01\\Desktop\\Bank_rejected_records.csv"
columnNames = ["UAN","Account_name","Account_No","IFSC_NO","Username","Date"]

def aadhar_pan_approval(driver, type_text, navigation, loop_counter_value, username, limit=125):
    global approved_bankDF, record_status_pf
    dbMatchedDf = pd.DataFrame(columns=['UAN', 'DocType', 'Name', 'DocNo','IFSCNO'])
    RejectedDF = pd.DataFrame(columns=['UAN', 'DocType', 'Name', 'DocNo','IFSCNO','Username', 'Failure_Reason'])
    if navigation is True:
        driver.find_element(By.XPATH,'//*[@id="menu"]/li[2]/a').click()  # Select Member
        time.sleep(1)  # A delay of 5 seconds, danger element
        driver.find_element(By.XPATH,            '//*[@id="menu"]/li[2]/ul/li[12]/a').click()  # Approve KYC seeded by member --> Usually time.sleep(12)
        time.sleep(2)
    else:
        pass

    #alert_box(driver, explicit_timeout=2, driver_timeout=0.5, max_retry_count=3, uipath_run=True)  # alert handler
    # AUtomate that pop up using UIpath and call it as a bat file in line 34, implement the same alertbox handler pyhton code in UIpAth
    loop_counter = 0
    time.sleep(5)
    try:
        while driver.find_element(By.XPATH,'//*[@id="load_kycPendingList"]').text == "Loading...":
            loop_counter = loop_counter + 1
            time.sleep(5)
            if loop_counter <= loop_counter_value:
                pass
            else:
                raise Exception("Portal is not able to load the page for PAN/Aadhar approval.")
    except:
        pass

    print("Page is loaded.")

    def select_doctype():
        print("select")
        # driver.find_element(By.XPATH,'//*select[@id="gs_docType"]/option[@value="PAN"]').click()
        sel = Select(driver.find_element(By.XPATH,'//*[@id="gs_docType"]'))
        sel.select_by_visible_text(type_text)
        time.sleep(1)
        print("Selected ", type_text)

    select_doctype()

    # -------------------------------> To check if there are any records or not
    def check_records():
        #time.sleep()
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[3]/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]')))
            if driver.find_element(By.XPATH,                    '/html/body/div[2]/div/div[2]/form/div[3]/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]').text == "No Record(s) Found":
                print("No records found")
                # driver.find_element(By.XPATH,'//*[@id="gview_kycPendingList"]/div[2]/div/table/thead/tr[2]/th[4]/div/table/tbody/tr/td[3]/a').click()
                driver.find_element(By.XPATH,'//*[@id="menu"]/li[2]/a').click()  # Select Member
                time.sleep(2)  # A delay of 2 seconds, danger element
                driver.find_element(By.XPATH,                    '//*[@id="menu"]/li[2]/ul/li[12]/a').click()  # Approve KYC seeded by member --> Usually time.sleep(12)
                time.sleep(1)
                approval_status = False
            else:
                approval_status = True
        except:
            approval_status = True

        print("approval status is : ", approval_status)
        time.sleep(1)
        return approval_status

    # Function ends here <--------------------------------------------------------

    if type_text == "Bank":
        # driver.find_element(By.XPATH,'//*[@id="gs_verificationStatus"]').send_keys("Success")
        result_uan_values, bankDataDf = get_uan_values(file_path="bank_approvals_page.html", driver_var=driver)
        print(bankDataDf)
        print(result_uan_values)
        df = execute_SP(uan_numbers=result_uan_values)
        time.sleep(1)
        # dbMatchedDf = pd.DataFrame(columns=['UAN', 'DocType','Name','DocNo'])
        print(df)

        # append rows to an empty DataFrame

        total = driver.find_element(By.XPATH,"//*[@id='kycPendingListPager_right']/div").text
        Count = total[-6:]
        print(Count)

        for index, row in bankDataDf.iterrows():
            if str(row["UAN"]) != "nan":
                emp_name = df.loc[df['UAN_Number'] == str(int(row["UAN"]))]["Employee_Name"].to_string(index=False)
                print(emp_name)
                if emp_name == "Series([], )":
                    print("No matches found for the UAN number: ", row["UAN"])
                    db_status = False
                    continue
                else:
                    account_num = df.loc[df['UAN_Number'] == str(int(row["UAN"]))]["Bank_Account_Number"].to_string(
                        index=False).replace(":", "")
                    ifsc_code = df.loc[df['UAN_Number'] == str(int(row["UAN"]))]["IFSC_Code"].to_string(index=False)
                    doc_type_pf = row["DocType"]
                    # print("Doc Type :", doc_type_pf)
                    account_num_pf = str(int(row["DocNo."]))
                    # print("Doc No :", account_num_pf)
                    ifsc_code_pf = str(row["IFSC"])
                    # print("IFSC :", ifsc_code_pf)
                    record_status_pf = str(row["VerificationStatus"])
                    # print("Status :", record_status_pf)
                    fuzz_pr = fuzz.partial_ratio(emp_name.lower(), row["Name"].lower())
                    fuzz_tsr = fuzz.token_sort_ratio(emp_name.lower(), row["Name"].lower())
                    print(account_num, account_num_pf, ifsc_code, ifsc_code_pf, doc_type_pf, record_status_pf,
                          emp_name, "-", row["Name"], "--->", fuzz_pr, "-", fuzz_tsr)
                    if str(record_status_pf).__contains__("Success"):
                        print("Match found: ", emp_name, account_num, ifsc_code, sep="<->")
                        dbMatchedDf = dbMatchedDf.append(
                            {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"], 'DocNo': row["DocNo."],
                             'IFSCNO': row["IFSC"]},
                            ignore_index=True)
                        db_status = True
                        record_approval_status = True
                    elif str(record_status_pf).__contains__("nan"):
                            if (account_num == account_num_pf) and (ifsc_code == ifsc_code_pf) and (
                                    doc_type_pf == "Bank") and (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                print("Match found: ", emp_name, account_num, ifsc_code, sep="<->")
                                dbMatchedDf = dbMatchedDf.append(
                                    {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                     'DocNo': row["DocNo."], 'IFSCNO': row["IFSC"]},
                                    ignore_index=True)
                                db_status = True
                                record_approval_status = True
                            else:
                                if (account_num != account_num_pf):
                                    if (ifsc_code != ifsc_code_pf):
                                        if not (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "-- AccountNo not same--IFSC Code not same---Name didn't matched---"},
                                                ignore_index=True)
                                            db_status = False
                                        else:
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "-- portal Account number & IFSC Code didn't matched with qzone data---"},
                                                ignore_index=True)
                                            db_status = False
                                    else:
                                        if not (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "--portal AccountNumber & Name didn't matched with qzone data---"},
                                                ignore_index=True)
                                            db_status = False
                                        else:
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "-- AccountNumber didn't matched with qzone data----"},
                                                ignore_index=True)
                                            db_status = False
                                else:
                                    if (ifsc_code != ifsc_code_pf):
                                        if not (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "-- IFSC Code & Name didn't matched with Qzone data---"},
                                                ignore_index=True)
                                            db_status = False
                                        else:
                                            if (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                                RejectedDF = RejectedDF.append(
                                                    {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                     'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                     'Failure_Reason': "----IFSC Code didn't matched with Qzone-----"},
                                                    ignore_index=True)
                                                db_status = False
                                    else:
                                        if not (fuzz_pr >= 85 or fuzz_tsr >= 85):
                                            RejectedDF = RejectedDF.append(
                                                {'UAN': row["UAN"], 'DocType': row["DocType"], 'Name': row["Name"],
                                                 'DocNo': int(row["DocNo."]), 'IFSCNO': row["IFSC"], 'Usename': username,
                                                 'Failure_Reason': "---Name didn't matched with Qzone---"},
                                                ignore_index=True)
                                            db_status = False
                                        else:
                                            pass
        RejectedDF.to_csv(rejected_records_bank, index=False)#for penny drop and rejected records
        #error_report()
        print("hello world")

    else:
        pass
    # The above code will filter verification status with success records.
    # connects to Qpay DB and returns a data frame

    driver.implicitly_wait(6)
    if check_records() is True:  # Checking for records in the table
        driver.implicitly_wait(15)
        print("Continuing to next step")
        if type_text == "Bank":  # If document type is Bank
            approved_UAN_numbers = []
            approved_account_no=[]#used for storing the approved records in the excel
            approved_ifsc_no= []#used for storing the approved records in the excel
            approved_name_list = []#used for storing the approved records in the excel
            process_status = True
            while process_status is True:
                #alert_box(driver, explicit_timeout=3, driver_timeout=0.5, max_retry_count=1,
                          #uipath_run=False)  # alert handler
                count = 0
                count_final = 10
                max_loop_value = 0
                record_approval_status = False
                loop_breaker = False
                dict1 = {'UAN_Numbers': []}
                df1_dict1 = pd.DataFrame(dict1)
                uan_list = []
                # print(df['UAN_Number'])
                # driver.find_element(By.XPATH,'//*[@id="gs_uan"]').send_keys(int(str(df['UAN_Number'][0][:3])))
                time.sleep(5)
                if len(dbMatchedDf.index) == 0:
                    break
                else:
                    for ind, row in dbMatchedDf.iterrows():
                        print(ind)
                        matchname = row["Name"]
                        print(matchname)
                        accont_no = row["DocNo"]
                        print(accont_no)
                        uan_no = row["UAN"]
                        print(uan_no)
                        IFSC_NO = row["IFSCNO"]
                        print(IFSC_NO)
                        # process_status = False
                        # # row_id = i.get_attribute('id')
                        # max_loop_value = max_loop_value + 1
                        # # print(row_id, type(row_id))
                        # if max_loop_value <= limit:
                        #     pass
                        # else:
                        #     loop_breaker = True
                        if row["UAN"] == "":
                            pass
                            # print("Not a proper row")
                        else:
                            print("index value: ", ind, "dataframe records count: ", len(dbMatchedDf.index))
                            last_record = False
                            if ind == (len(dbMatchedDf.index) - 1):
                                count = 20
                                process_status = False
                                last_record = True
                                driver.find_element(By.XPATH,f'//td[@title={str(int(row["UAN"]))}]').click()
                                approved_UAN_numbers.append(row["UAN"])
                                # uan_list.append(str(row["UAN"]))
                            else:
                                # alert_box(driver, explicit_timeout=3, driver_timeout=0.5, max_retry_count=1,
                                #           uipath_run=False)  # alert handler
                                driver.find_element(By.XPATH,f'//td[@title={str(int(row["UAN"]))}]').click()
                                if count == 0:
                                    uan_list = []
                                count = count + 1
                                approved_UAN_numbers.append(str(int(row["UAN"])))
                                approved_account_no.append(str(int(row["DocNo"])))
                                approved_name_list.append(row["Name"])
                                approved_ifsc_no.append(row["IFSCNO"])
                                Total_approverd = pd.DataFrame()

                                uan_list.append(str(row["UAN"]))
                                # If atleast one item is selected within max_loop_value then approve the records
                                #     loop_breaker = False
                                print("Count values is ", str(count))
                                print("Check values")
                                # time.sleep(10)

                            if count == 35:  # this count conditon is checking to acccept digital signature for every selected 10 records to avoid DSC loading issue
                                count = 0
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView(true);",
                                                          WebDriverWait(driver, 10).until(
                                                              EC.visibility_of_element_located(
                                                                  (By.ID, 'approve3'))))
                                    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.ID, 'approve3'))))

                                    print("<<<---------------------------------------Screen moved to the Approve DSC button----")
                                except Exception as ex:
                                    print(ex)
                                #alert_box(driver, explicit_timeout=1.5, driver_timeout=0.10,
                                         # max_retry_count=1, uipath_run=False)  # alert handler

                                if call_uirobot() is True:  # If UiPath robot was executed properly?
                                    print(approved_UAN_numbers)
                                    insertion(approved_UAN_numbers=approved_UAN_numbers )
                                    send_mail("EPFO Digital Signature process - Bank Approval Status on-" + username,
                                              "Hi Team,\n Bank approval process got executed on the UAN Numbers By DSC: " + "-".join(
                                                  approved_UAN_numbers) + "\n\nThanks & Regards \nTeam Automation",
                                              admin_status=False)

                                    list1,list2,list3,list4,list5,list6 = [approved_UAN_numbers],[approved_name_list],[approved_account_no],[approved_ifsc_no],[username] ,[datetime.date.today()]
                                    approved_bankDF = pd.DataFrame(list(zip(list1, list2, list3, list4, list5,list6)),columns=columnNames)
                                    if os.stat(file_path_bank).st_size == 0:
                                        print(file_path_bank, 'File is empty')
                                        approved_bankDF.to_csv(file_path_bank, index=False, header=columnNames)
                                    else:
                                        approved_bankDF.to_csv(file_path_bank, mode='a', index=False, header=False)
                                    del approved_bankDF
                                    #bank_report(username= username)# sending repot after every 10 approvals
                                    approved_UAN_numbers = []
                                    time.sleep(3)
                                    # Save UAN Data
                                    if last_record == True:
                                        uan_list.append(str(row["UAN"]))
                                    dict2 = {'UAN_Numbers': uan_list}
                                    df2_dict2 = pd.DataFrame(dict2)
                                    df1_dict1 = pd.DataFrame({'UAN_Numbers': []})
                                    df1_dict1 = df1_dict1.append(df2_dict2, ignore_index=True)
                                    df1_dict1.to_csv(r"D:\PySelenium_bank\log data.csv", mode='a', index=False, header=False)
                                    del uan_list
                                    del df1_dict1
                                    del df2_dict2
                                    # Checking whether the page is loaded or not
                                    status = True
                                    loop_counter = 0

                                    try:
                                        while driver.find_element(By.XPATH,'//*[@id="load_kycPendingList"]').text == "Loading...":
                                            time.sleep(2)
                                            loop_counter = loop_counter + 1
                                            if loop_counter <= loop_counter_value:
                                                status = True
                                            else:
                                                status = False
                                                break
                                        if status is True:
                                            process_status = True  # Page got loaded in time.
                                        else:
                                            process_status = False  # Page didn't get loaded in time.
                                            raise Exception("Portal is not able to load the page for Bank approval, but approval for previous records was done.")
                                    except:
                                        process_status = True
                                    if check_records() is True and process_status is True:  # Checking for records in the table
                                        select_doctype()

                                        # driver.find_element(By.XPATH,'//*[@id="gs_verificationStatus"]').send_keys("Success")
                                        #alert_box(driver, explicit_timeout=3, driver_timeout=0.5, max_retry_count=1,
                                                  #uipath_run=False)  # alert handler
                                        time.sleep(4)
                                        # break
                                    else:
                                        process_status = False  # There are no records to execute.
                                        if len(approved_UAN_numbers) == 0:
                                            approved_UAN_numbers.append(
                                                "'0' --> No records or 0 records found for 'Bank'")
                                        break

        else:  # Document type is other than Bank
            print("Document type is other than Bank")
            #alert_box(driver, explicit_timeout=3, driver_timeout=0.5, max_retry_count=1,
                      #uipath_run=False)  # alert handler
            WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cb_kycPendingList"]')))
            driver.find_element(By.XPATH,'//*[@id="cb_kycPendingList"]').send_keys(Keys.SPACE)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  WebDriverWait(driver, 10).until(
                                      EC.visibility_of_element_located(
                                          (By.ID, 'approve3'))))
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'approve3'))))
            #driver.find_element(By.XPATH,'//*[@id="approve1"]').click()
            #alert_box(driver, explicit_timeout=1.5, driver_timeout=0.10, max_retry_count=1,
                      #uipath_run=False)  # alert handler
            #driver.switch_to.alert.accept()
            call_uirobot()
            time.sleep(3)
            loop_counter = 0
            driver.implicitly_wait(15)
            while driver.find_element(By.XPATH,'//*[@id="load_kycPendingList"]').text == "Loading...":
                loop_counter = loop_counter + 1
                time.sleep(2)
                if loop_counter <= loop_counter_value:
                    pass
                else:
                    raise Exception("Portal is not able to load the page for PAN/Aadhar approval.")


# Below is the old code to check if that particular page is loaded or not
"""
    while re.match(r"View (\d+).+- (\d+).+of",
                   driver.find_element(By.XPATH,'//*[@id="kycPendingListPager_right"]/div').text) is None:
        loop_counter = loop_counter + 1
        time.sleep(2)
        if loop_counter <= loop_counter_value:
            pass
        else:
            raise Exception("Not able to find the page for PAN/Aadhar approval.")
"""
