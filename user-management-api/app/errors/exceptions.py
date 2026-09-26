class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class ConflictError(AppError):
    def __init__(self, message="Resource already exists"):
        super().__init__(message, 409)


class ValidationError(AppError):
    def __init__(self, message="Validation failed"):
        super().__init__(message, 400)