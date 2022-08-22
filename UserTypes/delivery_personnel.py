from staff import Staff

class DeliveryPersonnel(Staff):
    '''
    Create a delivery personnel in session

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