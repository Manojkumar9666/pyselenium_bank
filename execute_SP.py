# Refer: https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
# https://www.mytecbits.com/internet/python/execute-sql-server-stored-procedure

import pyodbc
import pandas as pd



def execute_SP(uan_numbers):
    # server = '10.225.170.57'
    server = 'QCPQPAYDBLTR'
    database = 'QPay_Prod'
    username = 'RPA_User'
    password = 'B!sa7ESp8_9IzuPogA'
    #'xEfRUqaS97BEq#wr'
    try:
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        print("got successfull")
        cursor = cnxn.cursor()
    except Exception as ex:
        print(ex)

    storedProc = "Exec spEmployeeBankDetails @uan_numbers=?"  # Or storedProc = "Exec spEmployeeBankDetails ?"  # Or storedProc = "Exec spEmployeeBankDetails @uan_numbers='"+uan_numbers+"'"
    # In the script we have to replace the parameter value with question mark (?)
    # The params variable can hold the parameter values in an array.
    print(storedProc)
    params = (uan_numbers)
    print("params valuee-------->", params)
    cursor.execute(storedProc, params)
    result = cursor.fetchall()

    print("result is ", result, " type is ", type(result)) # type is list of tuples
    # print(result[0])

    pd.set_option("display.max_rows", None, "display.max_columns",
                  None)  # None to set the maximum number of rows and columns to display to unlimited
    # Creates a DataFrame object from a structured ndarray, sequence of tuples or dicts, or DataFrame.
    df = pd.DataFrame.from_records(result, columns=['Employee_Name', 'Bank_Account_Number', 'IFSC_Code', 'UAN_Number'])
    df.to_excel("SP_details.xlsx", sheet_name='Sheet_name_1')
    # Close the cursor and delete it
    cursor.close()
    del cursor
    # Close the database connection
    cnxn.close()
    return df



"""
xyz = r"<EMPLOYEES><UAN_NUMBERS><UAN_NUMBER>101301105974</UAN_NUMBER></UAN_NUMBERS></EMPLOYEES>"
df = execute_SP(uan_numbers=xyz)
print(df)
# print("Employee Name is ", df.loc[df['UAN_Number'] == '100161514757']["Employee_Name"].to_string(index=False))
"""