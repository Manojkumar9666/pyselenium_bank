from login_page import EpfoLoginPage,get_login_page
import os



def main_otp_login(username , password):

    config_path = os.path.join(os.getcwd(), "config.cfg")
    current_directory = os.getcwd()


    driver = get_login_page(config_path)
    epfo_login_page = EpfoLoginPage(driver, current_directory)

    counter = 0
    login_status = True

    # Perform login attempts
    if driver:
        while counter <= 9 and login_status:
            print("Counter value is", counter, "and login status is", login_status)
            counter, login_status = epfo_login_page.epfo_login(username, password , counter, login_status)
        
        if not login_status:
            print("First page login successful, proceeding to OTP and Captcha")
            #second_login_status = epfo_login_page.epfo_second_login(username) #otp is not working

            # Check if the second page login is successful
            """if second_login_status:
                print("Second page login successful")
            else:
                print("Failed on the second page login")"""
    else:
        print("Driver initialization failed")

    return driver

