# pip install xlrd==1.2.0

import pandas as pd


def get_credentials():
    df = pd.read_excel(r"D:\\PySelenium_bank\\configuration_file.xlsx", sheet_name='Login Details')
    print( df["Username"][0], df["Password"][0], df["Firefox Addons Path"][0] )
    return df["Username"][0], df["Password"][0], df["Firefox Addons Path"][0]

def get_Other_PF_Details(login_iter):
    df = pd.read_excel(r"D:\\PySelenium_bank\\PFCodeDetails.xlsx", sheet_name='Sheet1')
    print(len(df.index))
    # print(df["Username"][0], df["Password"][0], df["Firefox Addons Path"][0], sep="--")
    # print( df["User Name"][login_iter], df["New Password"][login_iter],sep="--")
    return df["User Name"][login_iter], df["New Password"][login_iter]

