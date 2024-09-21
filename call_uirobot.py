import subprocess


def call_uirobot():
    try:
        #subprocess.call([r"C:\Users\RPA Testing\Desktop\transferApprovalsUiBot.bat"])
        subprocess.call([r"C:\\Users\\Bot01\\Desktop\\Bank_approval_uipath.bat"])
        uipath_status = True
        return uipath_status

    except:
        uipath_status = False
        return uipath_status

