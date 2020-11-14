class User:

    def __init__(self, id, first_name, last_name, email, password, bio):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.activated = 1
        self.bio = bio
