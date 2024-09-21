from fastapi import FastAPI
import pyodbc
import uvicorn

app = FastAPI()

def check_uan(uan: str):
    server = '10.225.170.57'
    database = 'QPay_Prod'
    username = 'RPA_User'
    password = 'xEfRUqaS97BEq#wr'
    # Establish a connection to the database
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
    )
    cursor = cnxn.cursor()
    # Replace 'TBL_PFUAN_Bank_KYC_Approval_Status' and 'UAN_Number' with your actual table and column names
    query = f"SELECT COUNT(*) FROM TBL_PFUAN_Bank_KYC_Approval_Status WHERE UAN_Number = ?"
    cursor.execute(query, (uan,))
    result = cursor.fetchone()

    if result[0] > 0:
        return {"result": True}
    else:
        return {"result": False}

@app.get("/check_uan/{uan}")
def trigger_operations(uan: str):
    return check_uan(uan)


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.79.69", port=8000)