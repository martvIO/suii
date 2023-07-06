from DataBaseConnector import DataBase
from flask import Flask, render_template, request,redirect,url_for, session
import datetime
import mysql.connector 
global bank 
bank = DataBase('localhost','3306','root','ii216695288','bank')
app = Flask(__name__)
app.secret_key = "martv"
app.permanent_session_lifetime = datetime.timedelta(days=5)
def addTransaction(values):
    connection = mysql.connector.connect(host='localhost', port='3306', user='root', password='ii216695288', database='bank')
    cursor = connection.cursor()
    query = "INSERT INTO bank_transactions (IN_amount,OUT_amount,bank_acount_id,transaction_date,acount_balance_before,acount_balance_after) VALUES (%s, 0, %s, %s, %s, %s), (%s, 0, %s, %s, %s, %s)"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close() 
def getBalance():
    id = session["id"]
    balacne = bank.getValue('current_balance','bank_acounts',f"id = {id}",None)
    balacne = str(balacne[0]).replace("'","")
    balacne = balacne.replace("[","")
    balacne = balacne.replace("]","")
    return balacne
def getBalanceV():
    id = session["id"]
    balacne = int(bank.getValue('current_balance','visacard',f"AcountId = {id}",None)[0])
    if balacne is None:
        return 0
    balacne = str(balacne[0]).replace("'","")
    balacne = balacne.replace("[","")
    balacne = balacne.replace("]","")
    return balacne
@app.route('/')
def i():
    if "user" in session:
        return render_template('menu.html',disable_button = True)
    return render_template('menu.html',disabled_button = False)
@app.route('/login', methods=['GET','POST'])
def login():
    if "user" in session and "id" in session:
        return redirect(url_for("index"))
    return render_template('login.html')
@app.route('/SignUp')
def sign():
    return render_template('signup.html')
@app.route('/signOut', methods=["POST"])
def signOut():
    session.pop("id",None)
    session.pop("user",None)         
    session.pop("email",None)       
    session.pop("password",None)  
    return redirect(url_for("login"))
@app.route('/home', methods=['GET','POST'])
def index():
    if "user" in session:
        return render_template('home.html',balanced=getBalance(),balanced_V = getBalanceV())
    if request.method == 'POST':
        email = request.form.get('emailO')
        if email is None:
            username = request.form.get('Username')          
            email = request.form.get('Email')
            password = request.form.get('Password')
            if not bank.getValue('id','bank_acounts',f"username = '{username}' AND email = '{email}' AND password = '{password}'",None):
                return render_template('login.html',error_message = 'their is no acount like this')
            session.pop("id",None)
            session.pop("user",None)         
            session.pop("email",None)       
            session.pop("password",None)  
            session["user"] = username
            session["email"] = email
            session["password"] = password
            session["id"] = int(bank.getValue('id','bank_acounts',f"username = '{username}' AND email = '{email}' AND password = '{password}'",None)[0])
            return render_template('home.html',balanced=getBalance(),balanced_V = getBalanceV())
        session.pop("id",None)
        session.pop("user",None)         
        session.pop("email",None)       
        session.pop("password",None)  
        email = request.form.get('emailO')
        username = request.form.get('username')
        error_U = bank.exists('bank_acounts', email, 'email',f"email = '{email}'")
        print(error_U)
        error = bank.exists('bank_acounts', username, 'username', f"username = '{username}'")
        print(error)
        if error_U or error:
            return render_template('signup.html', error_message="The email or username is already in use.")
        session["user"] = username
        fname = request.form.get('Fname')
        lname = request.form.get('Lname')
        age = request.form.get('age')
        b_date = request.form.get('B_Date')
        country = request.form.get('country')
        city = request.form.get('city')
        session["email"] = email
        password = request.form.get('password')
        session["password"] = password
        session["id"] = bank.countRows('bank_acounts')
        bank.add((str(session["id"]), '0', username, fname, lname, str(age), b_date, country, city, email, password, str(datetime.datetime.now().date()), '0'), 'bank_acounts')
        return render_template('home.html',balanced=getBalance(),balanced_V = getBalanceV())
    return render_template('signup.html')
@app.route('/AddVisa', methods=['GET', 'POST'])
def AddVisa():
    userID = session["id"]
    visa = request.form.get('visa')
    sDate = request.form.get('sDate')
    eDate = request.form.get('eDate')      
    if bank.exists('bank_acounts', visa, 'VisaCard', f"id = {userID}"):
        return render_template('home.html', error_message_V="Visa card already added",balanced=getBalance(),balanced_V = getBalanceV())
    if not bank.exists('visacard', visa, 'CardNumber', None) or not bank.exists('visacard', eDate, 'endDate', None) or not bank.exists('visacard', sDate, 'startDate', None):
        print('l',sDate,eDate,visa)
        return render_template('home.html', error_message_V="No such visa card exists in the bank system",balanced=getBalance(),balanced_V = getBalanceV())   
    connection = mysql.connector.connect(host='localhost', port='3306', user='root', password='ii216695288', database='bank')
    cursor = connection.cursor()
    query = f"UPDATE bank_acounts SET VisaCard = '{visa}' WHERE id = '{userID}'"
    cursor.execute(query)
    q = f"UPDATE visacard SET AcountId = '{userID}' WHERE CardNumber = '{visa}'"
    cursor.execute(q)
    connection.commit()    
    return render_template('home.html',balanced_V = getBalanceV(),balanced=getBalance(),error_message_V = "visa added succesfully!")
@app.route('/Transaction',methods=['GET','POST'])
def Transaction():
    id = session["id"]
    if not bank.exists('visacard',str(bank.getValue('VisaCard','bank_acounts',f"id = {id}",None)),'CardNumber',f"AcountId = {id}"):
        return render_template('home.html',error_message_T="you don't have visa like this is your acount",balanced_V = getBalanceV(),balanced=getBalance())    
    print(id,int(request.form.get('out_money')))
    IN = int(request.form.get('In_money'))
    OUT = int(request.form.get('out_money'))
    acount_balance = int(getBalance())
    visa_balance = int(getBalanceV())
    if IN > 0 and OUT == 0:
        new_visa_balanced = visa_balance - IN
        new_acount_balanced = acount_balance + IN 
    else:
        if OUT > 0 and IN == 0:
            new_visa_balanced = visa_balance + OUT
            new_acount_balanced = acount_balance - OUT
    if new_acount_balanced < 0 or new_visa_balanced < 0:
        return render_template('home.html',error_message_S="you can make this Transaction",balanced_V = getBalanceV(),balanced=getBalance())
    bank.add((str(IN),str(OUT),str(id),str(datetime.datetime.now().date()),str(acount_balance),str(new_acount_balanced)),'bank_transactions')
    bank.setValue('current_balance',new_acount_balanced,'bank_acounts',f"id = {id}")
    bank.setValue('current_balance',str(new_visa_balanced),'visacard',f"AcountId = {id}")
    return render_template('home.html',balanced_V = getBalanceV(),balanced=getBalance())
@app.route('/SendMoney', methods=["POST"])
def SendMoney():
    id = session["id"]
    amount = int(request.form.get("amount"))
    remail = request.form.get("remail")
    if not bank.exists('bank_acounts',remail,'email',None):
        return render_template('home.html',balanced_V = getBalanceV(),balanced=getBalance(),error_message_S = "the user you are looking for is not available")       
    if amount > int(getBalance()):
        return render_template('home.html',balanced_V = getBalanceV(),balanced=getBalance(),error_message_S = "you don't have enough money in you acount")
    rBalance = int(bank.getValue('current_balance','bank_acounts',f"email = '{remail}'",None)[0])
    r = rBalance + amount
    bank.setValue('current_balance',r,'bank_acounts',f"email = '{remail}'")
    cur = int(getBalance())
    bank.setValue('current_balance',cur - amount,'bank_acounts',f"id = {id}")
    o = int(bank.getValue('id','bank_acounts',f"email = '{remail}'",None)[0])
    values = (amount, id, datetime.datetime.now().date(), cur, cur - amount, amount, o, datetime.datetime.now().date(), rBalance, rBalance + amount)
    addTransaction(values)
    return render_template('home.html',balanced_V = getBalanceV(),balanced=getBalance())
app.run(debug=True)