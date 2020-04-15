import base64

class Auth:
    def __init__(self, password=None):
        self.password = password
        if password is not None:
            self.password_b64 = base64.b64encode(password.encode()).decode('utf8')
        else:
            self.password_b64=None
        self.require_login = password is not None

    def try_login(self, password):
        return password == self.password_b64

