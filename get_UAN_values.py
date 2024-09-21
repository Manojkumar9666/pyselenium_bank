# pip install lxml or import
# pip install openpyxl or import
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns",
              None)  # None to set the maximum number of rows and columns to display to unlimited


def get_uan_values(file_path, driver_var):

    tables = pd.read_html(driver_var.page_source)
    print("To check the values of tables ----->",tables)#test purpose later we can remove
    #print("end tables")
    print('Tables found:', len(tables))
    try:
        with open(file_path, "w") as html_code:  # write mode
            html_code.write(" ")
            html_code.write(driver_var.page_source)
        tables[9].to_excel("Table9.xlsx", sheet_name='Table9')
        print("UAN Files are ready")
    except:
        pass

    # df = tables[9].head(10) # Top 10 values from the table
    # for row in driver_var.find_elements_by_xpath('//*[@id="kycPendingList"]//tr'):
    #     print(row.get_aatribute('id'))
    df = tables[9]
    print(df)#test purpose later we can remove
    df.columns = ['SI','UAN','DocType', 'Name', 'DocNo.','IFSC','DocExpiry','VerificationStatus','Reject KYC']
    df.to_excel("Check.xlsx",sheet_name="Sheet1")
    # print(df.head(5))
    result_as_str = "<EMPLOYEES>"
    for index, row in df.iterrows():
        try:
            result_as_str = result_as_str+"<UAN_NUMBERS><UAN_NUMBER>"+str(int(row[1]))+"</UAN_NUMBER></UAN_NUMBERS>"
            print(result_as_str)
            # every row's value at index 1 (Type of row, index is Pandas Series , float )
        except:
            pass

    result_as_str = result_as_str + "</EMPLOYEES>"
    return result_as_str,df
