class AppException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExists(AppException):
    pass


class UserNotFound(AppException):
    pass


class RoomNotFound(AppException):
    pass


class QuestionsNotFound(AppException):
    pass
