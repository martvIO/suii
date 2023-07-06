import mysql.connector
from flask import session
from DataBaseConnector import DataBase
import os
from dotenv import load_dotenv
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
def addTransaction(values):
    connection = mysql.connector.connect(host='localhost', port='3306', user='root', password=PASSWORD, database='bank')
    cursor = connection.cursor()
    query = "INSERT INTO bank_transactions (IN_amount,OUT_amount,bank_acount_id,transaction_date,acount_balance_before,acount_balance_after) VALUES (%s, 0, %s, %s, %s, %s), (%s, 0, %s, %s, %s, %s)"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close() 
def getBalance(session: session,bank: DataBase):
    id = session["id"]
    balacne = int(bank.getValue('current_balance','bank_acounts',f"id = {id}",None)[0])
    return balacne
def getBalanceV(session: session,bank: DataBase):
    id = session["id"]
    try:
        balacne = int(bank.getValue('current_balance','visacard',f"AcountId = {id}",None)[0])
        if balacne is None:
            return 0
        return balacne
    except IndexError:
        return 0