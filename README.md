# OneBite<img src="./static/assets/onebite_logo.png" align="right" width="25%">


## Electronic Restaurant Order and Delivery System 

Develop an on-line restaurant order and delivery system so that the restaurant can provide menus of food, customers browse and order the food from the menu, delivery people of the restaurant deliver the food

## Specifications

### User Objects

1. Employees
    - [x] At least two chefs who independently decide the menus and make the dish
    - [X] At least two delivery people for food delivery
    - [X] One manager who process customer registrations, handles customer compliments and complaints, hire/fire/raise/cut pay for chef(s) and delivery people

2. Customers
    - [X] Registered customers who can browse/search, order and vote(lowest 1 star to highest 5 stars) delivered (on food and delivery quality/manners individually)
    - [X] Can start/participate a discussion topic on chefs dishes/delivery people
    - [X] Registered customers becomes a VIP after spending more than $100 or 5 orders
    - [X] As a VIP registered customers without complaints, they will receive 5% discount of their ordinary orders and 1 free delivery for every 3 orders, have access to specially developed dishes, and their complaints/compliments are counted twice as important as ordinary ones

3. Visitors
    - [X] Can browse the menus and ratings only
    - [X] Can apply to be the registered customer


## System Features
- [X] Provide a GUI, not necessarily web-based, with pictures to show the descriptions of each
dish and price 
- [X] Each registered customer/VIP has a password to login, when they log in
- [X] Based on the history of their prior choices, different registered customer/VIP will have different top 3 listing dishes. 
- [X] For new customers or visitors, the top 3 most popular dishes and top 3 highest rated dishes are listed on the first page
- [X] A customer can choose to 
    - [X] Pick up the dishes in person 
        - He/She can only complain/compliment the chef
    - [X] By restaurant delivery
- [X] A customer can file complaints/compliments to chef of the food s/he purchased and deliver person who delivered the dish or other customers who didn’t behave in the discussion forums.
- [x] Delivery person can complain/compliment customers s/he delivered dishes, all complaints/compliments are handled by the manager 
- [x] The complained person has the right to dispute the complaint, the manager made the final call to dismiss the
complaint or let the warning stay and inform the impacted parties 
- [X] Customers/delivery people whose complaints are decided to be without merit by the manager will receive one
additional warning.
- [X] Registered customers having 3 warnings are de-registered. 
- [X] VIPs having 2 warnings are put back to registered customers (with warnings cleared). 
- [X] The warnings should be displayed in the page when the customer logs in
- [X] Every customer should deposit some money to the system. If the price of the order is more expensive than the deposited money in the account, the order is rejected and the
customer receives one warning automatically for being reckless
- [X] Customers who are kicked out of the system or choose to quit the system will be handled by the manager: 
    - [X] clear the deposit and close the account. And kicked-out customer is on the blacklist of the restaurant: cannot register any more
- [ ] The chef whose dishes received consistently low ratings (<2) or 3 complaints, will be demoted (less salary), a chef demoted twice is fired. Conversely, a chef whose dishes receive high ratings (>4) or 3 compliments, will receive a bonus. 
- [X] One compliment can be used to cancel one complaint. The delivery people are handled the same way
- [X] The delivery people will compete to deliver the order by bidding, the manager assigns the order from bidding results: the one with lowest delivery price is generally chosen 
- [X] if the one with higher asking price is chosen, the manager should write a memo in the system as justifications. The delivery person who didn’t deliver any in the past 5 orders will automatically receive one warning

## Extra Features
- [X] Web-based application