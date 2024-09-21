# Source: https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15

import pyodbc
import pandas as pd
from datetime import date
from datetime import datetime
from mailer import send_mail
import os
import time

# Last_Date=2021-06-24 23:59:59
# today = date.today()  # Format : 2021-07-04
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

def file_creation():
    def getorup_datetime(value):
        if value == "get":
            with open(r"D:\PySelenium\DB_Datetime.txt", mode="r") as file:
                file.seek(0) # when seek is used the cursor moves at the beginning of the line
                out = file.read()
                out = out.split("=")[1].strip()
                print("Previous date is ", out)
                return out

        elif value == "up":
            print(" Current date is ", today)
            with open(r"D:\PySelenium\DB_Datetime.txt", mode="w") as file:
                file.write("Last_Date=" + today)

    def execute_DB():
        server = '10.225.170.57'
        database = 'QPay_Prod'
        username = 'RPA_User'
        password = 'xEfRUqaS97BEq#wr'
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        last_dtime = getorup_datetime(value="get")
        # testTIME = '2021-06-29 23:59:59'
        # query = f"SELECT TKU.*,TEI.UAN_Number FROM [QPay_Prod].[dbo].[TBL_KYC_UpdateRequest] TKU JOIN [QPay_Prod].[dbo].[tbl_Employee] TE ON TKU.Employee_Code=TE.Employee_Code JOIN [QPay_Prod].[dbo].[tbl_Employee_Information] TEI ON TE.Employee_Id=TEI.Employee_Id WHERE TKU.Status='APPROVED' AND TKU.StatusDate > '{last_dtime}';"
        # query = f"SELECT TKU.*,TEI.UAN_Number FROM [QPay_Prod].[dbo].[TBL_KYC_UpdateRequest] TKU JOIN [QPay_Prod].[dbo].[tbl_Employee] TE ON TKU.Employee_Code=TE.Employee_Code JOIN [QPay_Prod].[dbo].[tbl_Employee_Information] TEI ON TE.Employee_Id=TEI.Employee_Id WHERE TKU.Status='APPROVED' AND TKU.StatusDate BETWEEN '{last_dtime}' AND '{testTIME}' ;"
        query = f"SELECT TKU.*,TEI.UAN_Number FROM [QPay_Prod].[dbo].[TBL_KYC_UpdateRequest] TKU JOIN [QPay_Prod].[dbo].[tbl_Employee] TE ON TKU.Employee_Code=TE.Employee_Code JOIN [QPay_Prod].[dbo].[tbl_Employee_Information] TEI ON TE.Employee_Id=TEI.Employee_Id WHERE TKU.Status='APPROVED' AND (TKU.StatusDate >= '{last_dtime}' AND TKU.StatusDate < '{today}') ;"
        df = pd.read_sql_query(query, cnxn)
        # print(df)
        cnxn.close()
        if os.path.isfile(r'C:\Users\RPA Testing\Desktop\DB_Data.xlsx'):
            os.remove(r'C:\Users\RPA Testing\Desktop\DB_Data.xlsx')
            print("File Removed")
        df.insert(0,'SNo',df.index+1)
        df.to_excel('C:\\Users\\'+os.environ.get('USERNAME')+'\\Desktop\\DB_Data.xlsx', sheet_name="Sheet1", index=False)  # Disable it later.

        return df

    # df = execute_DB()
    # print("Emp Name is ", df.loc[df['UAN_Number'] == '100939686300']["Employee_Name"].to_string(index=False))

    def create_input(df):
        print("passed db df is ", df, "\n")
        row_count = len(df.axes[0])
        # print("row count is ", row_count)
        res_dict = {}
        result = ""
        separator = "#~#"
        failed_cases = []
        line_no = 0
        for i, row in df.iterrows():
            temp = ""
            if row["UAN_Number"] is None or str(row["UAN_Number"]).strip() == "" or pd.isna(row["UAN_Number"]) or str(row["UAN_Number"]).strip() == "NOT_AVAILABLE":
                failed_cases.append(str(row["Employee_Code"]))
                continue
            else:
                temp = str(int(row["UAN_Number"])) + separator + "B" + separator + str(row["Account_No"]) + separator + \
                        row["Employee_Name"] + separator + str(row["Ifsc_Code"]) + separator
                result += temp + "\n"
                line_no += 1
                res_dict[line_no] = temp

        result = result.strip()
        print("Result string is ", result, "\n")
        print("Failed cases are ", "---".join(failed_cases), "\n")
        if len(failed_cases) == 0:
            pass
        else:
            send_mail("EPFO Digital Signature process - Phase 3", "DB Failed cases are : "+"---".join(failed_cases)+"\n\nThanks & Regards \nTeam Automation",
                      admin_status=False)

        print("Result dict is ", res_dict)
        # https://www.w3schools.com/python/ref_string_translate.asp
        mytable = today.maketrans(": ", "-_")
        today_temp = today.translate(mytable)  # Updated Format : 2021-07-02 17-07-16
        file_path = f"D:\PySelenium\Input\input_{today_temp}_file.txt"
        with open(file_path, mode="w") as file:
            file.write(result)
        print("file path is ", file_path)
        return file_path, res_dict

    today = str(datetime.now()).split(".")[0].strip()  # datetime.now() --> 2021-07-02 16:43:27.491484
    print(" Current date is ", today)
    getorup_datetime(value="get")
    db_df = execute_DB()
    # getorup_datetime(value="up")
    print("db_df is ", db_df)
    file_location = create_input(df=db_df)
    # getorup_datetime(value="up")  # Disable it later
    return file_location, today


# x = file_creation()
# print("x is ", x, "type of x is ", type(x))
# print("Final Path is ", x[0], " Last run date is ", x[1])
