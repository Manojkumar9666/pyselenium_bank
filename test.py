import pyodbc
import pandas as pd


def insertion(approved_UAN_numbers):
    server = 'QCPQPAYDBLTR'
    database = 'QPay_Prod'
    username = 'RPA_User'
    password = 'B!sa7ESp8_9IzuPogA'

    # Status for each UAN number
    approval_status = 1

    # Create a list of tuples
    data_to_insert = [(str(uan), approval_status) for uan in approved_UAN_numbers]

    try:
        # Establish a connection to the database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
        )
        cursor = cnxn.cursor()

        # Insert data into the table
        insert_query = "INSERT INTO TBL_PFUAN_Bank_KYC_Approval_Status (UAN_Number, Bank_Approval_Status) VALUES (?, ?)"
        cursor.executemany(insert_query, data_to_insert)
        cnxn.commit()

        print("Data insertion successful.")

    except pyodbc.Error as ex:
        print("Error:", ex)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if cnxn:
            cnxn.close()

