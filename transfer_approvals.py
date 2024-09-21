# =====================================================================================================================>
# Project   : EPFO Automation-Transfer Approvals                                                      Last code changes : 08-07-2021
# Manager   : Shankara Giri G
# Team Leads : Sahil R Kulkarni
# Mobile No : +91 7995820483/8328091021
# Tools/Tech Used: Python, Selenium, UiPath, Data Scraping, Excel, Mailers, .bat files, Firefox
# --------------------------------------------------------------------------------------------------------------------->
# Project Status : Success
# =====================================================================================================================>
# import pre defined modules
import time
import os
from dsc_selector import dsc_selector
from capture import test_captcha
from selenium.webdriver.chrome.service import Service
from capture import get_user_input, run_test_captcha_with_retries
import subprocess
from main import main_otp_login
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import get_credentials,get_Other_PF_Details
from mailer import send_mail, send_mail_with_attachment
from selenium import webdriver
import wmi
from get_Kill_process import get_kill_process
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium.webdriver.common.by import By
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from flaky import flaky

# set the options for Firefox browser
options = webdriver.FirefoxOptions()
#options.add_argument('--headless')  # run browser in headless mode

# initialize the webdriver with Gecko driver

from selenium.webdriver.firefox.options import Options
from Report_bank_code import transfers_report

Current_date=datetime.date.today()
today_date=Current_date.strftime("%d-%m-%Y")
print(today_date)

approval_status = False





df = pd.read_excel(r"D:\\PySelenium_bank\\PFCodeDetails.xlsx", sheet_name='Sheet1')
print(len(df.index))
# writer = pd.ExcelWriter('C:\\Users\\RPA Testing\\Desktop\\transfer_approved_cases.xlsx', engine='xlsxwriter')
file_path = f"C:\\Users\\Bot2\\Desktop\\transfer_approved_cases.csv"
for login_iter in range(0,len(df.index)):
#=====================================================================================================================================
    def call_transfer_approval_uibot():
       
       try:
           return subprocess.call([r"C:\\Users\\Bot2\\Desktop\\transfer_approval.bat"])
       except Exception as ex:
           print(ex)
    #========================================================================================================================

    columnNames = ["Member Name","Previous MID","Present MID","Claim Date","LoginUser","Date"]
      # Create Data Frame to share the approved cases data in mail
    
    try:
        if os.path.exists(file_path):
            try:
                approvedDf = pd.read_csv(file_path)
                print("File exists with sheet name")
            except:
                approvedDf = pd.DataFrame(columns=columnNames)
                approvedDf.to_csv(f"C:\\Users\\Bot2\\Desktop\\transfer_approved_cases.csv")# create file if not available

        else:
            approvedDf = pd.DataFrame(columns=columnNames)
        # os.remove("C:\\Users\\RPA Testing\Desktop\\transfer_approved_cases.xlsx")
        os.system("taskkill /im firefox.exe /f")  # Kill all firefox browsers
        os.system("taskkill /im chrome.exe /f")  # Kill all chrome browsers
        get_kill_process()  # Kill UiPath processes
        print("<<<--------------------------------------Killed all process--------------------------------------------------------------------->>>.")
        processes_to_be_killed = ['UiPath.Executor.exe']  # this will be killed incase of bot failure to process digital signature
        running_processes = wmi.WMI()

        driver=  main_otp_login(username = get_Other_PF_Details(login_iter)[0].strip(), password = str(get_Other_PF_Details(login_iter)[1]).strip() )
    
        def navigate_to_transfer_approvals():  
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]').click()
            except:
                pass      
            driver.find_element(By.XPATH,'//*[@id="menu"]/li[8]/a').click() #Click on Online Services
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu"]/li[8]/ul/li[2]/a')))                           
            driver.find_element(By.XPATH,'//*[@id="menu"]/li[8]/ul/li[2]/a').click() #Click on Transfer Claim
    
            element = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbDoLogin"]/tbody/tr[1]')))                                                                          
            #element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "tbDoLogin_length"))) #wait till it loads the show entries text at the top left of the table
            print("<<<-----------------------------waited till the element exists-------------------------->>>")
            return driver
        #<<<<<----------------------this is defined as function to retry when session expired issue is encountered in the portal
        driver = navigate_to_transfer_approvals()

        #<<<------------------------------------------------------------------------------------------------->>>>

        try:
         
          empty_records = driver.find_element(By.CLASS_NAME, "dataTables_empty")
          if len(empty_records) == 1:
              send_mail(f"Transfer Approvals-EPFO({get_Other_PF_Details(login_iter)[0]})","Hi Team,\n\nThere are no transfer approval records found in the portal.\n\nThanks and regards,\nAutomation Team",admin_status=True)
              process_continue=False
          else:
              process_continue=True
        except NoSuchElementException:
            print("Transfer approval records are found")
            process_continue=True
        if process_continue:
            row=1
            # table_rows = driver.find_elements_by_xpath("//*[@id='tbDoLogin']/tbody/tr")
            # num_of_rows = len(table_rows)
            process_run = True
            try:
             while process_run: # this loop will run till all the records in the page are completed
                    try:
                        if len(driver.find_element(By.CLASS_NAME, "dataTables_empty")) == 1:
                         # Exit loop with break when the records are empty
                            process_run = False
                            break
                    except:
                        pass
                    def navigate_to_approve_dsc():
                       try:
                        time.sleep(1)
                        print(row)
                        driver.find_element(By.XPATH,f'//*[@id="tbDoLogin"]/tbody/tr[{row}]/td[6]/a/i').click()# Click on plus sign
                        process_run = True
                       except:
                           process_run = False
                       """element = WebDriverWait(driver, 30).until(
                           EC.presence_of_element_located((By.XPATH, "//*[@id='modalBodyHeader']/div/div[2]"))# wait till to get the body of the claim details in the portal
                       )"""
                       try:
                            try:
                                    time.sleep(1)
                                    element = driver.find_element(By.ID, "approve3") #find Approve DSC button in the web page
                                    actions = ActionChains(driver)
                                    time.sleep(1)
                                    actions.move_to_element(
                                        element).perform()  # this is used to page down till it reaches the Approve DSC button
                                    print("<<<---------------------------------------Screen moved to the Approve DSC button------------------------------------->>>")
                                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                                        (By.ID, "approve3"))).click()  # Click on Approve DSC button
                            except Exception as ex:
                                    try:
                                        element = driver.find_element(By.ID, "btnRejectDo") #find Approve DSC button in the web page
                                        actions = ActionChains(driver)
                                        actions.move_to_element(
                                            element).perform()  # this is used to page down till it reaches the Approve DSC button
                                        print("<<<---------------------------------------Screen moved to the Approve DSC button------------------------------------->>>")
                                        time.sleep(3)
                                    except Exception as ex:
                                        print(ex)
                       except:   
                            print("============================Exception occured in navigate to approve DSC function===============")
                       return process_run
                    retry_count=0 # initialise retry_count to Zero and the same record will be retried for three times if it is not successful as per the below conditon
                    while retry_count<6:
                      try:
                        try:
                         print("Refreshing the page")
                       
                        except:
                            #send_mail("Transfer Approval-Approved Cases",approvedDf,admin_status=True)
                            os.system("taskkill /im firefox.exe /f")
                            os.system("taskkill /im javaw.exe /f")
                            print("Proces relogin needed")
                            driver = navigate_to_transfer_approvals()
                        # element = WebDriverWait(driver, 30).until(
                        #     EC.presence_of_element_located((By.ID, "tbDoLogin_length"))# wait for the text "Show entries appeared on the screen"
                        # )
                        print("<<<---------------------------------------------Waited till the element exists or the transfer approval records loaded----------------------------------------------->>>")
                        try:
                            present_mid=str((driver.find_element(By.XPATH,"//*[@id='tbDoLogin']/tbody/tr[1]/td[4]").text)).strip()#this is one of the PRESENT MID value from the transfer approval table
                            print("<<<-------------------------------------Present MID: "+present_mid+"------------------------------------------>>>")
                            member_name = str(driver.find_element(By.XPATH,f"//*[@id='tbDoLogin']/tbody/tr[{row}]/td[2]").text).strip()# memeber name
                            print("<<<-------------------------------------Member Name: "+member_name+"------------------------------------------>>>")
                            previous_mid =str(driver.find_element(By.XPATH,f"//*[@id='tbDoLogin']/tbody/tr[{row}]/td[3]").text).strip()# Previous MID
                            print("<<<-------------------------------------Previous MID: "+previous_mid+"------------------------------------------>>>")
                            claimDate = str(driver.find_element(By.XPATH,f"//*[@id='tbDoLogin']/tbody/tr[{row}]/td[5]").text).strip()
                            print("<<<-------------------------------------Claim Date: "+claimDate+"------------------------------------------>>>")

                        except:
                            process_run = False # Exception occurs when there are no records found and can discontinue the approvals for the login ID
                            break
                        #<<<-----------------------Calling the function below------------------------------>>>

                        process_run = navigate_to_approve_dsc() # Call navigate to approve DSC Process(DSC->Digital Signature)

                       #<<<----------------------Function is called--------------------------------------->>>

                        try:
                            
                            status = dsc_selector(driver= driver)

                            if status:
                              call_transfer_approval_uibot()
                              #insertion(approved_UAN_numbers=approved_UAN_numbers )
                            print("<<<-------------------------------------------UiPath Robot is completed successfully------------------------>>>")
                            list1,list2,list3,list4,list5,list6 = [member_name], [previous_mid], [present_mid], [claimDate], [get_Other_PF_Details(login_iter)[0]], [today_date]
                            approvedDF = pd.DataFrame(list(zip(list1,list2,list3,list4,list5,list6)),columns=columnNames)
                            # approvedDf = approvedDf.append({columnNames[0]: member_name, columnNames[1]: previous_mid, columnNames[2]: present_mid,columnNames[3]: claimDate}, ignore_index=True)
                            approvedDF.to_csv(file_path, mode='a', index=False,header=None)
                            # approvedDf.to_excel(file_path,sheet_name=get_Other_PF_Details(login_iter)[0], index=False) # this file is written for some back up purpose when it is deleted accidentally on desktop
                            # writer.save()
                            del approvedDF
                            # approvedDf.to_excel("C:\\RPA\\Solutions\\TransferApprovalDesktopAutomation\\transfer_approved_cases.xlsx", sheet_name=get_Other_PF_Details(login_iter)[0], index=False) # this file is written for some back up purpose when it is deleted accidentally on desktop
                            print("Approved record is saved in excel")
                            print("sending successful mail----->")
                            #transfers_report(username=get_Other_PF_Details(login_iter)[0])
                            #send_mail(f"Transfer Approval-Approved Cases-{get_Other_PF_Details(login_iter)[0]}","Transfer approval case:\n"+str(approvedDF)+"\n\nPlease check below for full details of the record:\n\n"+str(member_name)+"-"+str(previous_mid)+"-"+present_mid+"-"+claimDate, admin_status=False)
                            element = WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbDoLogin"]/tbody/tr[1]')))
                            #element = WebDriverWait(driver, 50).until(
                                    #EC.presence_of_element_located((By.ID, "tbDoLogin_length"))
                                    # wait for the text "Show entries" appeared on the screen
                                # )
                            first_record = driver.find_element(By.XPATH,"//*[@id='tbDoLogin']/tbody/tr[1]/td[4]").text
                            print(first_record)
                            print(present_mid)
                            if(str(present_mid)==str(first_record).strip()):
                                print(f'<<<------------------------------------------The process is retrying for {retry_count+1} time------------------------------->>>')
                                retry_count += 1
                            else:
                                break
                           
                        except Exception as e:
                            print(e.args)
                            for process in running_processes.Win32_Process():
                                if process.name in processes_to_be_killed:
                                    process.Terminate()  # kill uipath executor
                            os.system("taskkill /im firefox.exe /f")  # Kill all firefox browsers
                            os.system("taskkill /im javaw.exe /f")
                            retry_count += 1
                            process_run = False if str(e.com_error.strerror) == 'Exception occurred.' else True
                            print("presocess relogin needed2") #better debugging purpose
                            print("Triggering mail 1---->>>")
                            #send_mail(f"Transfer Approval-Exception({get_Other_PF_Details(login_iter)[0]})",f"The process is getting retried due to session expired or DSC failure due to:{e}",admin_status=True)
                            driver = navigate_to_transfer_approvals()
                      except Exception as e:
                          os.system("taskkill /im firefox.exe /f")  # Kill all firefox browsers
                          os.system("taskkill /im javaw.exe /f")
                          print("Process relogin needed3") #better debugging purpose
                          print("Triggering mail 2---->>>")
                          #send_mail(f"Transfer Approval-Exception({get_Other_PF_Details(login_iter)[0]})", f"The process is getting retried due to session expired or DSC failure due to:{e}", admin_status=True)
                          driver = navigate_to_transfer_approvals()
                    row = 1
             send_mail_with_attachment(f"Transfer Approvals Bulk-{get_Other_PF_Details(login_iter)[0]}", "Hi Team, \n\nPlease find the attached excel file for the approved records.\n\nThanks and regards,\nAutomation Team","",file_path,admin_status=False)
            except Exception as e:
                process_run = False
                #send_mail(f"Transfer Approval-Exception{get_Other_PF_Details(login_iter)[0]}", f"Please verify whether process is running or not due to:{e}", admin_status=True)
    except Exception as ex:
        print(ex)
        send_mail(f"Transfer Approval-Exception({get_Other_PF_Details(login_iter)[0]})","Please check the process, It might be failed due to invalid credentials or due to portal issue",admin_status=False)
        print("Error in Login to EPF Portal")