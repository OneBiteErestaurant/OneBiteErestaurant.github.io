from user import User

class Staff(User):
    '''
    Create a staff in session

    DO NOT INSTANTIATE 

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
        
        try:
            self.salary = kwargs["salary"]
        except KeyError:
            self.salary = 0.00

        try:
            self.compliments = kwargs["compliments"]
        except KeyError:
            self.compliments = 0

        try:
            self.complaints = kwargs["complaints"]
        except KeyError:
            self.compliments = 0

        try:
            self.warnings = kwargs["warnings"]
        except KeyError:
            self.warnings = 0

        try:
            self.demotions = kwargs["demotions"]
        except KeyError:
            self.demotions = 0