# example.py

class User:
    def __init__(self, id, user_name, email, image_file):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.image_file = image_file
        
    @property
    def id(self):
        return self.id
    
    @property
    def user_name(self):
        return self.user_name

    @property
    def email(self):
        return self.email
    
    @property
    def image_file(self):
        return self.image_file