from flask import Flask, render_template, request, redirect, session, url_for, Markup
from re import A
from datetime import datetime
from database import *
from dish import Dish
from order import Order

app = Flask(__name__)
 
mysql = None

# store each user id that correspond with a user object
usersInSession = {}

def isUserStillInSession():
    '''
    Verify if the user exist in session

    if the user exist, return the user object
    '''
    if "user" in session: # If the user has previous logged in
        user = usersInSession.get(session["user"]) # check the program's memory for the user
        
        if not user: # cannot find user from the program (most likely the website restart and the user had not close their browsers)
            user = getUserInDatabaseByID(mysql, session["user"])
            
            if not user:
                return (False, None)       

        return (True, user)
    
    return (False, None)

@app.route("/",  methods = ['GET', 'POST'])
def homePage():
    '''
    Route to the home page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            if user.warnings > 0:
                flash(Markup("You have {0} warning(s), please check your <a href='/dashboard' class='alert-link' style='background-color: transparent;'>dashboard</a>".format(user.warnings)), category = "error")
            return render_template("home_page.html", user=user, favDishes=user.getFavoriteDishes(mysql), popularDishes=Dish.getPopularDishes(mysql), ratedDishes=Dish.getHighestRatedDishes(mysql))
        else:
            return redirect(url_for("dashboard"))

    return render_template("home_page.html", user=None, popularDishes=Dish.getPopularDishes(mysql), ratedDishes=Dish.getHighestRatedDishes(mysql))

@app.route("/about/")
def aboutPage():
    '''
    Route to the about page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("about.html", user=user)
        else:
            return redirect(url_for("homePage"))
    
    return render_template("about.html", user=None)
    
@app.route("/menu/")
def menu():
    '''
    Route to the menu page
    '''
    # Get all the dishes from the db
    APPETIZERS = Dish.getAppetizers(mysql)
    ENTREES = Dish.getEntrees(mysql)
    DESERTS = Dish.getDeserts(mysql)
    DRINKS = Dish.getDrinks(mysql)
    SPECIALS = Dish.getSpecials(mysql)
    
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("menu.html", 
                user=user,
                appetizers=APPETIZERS,
                entrees=ENTREES,
                deserts=DESERTS,
                drinks=DRINKS,
                specials=SPECIALS)
        else:
            return redirect(url_for("homePage"))

    return render_template("menu.html", 
        user=None, 
        appetizers=APPETIZERS,
        entrees=ENTREES,
        deserts=DESERTS,
        drinks=DRINKS)

@app.route("/login/", methods = ['GET', 'POST'])
def loginPage():
    '''
    Route to the user login page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("You are already logged in.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        user = getUserInDatabaseByLogin(mysql)
        if user != None: # Success
            session["user"] = user.id
            session["cart"] = { "dish" : [], "quantity" : [] }

            usersInSession[user.id] = user
            # if user is a customer
            if user.userType == 'customer':
                # user becomes downgraded after receiving 2 warnings as a VIP member and has warnings reset
                if user.isVIP == 1 and user.warnings >= 2:
                    user.setisVIP(mysql, 0)
                    user.setWarnings(mysql, 0)
                    user.setFreeDeliveries(mysql, 0)
                    user.setNumOrders(mysql, 0)

                # user becomes Blacklisted after receiving 3 warnings
                if user.isVIP == 0 and user.warnings >= 3:
                    user.setisBlacklisted(mysql, 1)
                    session.pop("user", None)
                    session.pop("cart", None)
                    flash("Your account has been blacklisted for receiving 3 or more warnings.", category = 'error')
                    return redirect(url_for("loginPage"))
                if user.address == None and user.wallet == 0:
                    flash("IMPORTANT: Set delivery address and add funds to your account in your profile page before making your first order.", category = "warning")
                elif user.wallet == 0:
                    flash("IMPORTANT: Add funds to your account in your profile page before making your first order.", category = "warning")
                elif user.address == None:
                    flash("IMPORTANT: Set delivery address in your profile page before making your first delivery order.", category = "warning")
                if user.warnings > 0:
                    flash("You have {0} warning(s), please check our dashboard".format(user.warnings), category = "error")
                return redirect(url_for("homePage"))
            # if user is an employee
            else:
                return redirect(url_for("dashboard"))

        else:
            return render_template('login_page.html')

    return render_template("login_page.html")

@app.route("/logout/")
def logout():
    '''
    Log out a user from the session
    '''
    session.pop("user", None)
    session.pop("cart", None)
    flash("You have successfully signed out.", category="success")
    return redirect(url_for("loginPage"))

@app.route("/forgot-password/", methods = ['GET', 'POST'])
def forgotpassPage():
    '''
    Route to the forgot password page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("Please logout first.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if forgotPassword(mysql):
            return redirect('/')

    return render_template('forgot_pass.html')

@app.route("/newuser/", methods = ['GET', 'POST'])
def newuserPage():
    '''
    Route to the new user page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("Please logout first.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if verifyNewUser(mysql):
            return redirect('/login/')

    return render_template('new_user.html')

@app.route("/faqs/")
def faqs():
    '''
    Route to the FAQs page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("faqs.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("faqs.html", user=None)

@app.errorhandler(404)
def pageNotFound(e):
    '''
    Route to this page is the page DNE
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("404.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("404.html", user=None)

@app.route("/tos/")
def tos():
    '''
    Route to the terms of service page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("tos.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("tos.html", user=None)

@app.route("/privacy/")
def privacyPolicy():
    '''
    Route to the privacy policy page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("privacy.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("privacy.html", user=None)

@app.route("/customer-support/")
def customerSupport():
    '''
    Route to the customer support page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("customer-support.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("customer-support.html", user=None)

@app.route("/careers/")
def careers():
    '''
    Route to the careers page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("careers.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("careers.html", user=None)

@app.route("/cart/", methods = ['GET', 'POST'])
def cartPage():
    '''
    Route to the cart page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in #
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))
    
    cart = session.get("cart")

    if cart == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    items = getCartItems(mysql, cart)
    cartInfo = getCartInfo(items, user.isVIP)

    if request.method == 'POST':
        if "cart-submit" in request.form:
            if cartInfo["subtotal"] == 0:
                flash("Error: Your cart is empty.", category = "error")
            else:
                return redirect(url_for("checkoutPage"))
        else:
            dish_id = request.form["dish-id"]
            index = cart["dish"].index(dish_id)
            if "minus" in request.form:
                cart = updateQuantity(cart, index, "minus")
                session["cart"] = cart
                if cart["quantity"][index] == 0:
                    removeDishFromCart(dish_id)
                return redirect(url_for("cartPage"))
            if "plus" in request.form:
                cart = updateQuantity(cart, index, "plus")
                session["cart"] = cart
                return redirect(url_for("cartPage"))

    return render_template("cart_page.html", user=user, cart=items, cartInfo=cartInfo)


@app.route("/add-dish-to-cart/<id>", methods = ['POST'])
def addDishToCart(id):
    '''
    Add a dish to the user cart
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if request.method == "POST":
        if not userExist:
            flash("Please Log In", category="error")
            return redirect(url_for("loginPage"))
        elif userExist and user.userType != 'customer':
            return redirect(url_for("homePage"))

        else:
            # Get cart
            cart = session.get("cart")

            # the list cannot be found, most likely their session timed out
            if cart == None:
                flash("Session timed out, please try again", category="error")
                return redirect(url_for("loginPage"))

            if id in cart["dish"]:
                # if item already exists, increase quantity
                index = 0
                for item in cart["dish"]:
                    if item == id:
                        cart["quantity"][index] += 1
                    index += 1
            else:
                # append the new dish
                cart["dish"].append(id)
                cart["quantity"].append(1)
            session["cart"] = cart
    return redirect(url_for("cartPage"))

@app.route("/remove-dish-from-cart/<id>", methods = ['POST'])
def removeDishFromCart(id):
    '''
    Remove a dish from the cart
    '''
    userExist, user = isUserStillInSession()

    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        cart = session.get("cart")

        if cart == None:
            flash("Session timed out, please try again", category="error")
            return redirect(url_for("loginPage"))

        index = cart["dish"].index(id)
        del cart["dish"][index]
        del cart["quantity"][index]
        session["cart"] = cart
        
    return redirect(url_for("cartPage"))

@app.route("/clear-cart/", methods = ['POST'])
def clearCart():
    '''
    Empties the cart
    '''
    userExist, user = isUserStillInSession()

    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        cart = session.get("cart")

        if cart == None:
            flash("Session timed out, please try again", category="error")
            return redirect(url_for("loginPage"))

        cart["dish"].clear()
        cart["quantity"].clear()
        session["cart"] = cart
        
    return redirect(url_for("cartPage"))
    
@app.route("/checkout/", methods = ['GET', 'POST'])
def checkoutPage():
    '''
    Route to the checkout page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    cart = session.get("cart")

    if cart == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    items = getCartItems(mysql, cart)
    cartInfo = getCartInfo(items, user.isVIP)

    if request.method == 'POST':
        if "checkout-submit" in request.form:
            order_type = request.form["check-type"]
            if order_type == 'delivery' and user.address == None:
                flash("Error: Cannot deliver to an unknown place. Please add a delivery address.", category = "error")
            else:
                return redirect(url_for("orderPlacedPage", order_type = order_type))

    return render_template("checkout_page.html", user=user, cart=items, cartInfo=cartInfo)

@app.route("/order-placed/", methods = ['GET', 'POST'])
def orderPlacedPage():
    '''
    Route to order confirmation/order failure
    '''

    if request.method == 'POST':
        if "disputesubmit" in request.form:
            retrieveDispute(mysql)
        if "complaintsubmit" in request.form:
            retrieveComplaint(mysql)
        if "complimentsubmit" in request.form:
            retrieveCompliment(mysql)
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    # grabbing cart session and cart info
    cart = session.get("cart")

    if cart == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    items = getCartItems(mysql, cart)
    cartInfo = getCartInfo(items, user.isVIP)

    total = float(cartInfo["total"])
    order_type = request.args.get("order_type")

    # order unsuccessful
    if user.wallet < total:
        prev_isVIP = 0
        user.setWarnings(mysql, user.warnings+1)

        # user becomes downgraded after receiving 2 warnings as a VIP member and has warnings reset
        if user.isVIP == 1 and user.warnings >= 2:
            prev_isVIP = 1
            user.setisVIP(mysql, 0)
            user.setWarnings(mysql, 0)
            user.setFreeDeliveries(mysql, 0)
            user.setNumOrders(mysql, 0)

        # user becomes Blacklisted after receiving 3 warnings
        if user.isVIP == 0 and user.warnings >= 3:
            user.setisBlacklisted(mysql, 1)
            session.pop("user", None)
            session.pop("cart", None)
            flash("Your account has been blacklisted for receiving 3 or more warnings.", category = 'error')
            return redirect(url_for("loginPage"))

        return render_template("order_placed.html", user=user, success=False, order_type=order_type, total=total, prevVIP = prev_isVIP)

    # order successful
    else:
        # update dish information
        for dish in cart["dish"]:
            index = cart["dish"].index(dish)
            old_count = getDishCount(mysql, dish)
            setDishCount(mysql, dish, cart["quantity"][index]+old_count)

        # update user information
        user.setWallet(mysql, user.wallet-total)
        user.setNumOrders(mysql, user.num_orders+1)
        user.setTotalSpent(mysql, user.total_spent+total)

        # if user is VIP, receive free delivery for every 3 orders
        if user.isVIP == 1 and user.num_orders%3 == 0:
            user.setFreeDeliveries(mysql, user.free_deliveries+1)

        isFree = 0
        # if user is VIP and has free deliveries, fee = 0 and decrease number of free deliveries remaining
        if user.isVIP == 1 and order_type == 'delivery' and user.free_deliveries > 0:
            user.setFreeDeliveries(mysql, user.free_deliveries-1)
            isFree = 1

        # user becomes VIP after 5 orders Or after spending $100 
        if user.isVIP == 0 and (user.num_orders > 5 or user.total_spent > 100) and user.warnings == 0:
            user.setisVIP(mysql, 1)
            user.setNumOrders(mysql, 0)

        # insert order details into database
        now = datetime.now()
        # mm/dd/YY H:M:S
        dt = now.strftime("%m/%d/%Y %H:%M:%S")
        orders = Order.insertIntoOrders(mysql, user, cartInfo, order_type, dt, isFree)
        Order.insertIntoDetails(mysql, user, orders, cart)

        # clear the cart
        session["cart"] = { "dish" : [], "quantity" : []}

        return render_template("order_placed.html", user=user, success=True, order_type=order_type, total=total)


@app.route("/profile/", methods = ['GET', 'POST'])
def profilePage():
    '''
    Route to profile page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if "pass-submit" in request.form:
            if forgotPassword(mysql):
                return redirect('/profile/')
        if "address-submit" in request.form:
            if changeAddress(mysql, user):
                return redirect('/profile/')
        if "card-submit" in request.form:
            if changeCard(mysql, user):
                return redirect('/profile/')
        if "wallet-submit" in request.form:
            if chargeFunds(mysql, user):
                return redirect('/profile/')
        if "delete-submit" in request.form:
            if deleteAcc(mysql, user):
                flash('Successful! Your deposit will be cleared and the account will be deleted.', category = 'success')
                return redirect('/logout/')
    return render_template("profile_page.html", user=user)

@app.route("/orders/", methods = ['GET', 'POST'])
def orders():
    '''
    Route to the orders page
    '''
    userExist, user = isUserStillInSession()
    if not userExist:
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    RECENTORDERS, RECENTDETAILS = Order.getMostRecentOrder(mysql, user.id)
    PASTORDERS, PASTDETAILS = Order.getPastOrders(mysql, user.id)

    if request.method == 'POST':
        if "compliment-dish" in request.form:
            # fetch form data
            userDetails = request.form
            order_id = userDetails['order_id']
            dish_id = userDetails['dish_id']
            dish_name = userDetails['dish_name']
            return redirect(url_for("commentForm", comment_type = "compliment-chef", order_id = order_id, dish_id = dish_id, dish_name = dish_name))
        if "complaint-dish" in request.form:
            # fetch form data
            userDetails = request.form
            order_id = userDetails['order_id']
            dish_id = userDetails['dish_id']
            dish_name = userDetails['dish_name']
            return redirect(url_for("commentForm", comment_type = "complaint-chef", order_id = order_id, dish_id = dish_id, dish_name = dish_name))
        if "compliment-delivery" in request.form:
            # fetch form data
            userDetails = request.form
            order_id = userDetails['order_id']
            return redirect(url_for("commentForm", comment_type = "compliment-delivery", order_id = order_id))
        if "complaint-delivery" in request.form:
            # fetch form data
            userDetails = request.form
            order_id = userDetails['order_id']
            return redirect(url_for("commentForm", comment_type = "complaint-delivery", order_id = order_id))

    return render_template("orders.html", user=user, recentOrders = RECENTORDERS, recentDetails = RECENTDETAILS, pastOrders = PASTORDERS, pastDetails = PASTDETAILS)

@app.route("/comment-form/", methods = ['GET', 'POST'])
def commentForm():
    '''
    Route to compliment/complaint form
    '''
    userExist, user = isUserStillInSession()
    if not userExist:
        return redirect(url_for("loginPage"))
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d")
        user.makeComment(mysql, dt)
        flash('Successfully submitted.', category = 'success')
        return redirect(url_for('orders'))

    comment_type = request.args.get("comment_type")
    order_id = request.args.get("order_id")
    if comment_type == "compliment-chef" or comment_type == "complaint-chef":
        dish_id = request.args.get("dish_id")
        dish_name = request.args.get("dish_name")
        return render_template("comment_form.html", user=user, comment_type = comment_type, order_id = order_id, dish_id = dish_id, dish_name = dish_name)
    else:
        return render_template("comment_form.html", user=user, comment_type = comment_type, order_id = order_id)

@app.route("/dashboard/",  methods = ['GET', 'POST'])
def dashboard():
    '''
    Route to the dashboard page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        if "disputesubmit" in request.form:
            retrieveDispute(mysql)
        if "complaintsubmit" in request.form:
            retrieveComplaint(mysql)
        if "complimentsubmit" in request.form:
            retrieveCompliment(mysql)
        if "editsubmit" in request.form:
            print("test\n\n")
            edititem(mysql)
        if "removeitem" in request.form:
            removeitem(mysql)
        if "addsubmit" in request.form:
            additem(mysql)
        if "postsubmit" in request.form:
            retrievePost(mysql)
        if "postcommentsubmit" in request.form:
            retrievePostComment(mysql)
        if "givewarning" in request.form:
            addwarning(mysql)
        if "giveforumwarning" in request.form:
            addforumwarning(mysql)
        if "removecomment" in request.form:
            removeComment(mysql)
        if "warningsubmit" in request.form:
            retrieveForumWarnings(mysql)
            
    if user.userType == "manager":
        if request.method == 'POST':
            if "assign-submit" in request.form:
                Order.assignBid(mysql)
            if "cleardeposit" in request.form:
                clearDeposit(mysql)
            if "deleteaccount" in request.form:
                deleteAccount(mysql)
            if "givewarning" in request.form:
                addwarning(mysql)
        rows=loadDisputes(mysql)
        posts=loadPost(mysql)
        postcomments=loadPostComments(mysql)
        compliments=loadCompliments(mysql,user)
        complaints=loadComplaints(mysql,user)
        forumwarnings=loadForumWarnings(mysql)
        # print(rows)
        DELIVERYBIDS = Order.getBid(mysql, user)
        CHEFS, DELIVERYS, CUSTOMERS = retrieveUsers(mysql)
        PREVIOUSCUSTOMERS = retrievePrevious(mysql)
        return render_template("dashboard.html", user=user, userType=user.userType, rows=rows,chefs=CHEFS, deliverys=DELIVERYS, customers=CUSTOMERS, posts=posts, postcomments=postcomments, deliverybids = DELIVERYBIDS, forumwarnings=forumwarnings, previousCustomers = PREVIOUSCUSTOMERS, compliments=compliments, complaints= complaints)

    if user.userType == "delivery":
        if request.method == 'POST':
            if "bid-submit" in request.form:
                if Order.placeBid(mysql, user):
                    flash('Bid placement successful.', category = "success")
                else:
                    flash('Bid placement failed. You must bid a lower asking delivery price.', category = "error")
        rows=loadPastDeliveries(mysql)
        compliments=loadCompliments(mysql,user)
        complaints=loadComplaints(mysql,user)
        warnings=loadWarnings(mysql,user)
        DELIVERYBIDS = Order.getBid(mysql, user)
        RECENTDELIVERY = Order.getRecentDelivery(mysql, user)
        return render_template("dashboard.html", user=user, userType=user.userType, rows=rows,compliments=compliments, complaints=complaints,warnings=warnings, deliverybids = DELIVERYBIDS, recentDelivery = RECENTDELIVERY)
        
    if user.userType == "chef":
        entree=loadEntrees(mysql,user)
        appetizers=loadAppt(mysql,user)
        desserts=loadDesserts(mysql,user)
        drinks=loadDrinks(mysql,user)
        menu=loadMenu(mysql,user)
        special=loadSpecials(mysql,user)
        compliments=loadCompliments(mysql,user)
        complaints=loadComplaints(mysql,user)
        warnings=loadWarnings(mysql,user)
        return render_template("dashboard.html", user=user, userType=user.userType,entree=entree, appetizers=appetizers,desserts=desserts,drinks=drinks,menu=menu,special=special, compliments=compliments, complaints=complaints, warnings=warnings)
    
    if user.userType == "customer":
        posts=loadPost(mysql)
        postcomments=loadPostComments(mysql)
        return render_template("dashboard.html", user=user, userType=user.userType, posts=posts, postcomments=postcomments)
    return render_template("dashboard.html", user=user, userType=user.userType)

@app.route("/index")
def index():
    '''
    Route to profile page
    '''
    userExist, user = isUserStillInSession()

    return render_template("index.html", user=user)

@app.route("/thread")
def thread():
    '''
    Route to profile page
    '''
    userExist, user = isUserStillInSession()

    return render_template("thread.html", user=user)

# Run the app
if __name__ == "__main__":
    mysql = databaseInit(app) # Setup the database
    app.run(debug=True)