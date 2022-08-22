class User():
    def __init__(self, **kwargs):
        '''
        Create a new User in session
        
        DO NOT INSTANTIATE 

        Parameters:
        ----------
        id : int
        firstName : str
        lastName : str
        email : str
        uname : str
        password : str
        phoneNumber : str
        userType : str
        '''
        try:
            self.id = kwargs["id"]
        except KeyError:
            self.id = None
            
        try:
            self.firstName = kwargs["firstName"]
        except KeyError:
            self.firstName = None

        try:
            self.lastName = kwargs["lastName"]
        except KeyError:
            self.lastName = None
        
        try:
            self.email = kwargs["email"]
        except KeyError:
            self.email = None

        try:
            self.username = kwargs["username"]
        except KeyError:
            self.username = None
            
        try:
            self.password = kwargs["password"]
        except KeyError:
            self.password = None

        try:
            self.phoneNumber = kwargs["phoneNumber"]
        except KeyError:
            self.phoneNumber = None

        try:
            self.userType = kwargs["type"]
        except KeyError:
            self.userType = None

    def setName(self, firstName = None, lastName = None):
        '''
        Update the user first and last name
        '''
        self.firstName = firstName
        self.lastName = lastName

    def setEmail(self, email = None):
        '''
        Update the user's email
        '''
        self.email = email

    def setUsername(self, username = None):
        '''
        Update the user's username
        '''
        self.username = username

    def setPhoneNumber(self, phoneNumber = None):
        '''
        Update the user's phone number
        '''
        self.phoneNumber = phoneNumber