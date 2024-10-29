class GenericException(Exception):
    
    status_code = 0
    message = None
    desc = None
    
    def __init__(self, status_code, message, desc):
        self.status_code = status_code
        self.message = message
        self.desc = desc
        super().__init__(self.status_code, self.message, self.desc)