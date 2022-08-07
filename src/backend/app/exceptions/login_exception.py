class LoginException(Exception):
    def __str__(self):
        return "Login error wrong user or password."
