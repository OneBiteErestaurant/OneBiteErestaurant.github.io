import MySQLdb.cursors
from flask_mysqldb import MySQL

class Dish():
    def __init__(self, id: int, type : str, name : str, price : float, desc : str, img : str, chef : int, rating : float, num_ratings : int, count : int, status : int):
        '''
        Create a dish object that stores its components

        Parameters
        ----------
        id      : int
        type    : str
        name    : str
        price   : float
        desc    : str
        img     : str (url)
        chef    : int
        rating  : float
        num_ratings : int
        count   : int
        status  : boolean
        '''
        self.name = name
        self.desc = desc
        self.img = img
        self.price = price
        self.id = id
        self.type = type
        self.chef = chef
        self.rating = round(rating)
        self.num_ratings = num_ratings
        self.count = count
        self.status = status

    def __str__(self):
        return f'Dish Name: {self.name}\n\nDish Desc: {self.desc}\n\nDish Image: {self.img}\n\nDish Price: {str(self.price)}\n'

    @staticmethod
    def getAppetizers(db : MySQL):
        '''
        Get all appetizers from a database

        returns a list of dish object from the database
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "appetizer"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data           

    @staticmethod
    def getEntrees(db : MySQL):
        '''
        Get all entrees from a database

        returns a list of dish object from the database
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "entree"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data 

    @staticmethod
    def getDeserts(db : MySQL):
        '''
        Get all deserts from a database

        returns a list of dish object from the database
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "dessert"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data

    @staticmethod
    def getDrinks(db: MySQL):
        '''
        Get all drinks from a database

        returns a list of dish object from the database
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "drink"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data

    @staticmethod
    def getSpecials(db: MySQL):
        '''
        Get all specials from a database

        returns a list of dish object from the database
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "special"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data

    @staticmethod
    def getPopularDishes(db: MySQL):
        '''
        Get top 3 most popular dishes from a database

        returns a list of dish objects from the database
        '''
        data = []  # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish ORDER BY count DESC')
        popular = cursor.fetchmany(3)

        for dish in popular:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data

    @staticmethod
    def getHighestRatedDishes(db: MySQL):
        '''
        Get top 3 highest rated from a database

        returns a list of dish object from the database
        '''
        data = []  # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish ORDER BY rating DESC')
        popular = cursor.fetchmany(3)

        for dish in popular:
            data.append(Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"]))

        cursor.close()
        return data

    @staticmethod
    def getDishFromID(db : MySQL, id):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_id = %s', (str(id),))
        dish = cursor.fetchone()

        cursor.close()
        return Dish(dish["dish_id"], dish["dish_type"], dish["name"], dish["price"], dish["description"], dish["img"], dish["chef"], dish["rating"], dish["num_ratings"], dish["count"], dish["status"])