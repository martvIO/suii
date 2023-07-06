from DataBaseConnector import DataBase
from flask import Flask, render_template, request,redirect,url_for, session
import mysql.connector,os,datetime
from utilities import addTransaction,getBalance,getBalanceV
from dotenv import load_dotenv
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
SECRET = os.getenv("SECRET")
global bank
bank = DataBase('localhost','3306','root',PASSWORD,'bank')
app = Flask(__name__)
app.secret_key = SECRET
app.permanent_session_lifetime = datetime.timedelta(days=5)
@app.route('/')
def i():
    if "user" in session:
        return render_template('menu.html',disable_button = True) #if the user is already loged in go to home page
    return render_template('menu.html',disabled_button = False) #else go to sign up and log in page
@app.route('/login', methods=['GET','POST'])
def login():
    if "user" in session and "id" in session:
        return redirect(url_for("index")) #if the user is already loged in go to home page (like when he cxome visit the web again and the info steal in the session)
    return render_template('login.html') #else go to sign up and log in page
@app.route('/SignUp')
def sign():
    return render_template('signup.html') #go to sign up page
@app.route('/signOut', methods=["POST"])
def signOut():
    session.pop("id",None)
    session.pop("user",None)         
    session.pop("email",None)       
    session.pop("password",None)  
    #remove all the info from the old user
    return redirect(url_for("login")) # go to log in page
@app.route('/home', methods=['GET','POST'])
def index():
    if "user" in session: 
        return render_template('home.html',balanced=getBalance(session,bank),balanced_V = getBalanceV(session,bank)) #if the user info in the seesion go to the home page
    if request.method == 'POST':
        email = request.form.get('emailO')
        if email is None:
            # if the page we take the action from doesn't have the input box that have name emailO (sign up page) that's means that the user try to log in 
            username = request.form.get('Username')          
            email = request.form.get('Email')
            password = request.form.get('Password')
            if not bank.getValue('id','bank_acounts',f"username = '{username}' AND email = '{email}' AND password = '{password}'",None): 
                #check if their are this values in the database 
                return render_template('login.html',error_message = 'their is no acount like this')
            session.pop("id",None)
            session.pop("user",None)         
            session.pop("email",None)       
            session.pop("password",None) 
            #remove the old user info from the session if their was 
            session["user"] = username
            session["email"] = email
            session["password"] = password
            session["id"] = int(bank.getValue('id','bank_acounts',f"username = '{username}' AND email = '{email}' AND password = '{password}'",None)[0]) 
            #add the new values to the session
            return render_template('home.html',balanced=getBalance(session,bank),balanced_V = getBalanceV(session,bank))
            #bakanced is the current balance that the user have in the acount and balanced_V is the current visa balance
        session.pop("id",None)
        session.pop("user",None)         
        session.pop("email",None)       
        session.pop("password",None)
        #remove the old user info from the session if their was  
        email = request.form.get('emailO')
        username = request.form.get('username')
        error_U = bank.exists('bank_acounts', email, 'email',f"email = '{email}'")
        print(error_U)
        error = bank.exists('bank_acounts', username, 'username', f"username = '{username}'")
        print(error)
        if error_U or error:
            return render_template('signup.html', error_message="The email or username is already in use.")
        #check if the email or the username had already been taken
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
        #take the user info and add it to the database and the session
        return render_template('home.html',balanced=getBalance(session,bank),balanced_V = getBalanceV(session,bank))
    return render_template('signup.html') # if the user try to go to home page without sign up or log in it will send him to sign up page
@app.route('/AddVisa', methods=['GET', 'POST'])
def AddVisa():
    userID = session["id"]
    visa = request.form.get('visa')
    sDate = request.form.get('sDate')
    eDate = request.form.get('eDate')      
    if bank.exists('bank_acounts', visa, 'VisaCard', f"id = {userID}"):
        return render_template('home.html', error_message_V="Visa card already added",balanced=getBalance(session,bank),balanced_V = getBalanceV(session,bank))
    if not bank.exists('visacard', visa, 'CardNumber', None) and not bank.exists('visacard', eDate, 'endDate', None) and not bank.exists('visacard', sDate, 'startDate', None):
        return render_template('home.html', error_message_V="No such visa card exists in the bank system",balanced=getBalance(session,bank),balanced_V = getBalanceV(session,bank))   
    #check if the visa is real
    connection = mysql.connector.connect(host='localhost', port='3306', user='root', password=PASSWORD, database='bank')
    cursor = connection.cursor()
    query = f"UPDATE bank_acounts SET VisaCard = '{visa}' WHERE id = '{userID}'"
    cursor.execute(query)
    q = f"UPDATE visacard SET AcountId = '{userID}' WHERE CardNumber = '{visa}'"
    cursor.execute(q)
    #now the acount have a visa card and the visa card is only accesable from this acount 
    connection.commit()    
    return render_template('home.html',balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank),error_message_V = "visa added succesfully!")
@app.route('/Transaction',methods=['GET','POST'])
def Transaction():
    id = session["id"]
    if not bank.exists('visacard',str(bank.getValue('VisaCard','bank_acounts',f"id = {id}",None)),'CardNumber',f"AcountId = {id}"):
        return render_template('home.html',error_message_T="you don't have visa like this is your acount",balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank))    
    #if the acount doesn't have a visa card the user will not be able to make transaction 
    IN = int(request.form.get('In_money'))
    OUT = int(request.form.get('out_money'))
    #take the amount of money the user want to take or send from the visa
    acount_balance = int(getBalance(session,bank))
    visa_balance = int(getBalanceV(session,bank))
    #take the current balance for the acount and the visa 
    if IN > 0 and OUT == 0:
        new_visa_balanced = visa_balance - IN
        new_acount_balanced = acount_balance + IN 
    else:
        if OUT > 0 and IN == 0:
            new_visa_balanced = visa_balance + OUT
            new_acount_balanced = acount_balance - OUT
        else:
            return render_template('home.html',error_message_S="put i values",balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank))       
    #check if the user want to put or send money to visa
    if new_acount_balanced < 0 or new_visa_balanced < 0:
        return render_template('home.html',error_message_S="you can make this Transaction",balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank))  
    #if the user doesn't have enough money for this transaction it will show a error on the web
    bank.add((str(IN),str(OUT),str(id),str(datetime.datetime.now().date()),str(acount_balance),str(new_acount_balanced)),'bank_transactions')
    #add to bank transactions history 
    bank.setValue('current_balance',new_acount_balanced,'bank_acounts',f"id = {id}")
    bank.setValue('current_balance',str(new_visa_balanced),'visacard',f"AcountId = {id}")
    #set the new balance for the visa and for the acount 
    return render_template('home.html',balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank))
@app.route('/SendMoney', methods=["POST"])
def SendMoney():
    id = session["id"]
    amount = int(request.form.get("amount"))
    remail = request.form.get("remail")
    #take the amount you want to send and the email for the one who will recieve it
    if not bank.exists('bank_acounts',remail,'email',None):
        return render_template('home.html',balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank),error_message_S = "the user you are looking for is not available")       
    if amount > int(getBalance(session,bank)):
        return render_template('home.html',balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank),error_message_S = "you don't have enough money in you acount")
    #check if the email exist and if you have enough money in you bank acount
    rBalance = int(bank.getValue('current_balance','bank_acounts',f"email = '{remail}'",None)[0])
    #take the current balance for the one you want to send him the money
    bank.setValue('current_balance',rBalance + amount,'bank_acounts',f"email = '{remail}'")
    #set the balance for one that will recieve your money to the new balance = his balance + amount
    cur = int(getBalance(session,bank))
    bank.setValue('current_balance',cur - amount,'bank_acounts',f"id = {id}")
    #set your new balance
    o = int(bank.getValue('id','bank_acounts',f"email = '{remail}'",None)[0])
    values = (amount, id, datetime.datetime.now().date(), cur, cur - amount, amount, o, datetime.datetime.now().date(), rBalance, rBalance + amount)
    addTransaction(values)
    #add the transaction to bank transction history
    return render_template('home.html',balanced_V = getBalanceV(session,bank),balanced=getBalance(session,bank))
app.run(debug=True)