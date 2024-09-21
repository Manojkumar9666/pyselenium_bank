import time
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from flaky import flaky
from selenium.common.exceptions import NoSuchElementException

# Custom Exception for Invalid OTP
class InvalidOTPException(Exception):
    pass

# Function to get input from the user using a dialog box
def get_user_input(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring("Input", prompt)
    root.destroy()  # Destroy the root window after getting input
    return user_input

def test_captcha(driver):
    
    # Enter the first CAPTCHA
    otp_captcha = get_user_input("Please enter the OTP CAPTCHA:")
    print(f"OTP CAPTCHA entered: {otp_captcha}")
    driver.find_element(By.ID, "otpInput").send_keys(otp_captcha) 
    # Sleep to simulate delay
    time.sleep(2)
    # Enter the second CAPTCHA
    captcha = get_user_input("Please enter the CAPTCHA:")
    print(f"CAPTCHA entered: {captcha}")
    driver.find_element(By.ID, "captcha").send_keys(captcha)
    
    # Sleep before clicking submit
    time.sleep(2)
    
    # Click the submit button
    driver.find_element(By.XPATH, '//*[@id="confirmOtp"]/div[1]/div/div[3]/div/div[3]/div/button').click()

    # Wait to ensure the response is loaded
    time.sleep(2)

    # Check for any validation messages
    try:
        invalid_message = driver.find_element(By.XPATH, '//*[@id="confirmOtp"]/div[1]/div/div[2]/div').text
        print(f"Validation message: {invalid_message}")
        if invalid_message.__contains__("INVALID OTP.") or  invalid_message.__contains__("Invalid Captcha Entered."):
            status = False
        else:
            status = True
             
    except NoSuchElementException:
        status = True
        # No validation message found; this could be a successful case or an issue with the XPath
        pass

    return status



def run_test_captcha_with_retries(driver, max_retries=3):
    attempts = 0
    while attempts < max_retries:
        status = test_captcha(driver)
        if status == True:
            print("Captcha test passed.")
            break  # Exit loop if function is successful
        else:
            attempts += 1
            print(f"Attempt {attempts}")
            if attempts >= max_retries:
                print("Max retries reached. Captcha test failed.")
                # Optionally: raise the exception or handle it as needed
                raise
            # Optionally: wait before retrying
            import time
            time.sleep(2)  # Sleep for 2 seconds before retrying



        