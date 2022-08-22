from user import User
import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import request
from dish import *

class Customer(User):
    def __init__(self, **kwargs):
        '''
        Create a new customer in session

        Parameters:
        ----------
        id : int
        firstName : str
        lastName : str
        email : str
        username : str
        password : str
        phoneNumber : str
        type : str
        wallet : float
        cardNumber : str
        address : str
        num_orders : int
        total_spent : float
        warnings : int
        isClosed : boolean
        isBlacklisted : boolean
        isVIP : boolean
        free_deliveries : int
        '''
        super().__init__(**kwargs)

        try:
            self.cardNumber = kwargs["cardNumber"]
        except KeyError:
            self.cardNumber = None

        try:
            self.isVIP = kwargs["isVIP"]
        except KeyError:
            self.isVIP = 0

        try:
            self.wallet = kwargs["wallet"]
        except KeyError:
            self.wallet = 0.0

        try:
            self.address = kwargs["address"]
        except KeyError:
            self.address = None

        try:
            self.num_orders = kwargs["num_orders"]
        except KeyError:
            self.num_orders = 0

        try:
            self.total_spent = kwargs["total_spent"]
        except KeyError:
            self.total_spent = 0.0

        try:
            self.warnings = kwargs["warnings"]
        except KeyError:
            self.warnings = 0

        try:
            self.isBlacklisted = kwargs["isBlacklisted"]
        except KeyError:
            self.isBlacklisted = 0

        try:
            self.isClosed = kwargs["isClosed"]
        except KeyError:
            self.isClosed = 0

        try:
            self.free_deliveries = kwargs["free_deliveries"]
        except KeyError:
            self.free_deliveries = 0

    def setCardNumber(self, db, cardNumber = None):
        if cardNumber == None:
            return

        self.cardNumber = cardNumber

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET cardnumber = %s WHERE customer_id = %s', (self.cardNumber, str(self.id),))
        db.connection.commit()
        cursor.close()

    def setisVIP(self, db, isVIP = None):
        if isVIP == None:
            return

        self.isVIP = isVIP

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET isVIP = %s WHERE customer_id = %s', (str(self.isVIP), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setWallet(self, db, wallet = None):
        if wallet == None:
            return

        self.wallet = wallet

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET wallet = %s WHERE customer_id = %s', (str(self.wallet), str(self.id),))
        db.connection.commit()
        cursor.close()
    
    def setAddress(self, db, address = None):
        if address == None:
            return

        self.address = address

    def setNumOrders(self, db, num_orders = None):
        if num_orders == None:
            return

        self.num_orders = num_orders

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET num_orders = %s WHERE customer_id = %s', (str(self.num_orders), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setTotalSpent(self, db, total_spent = None):
        if total_spent == None:
            return

        self.total_spent = total_spent

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET total_spent = %s WHERE customer_id = %s', (str(self.total_spent), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setWarnings(self, db, warnings = None):
        if warnings == None:
            return

        self.warnings = warnings

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET warnings = %s WHERE customer_id = %s', (str(self.warnings), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setisBlacklisted(self, db, isBlacklisted = None):
        if isBlacklisted == None:
            return

        self.isBlacklisted = isBlacklisted

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET isBlacklisted = %s WHERE customer_id = %s', (str(self.isBlacklisted), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setisClosed(self, db, isClosed = None):
        if isClosed == None:
            return

        self.isClosed = isClosed

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET isClosed = %s WHERE customer_id = %s', (str(self.isClosed), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setFreeDeliveries(self, db, free_deliveries = None):
        if free_deliveries == None:
            return

        self.free_deliveries = free_deliveries

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE customer SET free_deliveries = %s WHERE customer_id = %s', (str(self.free_deliveries), str(self.id),))
        db.connection.commit()
        cursor.close()

    def setName(self, db, firstName = None, lastName = None):
        if firstName == None or lastName == None:
            return

        # DB stuff go here

        super().setName(firstName, lastName)

    def setEmail(self, db, email = None):
        '''
        Update the user's email
        '''
        if email == None:
            return

        # DB stuff go here

        super().setEmail(email)

    def setUsername(self, db, username = None):
        '''
        Update the user's username
        '''
        if username == None:
            return

        super().setUsername(username)

    def setPhoneNumber(self, db, phoneNumber = None):
        '''
        Update the user's phone number
        '''
        if phoneNumber == None:
            return

        super().setPhoneNumber(phoneNumber)

    def getFavoriteDishes(self, db):
        '''
        Get and set the user's top dishes
        '''       
        self.favoriteDishes = []

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT order_id, customer_id, dish_id, SUM(quantity) FROM orderDetails WHERE customer_id = %s GROUP BY customer_id, dish_id ORDER BY SUM(quantity) DESC', (str(self.id),))
        favorites = cursor.fetchmany(3)
        for dish in favorites:
            dish_id = dish["dish_id"]
            cursor.execute('SELECT * FROM dish WHERE dish_id = %s', (str(dish_id),))
            item = cursor.fetchone()
            self.favoriteDishes.append(Dish(item["dish_id"], item["dish_type"], item["name"], item["price"], item["description"], item["img"], item["chef"], item["rating"], item["num_ratings"], item["count"], item["status"]))

        return self.favoriteDishes

    def makeComment(self, db, dt):
        '''
        Insert comment into database
        '''
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        # obtain form details
        userDetails = request.form
        if "compliment-dish-submit" in request.form:
            comment = "compliment"
            content = userDetails['compliment-box']
            dish_id = userDetails['dish_id']

            cursor.execute('SELECT chef FROM dish WHERE dish_id = %s', (str(dish_id),))
            chef_id = cursor.fetchone()
            recipient_id = chef_id["chef"]
            cursor.execute('INSERT INTO compliment(first_name, last_name, complimenter_id, receiver_id, compliment_date, compliment_content) VALUES (%s, %s, %s, %s, %s, %s)', (self.firstName, self.lastName, str(self.id), str(recipient_id), dt, content))

        if "complaint-dish-submit" in request.form:
            comment = "complaint"
            content = userDetails['complaint-box']
            dish_id = userDetails['dish_id']

            cursor.execute('SELECT chef FROM dish WHERE dish_id = %s', (str(dish_id),))
            chef_id = cursor.fetchone()
            recipient_id = chef_id["chef"]
            cursor.execute('INSERT INTO complaint(first_name, last_name, complainer_id, receiver_id, complaint_date, complaint_content) VALUES (%s, %s, %s, %s, %s, %s)', (self.firstName, self.lastName, str(self.id), str(recipient_id), dt, content))

        if "compliment-delivery-submit" in request.form:
            comment = "compliment"
            content = userDetails['compliment-box']
            order_id = userDetails['order_id']

            cursor.execute('SELECT delivery_id FROM orders WHERE order_id = %s', (str(order_id),))
            delivery_id = cursor.fetchone()
            recipient_id = delivery_id["delivery_id"]
            cursor.execute('INSERT INTO compliment(first_name, last_name, complimenter_id, receiver_id, compliment_date, compliment_content) VALUES (%s, %s, %s, %s, %s, %s)', (self.firstName, self.lastName, str(self.id), str(recipient_id), dt, content))
            
        if "complaint-delivery-submit" in request.form:
            comment = "complaint"
            content = userDetails['complaint-box']
            order_id = userDetails['order_id']

            cursor.execute('SELECT delivery_id FROM orders WHERE order_id = %s', (str(order_id),))
            delivery_id = cursor.fetchone()
            recipient_id = delivery_id["delivery_id"]
            cursor.execute('INSERT INTO complaint(first_name, last_name, complainer_id, receiver_id, complaint_date, complaint_content) VALUES (%s, %s, %s, %s, %s, %s)', (self.firstName, self.lastName, str(self.id), str(recipient_id), dt, content))

        print(comment, content)

        db.connection.commit()
        cursor.close()