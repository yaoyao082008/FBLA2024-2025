import firebase_admin
from firebase_admin import firestore, credentials
import datetime
import os




# Application Default credentials are automatically created.
creds = credentials.Certificate({
  "type": "service_account",
  "project_id": "fbla-financial",
  "private_key_id": "2bff76ff00066650cbc0dd9ea6669dad897076e1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCaocX4CUb+Ioul\nlbIJUsGpwn/I21zqt/yBeaUFmoQl5l3cnrz6omZgo3mRsqIW7QPSJywb3CNZ+hOf\nAFloonRiTToKQGPXFsxU1r4l6oU2KVSJA9P2hRhez1uzFoUZCHZ4v5WrI7fAYfNh\ncONv/28lMEDZ8IRQnCSYBQDtjxye5Vs/XzYQ6mG6hx63MkfDzzIxuNhRYprQQNVd\njXTw0lf3wsWVvkOa1qotkxfgKr/K1BFPbxFG0iPZLULFH8v1vPBsHHixjQQfdWJT\ntlLn3mvFCcrjIZN24zUUG8mgfORvHvKmqH1tHaWZ7ab3SNeh+Y4ETwPUA5gLEQKK\n0RXf5yFvAgMBAAECggEAS0pVgC3UOU1MvXUj2NJIpYWkfoIAvfCTq9808IOJsIJ4\nVUGdNlP4kTlHqh9WON9yqtKT8YTAWcEf6J1c60uea3a6ud8cPdBF8VEWCJQmBHcf\nSA9rF286rH8+YPaoG8Y5GRX/o/KiN7P5swoqU5AF6A+UpAkuA6njT3mwN/skrmCw\nwXfboprdK27qSA9i5CLYHoom2GWjQTTfOiUDvMZzGaLKSYXaWWMqi/hfVi2Evs9X\nrXdIEIadle9kAez/LzXCKxZTVJsKI0M3peOLGqQ9oSse/ReS818P5lUG7bbbvPFm\niu8jlnpwRbi6kwCAVV4Nk52YzajTpU7duJjPSsyJoQKBgQDK0tqoX2IhYBUyCA6y\nigEAdHDuhe+JpDjqQgsxAExnEesF901ZFXTsiSRDIzfzSe7mrlyJBrh9M0FWD841\nyzlHt1FuIRzpZ8D/Fn8eWTm0xX0w6lonVK62YE9r5ZHUWtj6FBgJP5bj3SlKARJ2\npD0q8gCKkCa7E79QgNOoPrQFlwKBgQDDLGFn4zAZ7D8Ub6auFWKX98NirJ93fCjG\ne/x7aMOOJ8oDtkA8eDZvflGBjkQsHSA5h1QMWfm8f0bu3SJ4HKTMFDWkSPxpvMey\n3LoLm8olXII4EA5TUfzCj+HCna+KLyfj98eMcO6H2GODKtkMuSPOaoNjHNwpqSSm\nBok22tGt6QKBgDDh3qcjze/DS3hybrBjCFjGt40VJKUkuj7jSfU2YDObIuyeLLsi\nq7pyVxYDP/HXyMc6EL1JrF8oYj/OsWFPqG97ZBnJy0EJq38POfXjhT/nNQP8B1xh\nUXZNAfc8LghjGNY0z5IzDDfAzrmyRnPno4JdLvo2Qc9ms/4//kMXUaXjAoGAI4T1\nKSnwfBdBl5+GLxJXQh7mIRQXZXBkH1M7LN5xEHLvUeOeJyMdjQbpIHHauEiIr8+Q\nHTtWttZW+2ulNUTJPRbEeGSMA1ZG5adD+I7eqBQA4uERKlq2bFYxGPEHnFdepB9Y\n4pc+4dwgqCNpIuaivJMn3CbJbo+IyupPmHsUQ9kCgYBxSscxgNFNfKPc1QDdItiF\ntql/kgbEjAy0f8DlxvRhHzMiyJMTIC7nCQPBwbqTYSuzZ9Jt8rslYq+eFPPqLTBX\nYi+asHhFIM+WnxfTTnHxIiT5nq150+YmgCbJlmzJ0IBdeNShsWJHmNKc4aNRK5b4\n1mnxRNX/YZjnfY0FBhsDfQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3k9zy@fbla-financial.iam.gserviceaccount.com",
  "client_id": "107625074037412958955",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3k9zy%40fbla-financial.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
app = firebase_admin.initialize_app(creds)
db = firestore.client()

current_year = int(datetime.datetime.today().strftime("%Y"))

# get user from database
def get_user(email, name=None):
    ref = db.collection("users").stream()
    for usr in ref:
        usr = usr.to_dict()
        try:
            if usr["email"] == email:
                return usr # return user if exists
        except Exception as e:
            pass      
    new_user(email, name)

def new_user(email, name):
    ref = db.collection("users").document(email)

    data = {
        "email": email,
        "name": name,
        "incomes": [],
        "expenses": [],
        "balance": 0,
        "months": [0 for i in range(12)]
        }
    
    ref.set(data)

def update_incomes(email, incomes):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    for income in incomes:
        data[incomes[income][0]] = {
            'type': incomes[income][1],
            'amt': incomes[income][2],
            'date': incomes[income][3]
            }
    
    ref.update({"incomes": data})
    

def update_expenses(email, expenses):
    #name, type, amt, date
    ref = db.collection("users").document(email)
    data = {}
    for expense in expenses:
        data[expenses[expense][0]]=  {
            'type': expenses[expense][1],
            'amt': expenses[expense][2],
            'date': expenses[expense][3]
            }
            
    ref.update({"expenses": data})
    

def update_balance(email):
    ref = db.collection("users").document(email)
    usr = get_user(email)
    total_income = 0
    incomes = usr['incomes']

    months = [0 for i in range(12)]
    #finds total income
    for i in incomes:
        curr_amount = float(incomes[i]["amt"])
        total_income += curr_amount

        #dates incomes by month
        date = [int(d) for d in incomes[i]["date"].split("-")]
        if date[0] == current_year:
            months[date[1]-1] += curr_amount
    
        
    expenses = usr['expenses']
    total_expense = 0
    #finds total expenses
    for i in expenses:
        curr_amount = float(expenses[i]["amt"])
        total_income -= curr_amount
        
        #dates expenses by month
        date = [int(d) for d in expenses[i]["date"].split("-")]
        if date[0] == current_year:
            months[date[1]-1] -= curr_amount
    

    bal = total_expense + total_income

    data = {
        "balance": bal,
        "months": months
        }

    ref.update(data)
