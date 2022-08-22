-- DROP DATABASE team_m_restaurant;

/* creates database */
CREATE DATABASE IF NOT EXISTS team_m_restaurant DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE team_m_restaurant;

/* Table Accounts */
CREATE TABLE IF NOT EXISTS accounts (
	id int(11) NOT NULL AUTO_INCREMENT,
    fname varchar(50) NOT NULL,
    lname varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    phone varchar(10) NOT NULL,
    type varchar(20) DEFAULT 'customer',
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Accounts */
INSERT INTO accounts VALUES (1, 'Dennis O.', 'Johnson', 'admin', '123abcABC', 'admin@onebite.com', '1234567890', 'manager');
INSERT INTO accounts VALUES (2, 'Melinda F.', 'Thompson', 'chef1', '123abcABC', 'chef1@onebite.com', '1234567891', 'chef');
INSERT INTO accounts VALUES (3, 'Thomas S.', 'Brooks', 'chef2', '123abcABC', 'chef2@onebite.com', '1234567892', 'chef');
INSERT INTO accounts VALUES (4, 'Sandra', 'Pickett', 'delivery1', '123abcABC', 'delivery1@onebite.com', '1234567893', 'delivery');
INSERT INTO accounts VALUES (5, 'Brock', 'Apple', 'delivery2', '123abcABC', 'delivery2@onebite.com', '1234567894', 'delivery');
SELECT * FROM accounts;

/* Table Employee */
CREATE TABLE IF NOT EXISTS employee (
	employee_id int(11) NOT NULL AUTO_INCREMENT,
    fname varchar(50) NOT NULL,
    lname varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    phone varchar(10) NOT NULL,
    type varchar(20),
    PRIMARY KEY (employee_id),
    FOREIGN KEY (employee_id) REFERENCES accounts(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Employee */
INSERT INTO employee(employee_id, fname, lname, username, password, email, phone, type) 
SELECT id, fname, lname, username, password, email, phone, type
FROM accounts WHERE type = 'manager' or type = 'chef' or type = 'delivery';
SELECT * FROM employee;

/* Table Chef */
CREATE TABLE IF NOT EXISTS chef (
	chef_id int(11) NOT NULL AUTO_INCREMENT,
    salary float(11, 2) DEFAULT '5500.00',
	num_compliment int(11) DEFAULT 0,
    num_complaint int(11) DEFAULT 0,
    warnings int(11) DEFAULT 0,
    demotions int(11) DEFAULT 0,
    PRIMARY KEY (chef_id),
    FOREIGN KEY (chef_id) REFERENCES employee(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Chef */
INSERT INTO chef(chef_id) 
SELECT employee_id FROM employee WHERE type = 'chef';
SELECT * FROM chef;

/* Table Delivery */
CREATE TABLE IF NOT EXISTS delivery (
	delivery_id int(11) NOT NULL AUTO_INCREMENT,
    salary float(11, 2) DEFAULT '4000.00',
	num_compliment int(11) DEFAULT 0,
    num_complaint int(11) DEFAULT 0,
    warnings int(11) DEFAULT 0,
    demotions int(11) DEFAULT 0,
    PRIMARY KEY (delivery_id),
    FOREIGN KEY (delivery_id) REFERENCES employee(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Delivery */
INSERT INTO delivery(delivery_id) 
SELECT employee_id FROM employee WHERE type = 'delivery';
SELECT * FROM delivery;

/* Table Customer */
CREATE TABLE IF NOT EXISTS customer (
	customer_id int(11) NOT NULL AUTO_INCREMENT,
    wallet float(7, 2) DEFAULT '0.00',
    cardnumber varchar(16),
    address text,
    num_orders int(11) DEFAULT 0,
    total_spent float(11, 2) DEFAULT '0.00',
    warnings int(11) DEFAULT 0,
    isClosed tinyint(1) DEFAULT 0,
    isBlacklisted tinyint(1) DEFAULT 0,
    isVIP tinyint(1) DEFAULT 0,
    status tinyint(1) DEFAULT 1,
    free_deliveries int(11) DEFAULT 0,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (customer_id) REFERENCES accounts(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Customer */
SELECT * FROM customer;

/* Table Dishes */
CREATE TABLE IF NOT EXISTS dish (
	dish_id int(11) NOT NULL AUTO_INCREMENT,
    dish_type varchar(50) NOT NULL,
    name varchar(100) NOT NULL,
	price float(6, 2) NOT NULL DEFAULT '0.00',
    description text NOT NULL,
	img text NOT NULL,
    chef int(11) NOT NULL,
    rating float NOT NULL DEFAULT 0.00,
    num_ratings int(11) NOT NULL DEFAULT 0,
    count int(11) NOT NULL DEFAULT 0,
    status tinyint(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (dish_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Dishes */
INSERT INTO dish VALUES (1, 'special', 'Oven-Baked Pizza', '15.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1589477500339-82aeb8718167?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 4.2, 211, 0, 1);
INSERT INTO dish VALUES (2, 'special', 'Cheeseburger with Fries', '14.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1600688640154-9619e002df30?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=654&q=800', 2, 3.8, 112, 0, 1);
INSERT INTO dish VALUES (3, 'special', 'Lemon Pepper Spaghetti', '14.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1481931098730-318b6f776db0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=780&q=80', 2, 4.6, 109, 0, 1);
INSERT INTO dish VALUES (4, 'special', 'Pasta Carbonara', '14.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1546549032-9571cd6b27df?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 3.8, 90, 0, 1);
INSERT INTO dish VALUES (5, 'special', 'Donut of the Day', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1618411640018-972400a01458?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 3.1, 101, 0, 1);
INSERT INTO dish VALUES (6, 'special', 'Pie of the Week', '9.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1535920527002-b35e96722eb9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 3.4, 208, 0, 1);
INSERT INTO dish VALUES (7, 'special', 'Caramel Cheesecake', '9.25', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1547414368-ac947d00b91d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 3, 3.5, 89, 0, 1);
INSERT INTO dish VALUES (8, 'special', 'Ferrero Chocolate Milkshake', '7.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1594488506255-a8bbfdeedbaf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 4.2, 81, 0, 1);
INSERT INTO dish VALUES (9, 'appetizer', 'Acai Bowl', '6.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1590301157284-ab2f8707bdc1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 4.6, 78, 0, 1);
INSERT INTO dish VALUES (10, 'appetizer', 'Classic Caesar Salad', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1594834749740-74b3f6764be4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=782&q=80', 2, 2.9, 389, 0, 1);
INSERT INTO dish VALUES (11, 'appetizer', 'Eggs Benedict', '7.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 4.0, 107, 0, 1);
INSERT INTO dish VALUES (12, 'appetizer', 'Pita Chips and Spinach Dip', '4.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1627308595127-d9acf19107ce?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 3.1, 241, 0, 1);
INSERT INTO dish VALUES (13, 'entree', 'Blueberry Pancakes', '9.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1506084868230-bb9d95c24759?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 3.5, 89, 0, 1);
INSERT INTO dish VALUES (14, 'entree', 'French Toast', '10.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=898&q=80', 2, 4.1, 156, 0, 1);
INSERT INTO dish VALUES (15, 'entree', 'Fresh Crepes', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1519676867240-f03562e64548?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 2.7, 120, 0, 1);
INSERT INTO dish VALUES (16, 'entree', 'Croissant Sandwich', '11.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1600761857007-5f51d5dc82a0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 4.5, 46, 0, 1);
INSERT INTO dish VALUES (17, 'entree', 'Pulled Pork Sourdough Toast', '13.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1559054663-e8d23213f55c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 3.8, 50, 0, 1);
INSERT INTO dish VALUES (18, 'entree', 'Smoked Salmon Sourdough Toast', '13.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1627308595216-439c00ade0fe?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 4.2, 105, 0, 1);
INSERT INTO dish VALUES (19, 'dessert', 'Black Cherry Chocolate Tart', '4.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1547043184-599cd7e6acb9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 3.9, 125, 0, 1);
INSERT INTO dish VALUES (20, 'dessert', 'Blackberry Lemon Tart', '4.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1560180474-e8563fd75bab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 2.9, 89, 0, 1);
INSERT INTO dish VALUES (21, 'dessert', 'Blueberry Cheesecake', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1567327613485-fbc7bf196198?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 1.8, 109, 0, 1);
INSERT INTO dish VALUES (22, 'dessert', 'Lemon Meringue Pie', '8.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 4.5, 89, 0, 1);
INSERT INTO dish VALUES (23, 'dessert', 'Peach Pavlova', '7.25', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1624300603538-1207400f4116?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 2.9, 312, 0, 1);
INSERT INTO dish VALUES (24, 'dessert', 'Strawberry Panna Cotta', '5.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 4.1, 108, 0, 1);
INSERT INTO dish VALUES (25, 'drink', 'Coffee', '4.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1540692802289-42509772934e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 4.8, 189, 0, 1);
INSERT INTO dish VALUES (26, 'drink', 'Hot Chocolate', '5.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1548329408-0bcd6e68058d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 3.4, 209, 0, 1);
INSERT INTO dish VALUES (27, 'drink', 'Blackberry Lemonade', '5.75', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1560179304-6fc1d8749b23?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 2.9, 182, 0, 1);
INSERT INTO dish VALUES (28, 'drink', 'Blueberry Limeade', '5.75', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1504310578167-435ac09e69f3?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 3.5, 129, 0, 1);
SELECT * FROM dish;

/* Table Dispute */
CREATE TABLE IF NOT EXISTS dispute (
	first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
	dispute_id int(11) NOT NULL AUTO_INCREMENT,
    complainer_id int(11) NOT NULL,
    disputer_id int(11) NOT NULL,
    dispute_date DATE NOT NULL,
    dispute_content text NOT NULL,
    primary key(dispute_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO dispute VALUES ('chef1', '1', '5,', '4', '2020-10-30', 'trash');
/* Display Dispute */
SELECT * FROM dispute;

/* Table Complaint */
CREATE TABLE IF NOT EXISTS complaint (
	first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    complaint_id int(11) NOT NULL AUTO_INCREMENT,
    complainer_id int(11) NOT NULL,
    receiver_id int(11) NOT NULL,
    complaint_date DATE NOT NULL,
    complaint_content text NOT NULL,
    primary key(complaint_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO complaint VALUES ('apple', 'jeans', '1','5','4','2022-5-17','smelly deliverer');
/* Display Complaint */
SELECT * FROM complaint;

/* Table Compliments */
CREATE TABLE IF NOT EXISTS compliment (
	first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    compliment_id int(11) NOT NULL AUTO_INCREMENT,
    complimenter_id int(11) NOT NULL,
    receiver_id int(11) NOT NULL,
    compliment_date DATE NOT NULL,
    compliment_content text NOT NULL,
    primary key(compliment_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO compliment VALUES('apple', 'bottom', '1', '3', '4', '2022-1-10', 'test compliment for deliverer 4');
INSERT INTO compliment VALUES('apple', 'bottom', '2', '10', '5', '2022-1-10', 'test compliment for deliverer 5');
INSERT INTO compliment VALUES('apple', 'bottom', '3', '10', '2', '2022-1-10', 'test compliment for chef 1');
INSERT INTO compliment VALUES('apple', 'bottom', '4', '10', '2', '2022-1-10', 'test compliment for chef 1');

/* Display Compliments */
SELECT * FROM compliment;

/* Table PastDeliveries */
CREATE TABLE IF NOT EXISTS PastDeliveries (
	first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    order_id int(11) NOT NULL AUTO_INCREMENT,
    customer_id int(11) NOT NULL,
    delivery_date DATE NOT NULL,
    subtotal int(11) NOT NULL,
    primary key(order_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO PastDeliveries VALUES ("Apple", "Bottom", "1400", "1","2020-05-15","500");
INSERT INTO PastDeliveries VALUES ("Olimpiada", "Ayaz", "1401", "2","2020-05-15","15");
INSERT INTO PastDeliveries VALUES ("Sky", "Theudelinda", "1402", "3","2020-05-15","30");
INSERT INTO PastDeliveries VALUES ("Rashnu", "Hortensius", "1403", "4","2020-05-15","50");
INSERT INTO PastDeliveries VALUES ("Cadmus", "Aífe", "1404", "5","2020-05-15","15");
INSERT INTO PastDeliveries VALUES ("Noémia", "Marie-Laure", "1405", "6","2020-05-15","50");
INSERT INTO PastDeliveries VALUES ("Jamilah", "Guntur", "1406", "7","2020-05-15","5");
INSERT INTO PastDeliveries VALUES ("Jānis", "Athanasia", "1407", "8","2020-05-15","12");
INSERT INTO PastDeliveries VALUES ("Azamat", "Linn", "1408", "9","2020-05-15","244");
INSERT INTO PastDeliveries VALUES ("Adrasteia", "Madhavi", "1409", "10","2020-05-15","44");
INSERT INTO PastDeliveries VALUES ("Lula", "Seung", "1410", "11","2020-05-15","23");
INSERT INTO PastDeliveries VALUES ("Hayat", "Puja", "1411", "12","2020-05-15","50");
INSERT INTO PastDeliveries VALUES ("Lykos", "Genovefa", "1412", "13","2020-05-15","10");
INSERT INTO PastDeliveries VALUES ("Seong-Jin", "Zulfaqar", "1413", "14","2020-05-15","7");
INSERT INTO PastDeliveries VALUES ("Dianne", "Antoinette", "1414", "15","2020-05-15","0");
INSERT INTO PastDeliveries VALUES ("Pratima", "Luka", "1415", "16","2020-05-15","90");
INSERT INTO PastDeliveries VALUES ("Máel Sechlainn", "Azad", "1416", "17","2020-05-15","30");

/* Display Past Deliveries */
SELECT * FROM PastDeliveries;

/* Table Orders */
CREATE TABLE IF NOT EXISTS orders (
	order_id int(11) NOT NULL AUTO_INCREMENT,
    customer_id int(11) NOT NULL,
    num_items int(11) NOT NULL,
    subtotal float NOT NULL,
    tax float NOT NULL,
    discount float NOT NULL,
    delivery_fee float NOT NULL DEFAULT 0.0,
    total float NOT NULL,
    datetime varchar(50) NOT NULL,
    type varchar(50) NOT NULL,
    status tinyint(1) NOT NULL DEFAULT 0,
    isFree tinyint(1) NOT NULL DEFAULT 0,
    delivery_id int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (order_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Orders */
SELECT * FROM orders;

/* Table OrderDetails */
CREATE TABLE IF NOT EXISTS orderDetails (
	order_id int(11) NOT NULL DEFAULT 0,
    customer_id int(11) NOT NULL,
    dish_id int(11) NOT NULL,
    quantity int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display OrderDetails */
SELECT * FROM orderDetails;

/* Table DeliveryBid */
CREATE TABLE IF NOT EXISTS deliveryBid (
	order_id int(11) NOT NULL,
    customer_id int(11) NOT NULL,
    num_bids int(11) NOT NULL DEFAULT 0,
    current_bid float NOT NULL DEFAULT 0.0,
    delivery_bid float NOT NULL DEFAULT 0.0,
    delivery_id int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display DeliveryBid */
SELECT * FROM deliveryBid;

/* Table Posts */
CREATE TABLE IF NOT EXISTS post (
	post_id int(11) NOT NULL AUTO_INCREMENT,
	post_author varchar(255) NOT NULL,
	post_content TEXT NOT NULL,
	post_date DATE NOT NULL,
	post_title varchar(50) NOT NULL,
	user_id int(11) NOT NULL,
	PRIMARY KEY (post_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO post VALUES (1, "Manager", "Please be respectful to all users. Enjoy!", "2020-05-15","Welcome to OneBite!", 1);
INSERT INTO post VALUES (2, "Manager", "Tell us how you feel about our Appetizers!", "2020-05-16","Your Fav Appetizers?", 1);
INSERT INTO post VALUES (3, "Manager", "Tell us how you feel about our Entrees!", "2020-05-16","Your Fav Entrees?", 1);
INSERT INTO post VALUES (4, "Manager", "Tell us how you feel about our Drinks!", "2020-05-16","Your Fav Drinks?", 1);

/* Display Posts */
INSERT INTO post(user_id) 
SELECT customer_id FROM customer;
SELECT * FROM post;

/* Table Post Comments */
CREATE TABLE IF NOT EXISTS postcomments (
	postcomment_id int(11) NOT NULL AUTO_INCREMENT,
	postcomment_author varchar(255) NOT NULL,
	postcomment_content TEXT NOT NULL,
	postcomment_date DATE NOT NULL,
	user_id int(11) NOT NULL,
	PRIMARY KEY (postcomment_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- INSERT INTO postcomments VALUES (1, "User1", "first", "2020-05-16");
-- INSERT INTO postcomments VALUES (2, "User2", "second", "2020-05-16");

/* Display Post Comments */
INSERT INTO postcomments(user_id) 
SELECT customer_id FROM customer;
SELECT * FROM postcomments;

/* Table Forum Warnings */
CREATE TABLE IF NOT EXISTS forumwarnings (
	forumwarning_id int(11) NOT NULL AUTO_INCREMENT,
	forumwarning_author varchar(255) NOT NULL,
	forumwarning_accused varchar(255) NOT NULL,
	forumwarning_content TEXT NOT NULL,
	forumwarning_date DATE NOT NULL,
	user_id int(11) NOT NULL,
	reported_id int(11) NOT NULL,
	PRIMARY KEY (forumwarning_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Forum Warnings */
INSERT INTO forumwarnings(user_id) 
SELECT customer_id FROM customer;
INSERT INTO forumwarnings(reported_id)
SELECT user_id FROM postcomments WHERE forumwarning_accused = postcomment_author;
SELECT * FROM forumwarnings;
