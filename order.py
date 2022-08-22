import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import request
from dish import *

class Order():
    def __init__(self, order_id : int, customer_id : int, num_items : int, subtotal : float, tax : float, discount : float, delivery_fee : float, total : float, datetime : str, type : str, status : int, isFree : int):
        '''
        Create a dish object that stores its components

        Parameters
        ----------
        order_id    : int
        customer_id : int
        num_items   : int
        subtotal    : float
        tax         : float
        discount    : float
        delivery_fee: float
        total       : float
        datetime    : str
        type        : str
        status      : boolean
        isFree      : boolean
        '''
        self.order_id = order_id
        self.customer_id = customer_id
        self.num_items = num_items
        self.subtotal = subtotal
        self.tax = tax
        self.discount = discount
        self.delivery_fee = delivery_fee
        self.total = total
        self.datetime = datetime
        self.type = type
        self.status = status
        self.isFree = isFree

    def __str__(self):
        return f'Order ID: {self.order_id}\nCustomer: {self.customer_id}\nNumber of Items: {self.num_items}\nTotal: {str(self.total)}\nType: {self.type}\n\n'

    @staticmethod
    def insertIntoOrders(db : MySQL, user, cartInfo, order_type, datetime, isFree):
        '''
        Inserts new order into a database
        '''
        status = 0
        if order_type == 'pickup' or isFree == 1:
            status = 1
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO orders (customer_id, num_items, subtotal, tax, discount, total, datetime, type, status, isFree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                (str(user.id), str(cartInfo["num_items"]), str(cartInfo["subtotal"]), str(cartInfo["tax"]), str(cartInfo["discount"]), str(cartInfo["total"]), datetime, order_type, str(status), str(isFree)))
        cursor.execute('SELECT order_id FROM orders WHERE customer_id = %s ORDER BY order_id DESC', (str(user.id),))
        order_id = cursor.fetchone()
        if isFree == 0 and order_type == 'delivery':
            cursor.execute('SELECT delivery_id FROM delivery')
            personnel = cursor.fetchall()
            for person in personnel:
                cursor.execute('INSERT INTO deliveryBid(order_id, customer_id, delivery_id) VALUES (%s, %s, %s)', (str(order_id["order_id"]), str(user.id), str(person["delivery_id"])))
                print(person)
        db.connection.commit()
        cursor.close()

        return order_id["order_id"]

    @staticmethod
    def insertIntoDetails(db : MySQL, user, order_id, cart):
        '''
        Insert order details into a database
        '''
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        index = 0
        for item in cart["dish"]:
            quantity = cart["quantity"][index]
            cursor.execute('INSERT INTO orderDetails (customer_id, dish_id, quantity) VALUES (%s, %s, %s)', (str(user.id), str(item), str(quantity)))
            index += 1
            cursor.execute('UPDATE orderDetails SET order_id = %s WHERE order_id = 0', (str(order_id),))
        db.connection.commit()
        cursor.close()

    @staticmethod
    def getMostRecentOrder(db, customer_id):
        '''
        Get most recent order from a database

        returns an order object from the database
        '''
        data = []
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves most recent order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s AND status = 0 ORDER BY order_id DESC', (str(customer_id)))
        recent = cursor.fetchall()
        for order in recent:
            # retrieves most recent orders' details
            cursor.execute('SELECT orderDetails.order_id, dish.dish_id, dish.name, dish.price, orderDetails.quantity FROM dish INNER JOIN orderDetails ON dish.dish_id = orderDetails.dish_id WHERE customer_id = %s AND order_id = %s;', (str(customer_id), str(order["order_id"])))
            details = cursor.fetchall()
            data.append(details)
        cursor.close()

        return recent, data

    @staticmethod
    def getPastOrders(db : MySQL, customer_id):
        '''
        Get all past orders except the most recent from a database

        returns a list of orders object from the database
        '''
        data = []

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves past order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s AND status = 1 ORDER BY order_id DESC', (str(customer_id)))
        past = cursor.fetchall()
        for order in past:
            # retrieves completed orders' details
            cursor.execute('SELECT orderDetails.order_id, dish.dish_id, dish.name, dish.price, orderDetails.quantity FROM dish INNER JOIN orderDetails ON dish.dish_id = orderDetails.dish_id WHERE customer_id = %s AND order_id = %s', (str(customer_id), str(order["order_id"])))
            details = cursor.fetchall()
            data.append(details)
        cursor.close()

        return past, data

    @staticmethod
    def getOrderFromID(db : MySQL, id):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders WHERE order_id = %s', (str(id),))
        order = cursor.fetchone()

        cursor.close()
        return Order(order["order_id"], order["customer_id"], order["num_items"], order["subtotal"], order["tax"], order["discount"], 0.0, order["total"], order["type"], order["status"])

    @staticmethod
    def getBid(db : MySQL, user):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        if user.userType == 'manager':
            cursor.execute('SELECT * FROM deliveryBid INNER JOIN orders ON orders.order_id = deliveryBid.order_id INNER JOIN customer ON orders.customer_id = customer.customer_id INNER JOIN accounts ON orders.customer_id = accounts.id WHERE orders.isFree = 0 AND orders.status = 0 AND deliveryBid.delivery_bid <> 0')
            deliveries = cursor.fetchall()
        else:
            cursor.execute('SELECT * FROM deliveryBid INNER JOIN orders ON orders.order_id = deliveryBid.order_id INNER JOIN customer ON orders.customer_id = customer.customer_id INNER JOIN accounts ON orders.customer_id = accounts.id WHERE orders.isFree = 0 AND orders.status = 0 AND deliveryBid.delivery_id = %s', (str(user.id),))
            deliveries = cursor.fetchall()

        cursor.close()
        return deliveries

    @staticmethod
    def placeBid(db : MySQL, user):
        '''
        Place bid for order in database
        '''
        bidDetails = request.form
        order_bid = bidDetails["order_bid"]
        num_bid = int(bidDetails["num_bid"])+1
        bid = float(bidDetails["bid"])
        old_bid = float(bidDetails["old_bid"])
        delivery_id = bidDetails["delivery_id"]

        if old_bid != 0 and bid > old_bid:
            return False

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE deliveryBid SET num_bids = %s, current_bid = %s, delivery_bid = %s, delivery_id = %s WHERE order_id = %s AND delivery_id = %s', (str(num_bid), str(bid), str(bid), str(delivery_id), str(order_bid), str(user.id)))
        cursor.execute('UPDATE deliveryBid SET num_bids = %s, current_bid = %s WHERE order_id = %s AND delivery_id <> %s', (str(num_bid), str(bid), str(order_bid), str(user.id)))
        db.connection.commit()
        cursor.close()

        return True

    @staticmethod
    def assignBid(db : MySQL):
        '''
        Assign bid to delivery personnel
        '''
        bidDetails = request.form
        delivery_bid = bidDetails["delivery_bid"]
        delivery_id = bidDetails["delivery_id"]
        order_id = bidDetails["order_id"]
        total = float(bidDetails["total"]) + float(bidDetails["delivery_bid"])

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE orders SET total = %s, delivery_fee = %s, delivery_id = %s, status = 1 WHERE order_id = %s', (str(total), str(delivery_bid), str(delivery_id), str(order_id)))
        cursor.execute('DELETE FROM deliveryBid WHERE order_id = %s', (str(order_id)))

        # assigns warning to deliverer if not deliver past 5
        cursor.execute('SELECT * FROM orders WHERE type = %s AND status = 1 ORDER BY order_id DESC', ("delivery",))
        results = cursor.fetchmany(5)
        cursor.execute('SELECT * FROM delivery')
        personnel = cursor.fetchall()
        if len(results) < 5:
            pass
        else:
            num_delivered = 0
            for person in personnel:
                for order in results:
                    if order["delivery_id"] == person["delivery_id"]:
                        num_delivered += 1
                if num_delivered == 0:
                    warnings = int(person["warnings"]) + 1
                    cursor.execute('UPDATE delivery SET warnings = %s WHERE delivery_id = %s', (str(warnings), str(person["delivery_id"])))
            
        db.connection.commit()
        cursor.close()

    @staticmethod
    def getRecentDelivery(db, user):
        '''
        Grabs most recent delivery done by personnel
        '''
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders INNER JOIN customer ON orders.customer_id = customer.customer_id INNER JOIN accounts ON orders.customer_id = accounts.id WHERE orders.delivery_id = %s ORDER BY orders.order_id DESC', (str(user.id)))
        order = cursor.fetchone()
        return order