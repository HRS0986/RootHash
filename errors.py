# RootHash Errors

class PasswordNotMatchError(Exception):
    def __init__(self, error):
        super(PasswordNotMatchError, self).__init__(error)
        self.error_code = 20

class WrongPasswordError(Exception):
    def __init__(self, error):
        super(WrongPasswordError).__init__(error)
        self.error_code = 21

class WeekPasswordError(Exception):
    def __init__(self, error):
        super(WeekPasswordError, self).__init__(error)
        self.error_code = 22

class InvalidCommandError(Exception):
    def __init__(self, error):
        super(InvalidCommandError, self).__init__(error)
        self.error_code = 23

class RecordNotFoundError(Exception):
    def __init__(self, error):
        super(RecordNotFoundError, self).__init__(error)
        self.error_code = 24

class NotAlphaError(Exception):
    def __init__(self, error):
        super(NotAlphaError, self).__init__(error)
        self.error_code = 25

