from UserTypes.customer import Customer
from staff import Staff

class Manager(Staff):
    '''
    Create a manager in session

    Parameters
    ----------
    id : int
    firstName : str
    lastName : str
    email : str
    uname : str
    password : str
    phoneNumber : str
    userType : str
    
    salary : float
    compliments : int
    complaints : int
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def setStaffSalary(self, staff : Staff, amount):
    #     staff._salary = amount

    def setChefSalary(self, chef, amount):
        chef._salary = amount

    def setDeliveryPersonelSalary(self, dp, amount):
        dp._salary = amount
    
    def issueWarning(self, customer : Customer):
        customer.warnings += 1
        # connect to DB

    def blackListUser(self, customer : Customer):
        pass

