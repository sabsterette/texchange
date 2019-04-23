# example.py

class User:
    # def __init__(self, user_name, user_id, email, image_file):
    def __init__(self):
        print("testing")
        # self.user_name = user_name
        # self.user_id = user_id
        # self.set_user_id(user_id)
        # self.email = email
        # self.image_file = image_file
        
    @property
    def get_user_id(self):
        return self.user_id
        
    def set_user_id(self, user_id):
        self.user_id = user_id  
   
    @property
    def get_user_name(self):
        return self.user_name

    def set_user_name(self, user_name):
        self.user_name = user_name  
   

    @property
    def get_email(self):
        return self.email
    
    def set_email(self, email):
        self.email = email  
   
    @property
    def get_image_file(self):
        return self.image_file

    def set_image_file(self, image_file):
        self.image_file = image_file  
   