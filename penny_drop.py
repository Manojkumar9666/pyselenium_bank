import requests
from requests.structures import CaseInsensitiveDict
from fuzzywuzzy import fuzz
import pandas as pd
dbMatchedDf = pd.DataFrame(columns=['UAN', 'DocType', 'Name', 'DocNo'])
RejectedDF = pd.DataFrame(columns=['UAN', 'DocType', 'Name', 'DocNo'])

data = {
"id_number": "9552500101021600",
"ifsc": "KARB0000955",
}

auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2MTQxMDgxOCwianRpIjoiOTBiOGFjMTEtZmFkYi00YWU2LTg4YWItZDE5MWUzYWYwNDYwIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoiZGV2LmhlcHRhZ29uX2JhbmtfYXVnQHN1cmVwYXNzLmlvIiwibmJmIjoxNjYxNDEwODE4LCJleHAiOjE5NzY3NzA4MTgsInVzZXJfY2xhaW1zIjp7InNjb3BlcyI6WyJ3YWxsZXQiXX19.92vjqM1L-WVUsPiXzqEvU4gk9hNnuhl02eQIgoE7LwE'
hed = {'Authorization': 'Bearer ' + auth_token}
url = 'https://kyc-api.aadhaarkyc.io/api/v1/bank-verification/'
response = requests.post(url, json=data, headers=hed)
print(response)
out = response.json()
print(out['data'])
Account_Holder_name = out['data']['full_name']
print(Account_Holder_name)
Account_exist = out['data']['account_exists']
print(Account_exist)
"""
fuzz_pr = fuzz.partial_ratio(Account_Holder_name.lower(), row["Name"].lower())
fuzz_tsr = fuzz.token_sort_ratio(Account_Holder_name.lower(), row["Name"].lower())
if Account_exist == True and (fuzz_pr >= 85 or fuzz_tsr >= 85):
    print("Match found: ", )
    db_status = True
    record_approval_status = True
else:
    print("Not Matched")
    db_status = False
"""