from flask import request, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import sys

sys.path.append("./UserTypes")
from UserTypes import *

def databaseInit(app):
    '''
    Initialize the database
    '''

    # Setup the mysql with information from config.json
    data = None
    try:
        with open("config.json", "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        print("Config file cannot be found")
        exit(1)

    # configure db with your details
    app.config['SECRET_KEY'] = data["SECRET_KEY"]
    app.config['MYSQL_HOST'] = data['MYSQL_HOST']
    app.config['MYSQL_USER'] = data['MYSQL_USER']
    app.config['MYSQL_PASSWORD'] = data["MYSQL_PASSWORD"]
    app.config['MYSQL_DB'] = data["MYSQL_DB"]

    return MySQL(app)

def convertUser(account, acc_type):
    '''
    Convert raw query from the database and into a user object

    **THIS IS A HELPER FUNCTION, DO NOT USE IT BY ITSELF**
    '''
    if account["type"] == 'customer':
        return Customer(
            id=account["id"],          
            firstName=account["fname"],
            lastName=account["lname"],
            email=account["email"],
            username=account["username"],
            password=account["password"],
            phoneNumber=account["phone"],
            cardNumber=acc_type["cardnumber"],
            type="customer",
            wallet=acc_type["wallet"],
            address=acc_type["address"],
            num_orders=acc_type["num_orders"],
            total_spent=acc_type["total_spent"],
            warnings=acc_type["warnings"],
            isClosed=acc_type["isClosed"],
            isBlacklisted=acc_type["isBlacklisted"],
            isVIP=acc_type["isVIP"],
            free_deliveries=acc_type["free_deliveries"]
        )
    if account["type"] == 'manager':
        return Manager(
            id=account["id"],          
            firstName=account["fname"],
            lastName=account["lname"],
            email=account["email"],
            username=account["username"],
            password=account["password"],
            phoneNumber=account["phone"],
            type="manager"
        )
    if account["type"] == 'chef':
        return Staff(
            id=account["id"],
            firstName=account["fname"],
            lastName=account["lname"],
            email=account["email"],
            username=account["username"],
            password=account["password"],
            phoneNumber=account["phone"],
            salary=acc_type["salary"],
            compliments=acc_type["num_compliment"],
            complaints=acc_type["num_complaint"],
            warnings=acc_type["warnings"],
            demotions=acc_type["demotions"],
            type="chef"
        )
    if account["type"] == 'delivery':
        return Staff(
            id=account["id"],
            firstName=account["fname"],
            lastName=account["lname"],
            email=account["email"],
            username=account["username"],
            password=account["password"],
            phoneNumber=account["phone"],
            salary=acc_type["salary"],
            compliments=acc_type["num_compliment"],
            complaints=acc_type["num_complaint"],
            warnings=acc_type["warnings"],
            demotions=acc_type["demotions"],
            type="delivery"
        )

def getUserInDatabaseByLogin(db):
    '''
    Get a user from the database

    **USE THIS METHOD WHEN A USER IS ATTEMPTING TO LOG IN**

    return the user object if the account exist in the database 
    '''
    # fetch form data
    userDetails = request.form
    username = userDetails['username']
    password = userDetails['password']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        if account["type"] == 'customer':
            cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (str(account["id"]),))
            customer = cursor.fetchone()
            if customer["isClosed"] == 1:
                flash('Account was recently closed.', category = 'error')
            elif customer["isBlacklisted"] == 1:
                flash('Account is blacklisted.', category = 'error')
            else:
                flash('Logged in successfully!', category = 'success')
                return convertUser(account, customer)
        if account["type"] == 'manager':
            cursor.execute('SELECT * FROM employee WHERE employee_id = %s', (str(account["id"]),))
            manager = cursor.fetchone()
            return convertUser(account, manager)
        if account["type"] == 'chef':
            cursor.execute('SELECT * FROM chef WHERE chef_id = %s', (str(account["id"]),))
            chef = cursor.fetchone()
            return convertUser(account, chef)
        if account["type"] == 'delivery':
            cursor.execute('SELECT * FROM delivery WHERE delivery_id = %s', (str(account["id"]),))
            delivery = cursor.fetchone()
            return convertUser(account, delivery)

    else:
        # account does not exist or username/password is incorrect
        flash('Username/password is incorrect.', category = 'error')
        return None

def getUserInDatabaseByID(db, id):
    '''
    Get a user from the database

    **USE THIS METHOD WHEN THE USER ID IS KNOWN**

    return the user object if the account exist in the database 
    '''
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(id)))
    account = cursor.fetchone()

    if account:
        if account["type"] == 'customer':
            cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (str(id),))
            customer = cursor.fetchone()
            return convertUser(account, customer)
        if account["type"] == 'manager':
            cursor.execute('SELECT * FROM employee WHERE employee_id = %s', (str(id),))
            manager = cursor.fetchone()
            return convertUser(account, manager)
        if account["type"] == 'chef':
            cursor.execute('SELECT * FROM chef WHERE chef_id = %s', (str(id),))
            chef = cursor.fetchone()
            return convertUser(account, chef)
        if account["type"] == 'delivery':
            cursor.execute('SELECT * FROM delivery WHERE delivery_id = %s', (str(id),))
            delivery = cursor.fetchone()
            return convertUser(account, delivery)

    else: 
        return None


def verifyNewUser(db):
    '''
    Check to make sure that the new user creation is successful
    '''
    # fetch form data
    userDetails = request.form
    fname = userDetails['fname']
    lname = userDetails['lname']
    email = userDetails['email']
    username = userDetails['uname']
    password = userDetails['password']
    conpass = userDetails['conpass']
    phone = userDetails['phone']
    card = userDetails['cardnum']

    # checks requirements for registration
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()

    if account:
        if account["type"] == 'customer':
            cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (str(account["id"]),))
            customer = cursor.fetchone()
            # customer is blacklisted
            if customer["isBlacklisted"] == 1:
                flash('Account was blacklisted. You can no longer register.', category = 'error')
        else:
            # username must be unique
            flash('Username already exists.', category = 'error')
            return False

    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        # email must be valid
        flash('Email address is invalid.', category = 'error')
    elif not re.search(r"[\d]+", password):
        # password must contain a digit
        flash('Password must contain at least 1 digit.', category = 'error')
    elif not re.search(r"[A-Z]+", password):
        # password must contain an uppercase letter
        flash('Password must contain at least 1 uppercase letter.', category = 'error')
    elif not re.search(r"[a-z]+", password):
        # password must contain a lowercase letter
        flash('Password must contain at least 1 lowercase letter.', category = 'error')
    elif len(password) < 8:
        # password must be at least 8 characters
        flash('Password must contain at least 8 characters.', category = 'error')
    elif password != conpass:
        # checks that password matches confirm password
        flash('Passwords do not match.', category = 'error')
    elif len(phone) != 10:
        # checks that phone number length is valid
        flash('Phone number is invalid. Must be 10 digits.', category = 'error')
    elif len(card) != 16:
        # checks that card number length is valid
        flash('Card number is invalid. Must be 16 digits.', category = 'error')
    else:
        # account pending creation. must be approved by manager to be added to database
        flash('Account successfully created!', category = 'success')
        # inserts new account into database after approval by manager
        cursor.execute("INSERT INTO accounts(fname, lname, email, username, password, phone) VALUES(%s, %s, %s, %s, %s, %s)", (fname, lname, email, username, password, phone))
        cursor.execute("INSERT INTO customer(customer_id) SELECT id FROM accounts WHERE lname = %s and email = %s and username = %s", (lname, email, username,))
        cursor.execute("UPDATE customer SET cardnumber = %s WHERE customer_id = (SELECT id FROM accounts WHERE username = %s)", (card, username,))
        db.connection.commit()
        cursor.close()

        return True

def forgotPassword(db):
    '''
    Updates password in database
    '''
    # fetch form data
    userDetails = request.form
    email = userDetails['email']
    username = userDetails['username']
    newpass = userDetails['newpass']
    conpass = userDetails['conpass']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND username = %s', (email, username,))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        if not re.search(r"[\d]+", newpass):
        # password must contain a digit
            flash('Password must contain at least 1 digit.', category = 'error')
        elif not re.search(r"[A-Z]+", newpass):
            # password must contain an uppercase letter
            flash('Password must contain at least 1 uppercase letter.', category = 'error')
        elif not re.search(r"[a-z]+", newpass):
            # password must contain a lowercase letter
            flash('Password must contain at least 1 lowercase letter.', category = 'error')
        elif len(newpass) < 8:
            # password must be at least 8 characters
            flash('Password must contain at least 8 characters.', category = 'error')
        elif newpass != conpass:
            # checks that password matches confirm password
            flash('Passwords do not match.', category = 'error')
        else:
            cursor.execute('UPDATE accounts SET password = %s WHERE email = %s AND username = %s', (newpass, email, username,))
            flash('Successfully changed password.', category = 'success')
            db.connection.commit()
            cursor.close()

            return True
    else:
        flash('Email/username does not exist.', category = 'error')

def changeAddress(db, user):
    '''
    Updates address in database
    '''
    # fetch form data
    userDetails = request.form
    address = userDetails['address']
    city = userDetails['city']
    state = userDetails['state']
    zipcode = userDetails['zipcode']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(user.id),))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
            full_address = address + ", " + city + ", " + state + " " + zipcode
            if user.address == None:
                flash('Successfully set default address.', category = 'success')
            else:
                flash('Successfully changed address.', category = 'success')
            cursor.execute('UPDATE customer SET address = %s WHERE customer_id = %s', (full_address, str(user.id),))
            db.connection.commit()
            cursor.close()
            user.setAddress(user, full_address)

            return True
    else:
        flash('Email/username does not exist.', category = 'error')

def changeCard(db, user):
    '''
    Updates card number in database
    '''
    # fetch form data
    userDetails = request.form
    card = userDetails['card']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(user.id),))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        if len(card) != 16:
            # checks that card number length is valid
            flash('Card number is invalid. Must be 16 digits.', category = 'error')
        else:
            flash('Successfully changed payment method.', category = 'success')
            user.setCardNumber(db, card)
            
            return True
    else:
        flash('Email/username does not exist.', category = 'error')

    cursor.close()

def chargeFunds(db, user):
    '''
    Updates wallet in database
    '''
    # fetch form data
    userDetails = request.form
    funds = userDetails['funds']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(user.id),))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        if float(funds) <= 0:
            # checks that value to add is valid
            flash('Amount to be deposited must be $0.01 or more.', category = 'error')
        else:
            funds = float(funds) + user.wallet
            flash('Successfully deposited more funds.', category = 'success')
            user.setWallet(db, funds)

            return True
    else:
        flash('Email/username does not exist.', category = 'error')

    cursor.close()

def deleteAcc(db, user):
    '''
    Set account to closed in database
    '''

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(user.id),))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        user.setisClosed(db, 1)
        db.connection.commit()
        cursor.close()

        return True

def updateQuantity(cart, index, action):
    '''
    Updates quantity in cart
    '''
    # decrease item quantity by 1
    if action == "minus":
        cart["quantity"][index] -= 1
    # increase item quantity by 1
    elif action == "plus":
        cart["quantity"][index] += 1
    return cart

def getCartItems(db, cart):
    '''
    Get cart items from database
    '''
    data = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    index = 0
    for item in cart["dish"]:
        cursor.execute('SELECT * FROM dish WHERE dish_id = %s', (str(item),))
        rawQuery = cursor.fetchone()
        rawQuery["quantity"] = cart["quantity"][index]
        index += 1
        data.append(rawQuery)

    return data

def getCartInfo(cart, vipStatus):
    '''
    Gets cart info based on customer's cart
    '''
    info = {}
    subtotal = 0
    num_items = 0
    for row in cart:
        subtotal += row["quantity"]*row["price"]
        num_items += row["quantity"]

    # Calculate the subtotal, tax, and total
    info["num_items"] = num_items
    info["subtotal"] = subtotal
    info["tax"] = round(subtotal*0.08875, 2)
    if vipStatus == 1:
        info["discount"] = round(subtotal*0.05, 2)
    else:
        info["discount"] = 0.00
    info["total"] = round(subtotal + info["tax"] - info["discount"], 2)

    return info

def getDishCount(db, dish_id):
    '''
    Gets dish count in database
    '''
    # checks if dish exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_id = %s', (str(dish_id),))
    dish = cursor.fetchone()
    cursor.close()

    if dish:
        return dish["count"]

def setDishCount(db, dish_id, num):
    '''
    Updates dish count in database
    '''
    # checks if dish exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_id = %s', (str(dish_id),))
    dish = cursor.fetchone()

    if dish:
        cursor.execute('UPDATE dish SET count = %s WHERE dish_id = %s', (str(num), str(dish_id),))
        db.connection.commit()

    cursor.close()

def retrieveDispute(db):
    userDetails = request.form
    fname = userDetails['firstname']
    lname = userDetails['lastname']
    disputerid = userDetails['userid']
    complainerid = userDetails['complainerid']
    disputedescription = userDetails['deliverydispute']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute("INSERT INTO dispute (first_name, last_name, disputer_id, complainer_id, dispute_content, dispute_date) VALUES(%s, %s, %s,%s, %s, CURDATE())", (fname,lname,disputerid,complainerid,disputedescription))
    db.connection.commit()
    cursor.close()

    return True

def retrieveComplaint(db):
    print("retrieveomcplaint")
    userDetails = request.form
    fname = userDetails['firstname']
    lname = userDetails['lastname']
    receiverid = userDetails['receiverid']
    complainerid = userDetails['userid']
    complaintdescription = userDetails['complaintbox']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute("INSERT INTO complaint (first_name, last_name, complainer_id, receiver_id, complaint_content, complaint_date) VALUES(%s, %s, %s, %s, %s, CURDATE())", (fname,lname,complainerid,receiverid,complaintdescription))
    db.connection.commit()
    cursor.close()

    return True

def retrieveCompliment(db):
    print("retrievecompliment")
    userDetails = request.form
    fname = userDetails['firstname']
    lname = userDetails['lastname']
    receiverid = userDetails['receiverid']
    complainerid = userDetails['userid']
    complaintdescription = userDetails['complaintbox']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute("INSERT INTO compliment (first_name, last_name, complimenter_id, receiver_id, compliment_content, compliment_date) VALUES(%s, %s, %s, %s, %s, CURDATE())", (fname,lname,complainerid,receiverid,complaintdescription))
    db.connection.commit()
    cursor.close()

    return True

def loadDisputes(db):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT DISTINCT dispute.first_name, dispute.last_name, dispute.dispute_id, dispute.disputer_id, complaint.complainer_id, complaint.complaint_date, dispute.disputer_id, dispute.dispute_date, dispute.dispute_content FROM dispute INNER join complaint on complaint.receiver_id = dispute.disputer_id;')
    results = cursor.fetchall()
    cursor.close()
    return results

def loadPastDeliveries(db):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM PastDeliveries')
    results = cursor.fetchall()
    cursor.close()
    return results

def loadSpecials(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_type=%s and chef=%s', (['special'], str(user.id)) )
    results = cursor.fetchall()
    print(results)
    cursor.close()
    return results

def loadEntrees(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_type=%s and chef=%s', (['entree'], str(user.id)) )
    results = cursor.fetchall()
    print(results)
    cursor.close()
    return results

def loadAppt(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_type=%s and chef=%s', (['appetizer'], str(user.id)) )
    results = cursor.fetchall()
    print(results)
    cursor.close()
    return results

def loadDesserts(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_type=%s and chef=%s', (['dessert'], str(user.id)) )
    results = cursor.fetchall()
    print(results)
    cursor.close()
    return results

def loadDrinks(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE dish_type=%s and chef=%s', (['drink'], str(user.id)) )
    results = cursor.fetchall()
    print(results)
    cursor.close()
    return results

def loadMenu(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dish WHERE chef=%s', (str(user.id)) )
    results = cursor.fetchall()
    cursor.close()
    return results

def edititem(db):
    itemDetails = request.form
    newimage = itemDetails['newimage']
    itemname = itemDetails['itemname']
    description = itemDetails['editdescription']
    editprice = itemDetails['editprice']
    dishid = itemDetails['dishid']

    print("deeznutz\n")
    print(dishid)
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('UPDATE dish SET img = %s, name = %s, description = %s,  price = %s WHERE dish_id = %s', (newimage,itemname,description,editprice,dishid))
    db.connection.commit()
    cursor.close()

def removeitem(db):
    itemDetails = request.form
    dishid = itemDetails['removeitem']
    print(dishid)
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('DELETE FROM dish WHERE dish_id=%s', [dishid] )
    db.connection.commit()
    cursor.close()

def additem(db):
    itemDetails = request.form
    chefid = itemDetails['chefid']
    itemtype = itemDetails['dishtype']
    itemimage = itemDetails['image']
    itemname = itemDetails['itemname']
    itemdescription = itemDetails['description']
    itemprice = itemDetails['price']
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('INSERT INTO dish (dish_type, name, price, description, img, chef) VALUES (%s, %s, %s, %s, %s, %s)', (itemtype, itemname, itemprice, itemdescription, itemimage, chefid))
    db.connection.commit()
    cursor.close()

def retrieveUsers(db):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM chef INNER JOIN accounts WHERE chef_id = id')
    chef = cursor.fetchall()

    cursor.execute('SELECT * FROM delivery INNER JOIN accounts WHERE delivery_id = id')
    delivery = cursor.fetchall()


    cursor.execute('SELECT * FROM customer INNER JOIN accounts WHERE customer_id = id')
    customer = cursor.fetchall()
    # print(customer,"\n")

    return chef, delivery, customer

def loadCompliments(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM compliment WHERE receiver_id = %s', (str(user.id),))
    results = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM compliment WHERE receiver_id = %s', (str(user.id),))
    count = cursor.fetchone()
    if user.userType == "chef":
        print('THIS IS THE COMPLIMENT COUNT FOR CHEF', count["COUNT(*)"])
        cursor.execute('UPDATE chef SET num_compliment = %s WHERE chef_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "delivery":
        print('THIS IS THE COMPLIMENT COUNT FOR DELIVERY', count["COUNT(*)"])
        cursor.execute('UPDATE delivery SET num_compliment = %s WHERE delivery_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "customer":
        print('THIS IS THE COMPLIMENT COUNT FOR CUSTOMER', count["COUNT(*)"])
        cursor.execute('UPDATE customer SET num_compliment = %s WHERE customer_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "manager":
        cursor.execute('SELECT * from compliment')
        results = cursor.fetchall()
    cursor.close()

    return results

def loadComplaints(db,user):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM complaint WHERE receiver_id = %s', (str(user.id),))
    results = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM complaint WHERE receiver_id = %s', (str(user.id),))
    count = cursor.fetchone()
    if user.userType == "chef":
        print('THIS IS THE COMPLAINT COUNT FOR CHEF', count["COUNT(*)"])
        cursor.execute('UPDATE chef SET num_complaint = %s WHERE chef_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "delivery":
        print('THIS IS THE COMPLAINT COUNT FOR DELIVERY', count["COUNT(*)"])
        cursor.execute('UPDATE delivery SET num_complaint = %s WHERE delivery_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "customer":
        print('THIS IS THE COMPLAINT COUNT FOR CUSTOMER', count["COUNT(*)"])
        cursor.execute('UPDATE customer SET num_complaint = %s WHERE customer_id = %s', (count["COUNT(*)"], str(user.id),))
        db.connection.commit()
    if user.userType == "manager":
        cursor.execute('SELECT * from complaint')
        results = cursor.fetchall()
    cursor.close()

    return results

def loadWarnings(db,user):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if user.userType == "chef":
        cursor.execute('SELECT warnings FROM chef WHERE chef_id = %s', (str(user.id),))
        count = cursor.fetchone()
        print('THIS IS THE WARNING COUNT FOR CHEF', count["warnings"])
        db.connection.commit()
    if user.userType == "delivery":
        cursor.execute('SELECT warnings FROM delivery WHERE delivery_id = %s', (str(user.id),))
        count = cursor.fetchone()
        print('THIS IS THE WARNING COUNT FOR DELIVERY', count["warnings"])
        db.connection.commit()
    if user.userType == "customer":
        cursor.execute('SELECT warnings FROM customer WHERE customer_id = %s', (str(user.id),))
        count = cursor.fetchone()
        print('THIS IS THE WARNING COUNT FOR CUSTOMER', count["warnings"])
        db.connection.commit()
    cursor.close()
    return True

def addwarning(db):
    details = request.form
    usertype = details['usertype']
    userid = details['givewarning']
    commentType = details['commentType']
    commentID = details['id']
    print(usertype,userid)
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if usertype == "customer":
        cursor.execute('UPDATE customer SET warnings = warnings + 1 WHERE customer_id = %s', userid)
        db.connection.commit()
    if usertype == "chef":
        cursor.execute('UPDATE chef SET warnings = warnings + 1 WHERE chef_id = %s', userid)
        db.connection.commit()
    if usertype == "delivery":
        cursor.execute('UPDATE delivery SET warnings = warnings + 1 WHERE delivery_id = %s', userid)
        db.connection.commit()
    if usertype == "unknown":
        # chefs
        if userid == '2' or userid == '3': 
            cursor.execute('UPDATE chef SET warnings = warnings + 1 WHERE chef_id = %s', userid)
            db.connection.commit()
        # delivery
        if userid == '4' or userid == '5':
            cursor.execute('UPDATE delivery SET warnings = warnings + 1 WHERE delivery_id = %s', userid)
            db.connection.commit()
        # customers
        if userid >= '6':
            cursor.execute('UPDATE customer SET warnings = warnings + 1 WHERE customer_id = %s', userid)
            db.connection.commit()
    if commentType == "compliment":
            cursor.execute('DELETE FROM compliment WHERE compliment_id = %s', commentID)
            db.connection.commit()
    if commentType == "complaint":
        cursor.execute('DELETE FROM complaint WHERE complaint_id = %s', commentID)
        db.connection.commit()
    if commentType == "dispute":
        cursor.execute('DELETE FROM dispute WHERE dispute_id = %s', commentID)
        db.connection.commit()
    if commentType == "":
        print("donothing")
    cursor.close()
    return True

def addforumwarning(db):
    details = request.form
    usertype = details['usertype']
    userid = details['giveforumwarning']
    print(usertype,userid)
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if usertype == "customer":
       cursor.execute('UPDATE customer SET warnings = warnings + 1 WHERE customer_id = %s', userid)
       db.connection.commit()
    if usertype == "chef":
       cursor.execute('UPDATE chef SET warnings = warnings + 1 WHERE chef_id = %s', userid)
       db.connection.commit()
    if usertype == "delivery":
       cursor.execute('UPDATE delivery SET warnings = warnings + 1 WHERE delivery_id = %s', userid)
       db.connection.commit()
    cursor.close()
    return True

def retrievePost(db):
    userDetails = request.form
    postAuthor = userDetails['author']
    postTitle = userDetails['Title']
    postdescription = userDetails['post-comment']
    userid = userDetails['userID']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute('INSERT INTO post (post_author, post_title, post_content, user_id, post_date) VALUES(%s, %s, %s, %s, CURDATE())', (postAuthor, postTitle, postdescription, userid))
    db.connection.commit()
    cursor.close()

    return True

def loadPost(db):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM post')
    results = cursor.fetchall()
    cursor.close()
    return results

def retrievePostComment(db):
    userDetails = request.form
    postcommentauthor = userDetails['postcommentauthor']
    postcommentcontent = userDetails['comment-box']
    userid = userDetails['userID']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute("INSERT INTO postcomments (postcomment_author, postcomment_content, user_id, postcomment_date) VALUES(%s, %s, %s, CURDATE())", (postcommentauthor, postcommentcontent, userid))
    db.connection.commit()
    cursor.close()

    return True

def loadPostComments(db):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM postcomments')
    results = cursor.fetchall()
    cursor.close()
    return results

def retrieveForumWarnings(db):
    userDetails = request.form
    warningAuthor = userDetails['warningAuthor']
    warningAccused = userDetails['warningAccused']
    warningdescription = userDetails['warning-comment']

    cursor = db.connection.cursor()
    #insert data into dispute table in database
    cursor.execute("INSERT INTO forumwarnings (forumwarning_author, forumwarning_accused, user_id, reported_id, forumwarning_content, forumwarning_date) VALUES(%s, %s, %s, %s, %s, CURDATE())", (warningAuthor,warningAccused,7,6,warningdescription))
    db.connection.commit()
    cursor.close()

    return True

def loadForumWarnings(db):
    results = []
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM forumwarnings')
    results = cursor.fetchall()
    cursor.close()
    return results


def removeComment(db):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    userDetails = request.form
    commentType = userDetails['commentType']
    commentID = userDetails['id']
    if commentType == "compliment":
        cursor.execute('DELETE FROM compliment WHERE compliment_id = %s', commentID)
        db.connection.commit()
        cursor.close()
    if commentType == "complaint":
        cursor.execute('DELETE FROM complaint WHERE complaint_id = %s', commentID)
        db.connection.commit()
        cursor.close()
    if commentType == "dispute":
        cursor.execute('DELETE FROM dispute WHERE dispute_id = %s', commentID)
        db.connection.commit()
        cursor.close()
    return True

def retrievePrevious(db):
    '''
    Gets customers that are blacklisted/closed acc
    '''

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer INNER JOIN accounts ON customer.customer_id = accounts.id WHERE (isBlacklisted = 1 OR isClosed = 1) AND status = 1')
    customers = cursor.fetchall()
    cursor.close()
    return customers

def clearDeposit(db):
    '''
    Clear deposit from customer who left the system
    '''
    customer_id = request.form['customer_id']
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (str(customer_id),))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        cursor.execute('UPDATE customer SET wallet = 0')
        user = getUserInDatabaseByID(db, customer_id)
        user.setWallet(0)
    db.connection.commit()
    cursor.close()

def deleteAccount(db):
    '''
    Delete account of customer who left the system
    '''
    customer_id = request.form['customer_id']
    lost_type = request.form['lost_type']

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if lost_type == "blacklisted":
        cursor.execute('UPDATE customer SET status = 0 WHERE customer_id = %s AND isBlacklisted = 1', (str(customer_id)))
    else:
        cursor.execute('DELETE FROM forumwarnings WHERE user_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM postcomments WHERE user_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM post WHERE user_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM deliveryBid WHERE customer_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM orderDetails WHERE customer_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM orders WHERE customer_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM PastDeliveries WHERE customer_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM compliment WHERE receiver_id = %s OR complimenter_id = %s', (str(customer_id), str(customer_id),))
        cursor.execute('DELETE FROM complaint WHERE receiver_id = %s OR complainer_id = %s', (str(customer_id), str(customer_id),))
        cursor.execute('DELETE FROM dispute WHERE disputer_id = %s OR complainer_id = %s', (str(customer_id), str(customer_id),))
        cursor.execute('DELETE FROM customer WHERE customer_id = %s', (str(customer_id),))
        cursor.execute('DELETE FROM accounts WHERE id = %s', (str(customer_id),))
        print("thos")

    db.connection.commit()
    cursor.close()