class Recipient:
    def __init__(self, id, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.id == other.id and
                    self.email == other.email and
                    self.first_name == other.first_name and
                    self.last_name == other.last_name)
        return False
