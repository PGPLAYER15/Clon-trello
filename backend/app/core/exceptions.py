"""
Excepciones personalizadas para la aplicación.
Cada capa maneja sus propias excepciones:
- Repository: DatabaseError (errores de SQLAlchemy)
- Service: BusinessLogicError (errores de lógica de negocio)
- API/Router: HTTPException (errores HTTP)
"""


class AppException(Exception):
    """Excepción base de la aplicación"""
    def __init__(self, message: str = "Error en la aplicación"):
        self.message = message
        super().__init__(self.message)


class DatabaseError(AppException):
    """Excepción para errores de base de datos (Repository layer)"""
    def __init__(self, message: str = "Error en la base de datos", original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message)


class NotFoundError(AppException):
    """Excepción cuando un recurso no se encuentra"""
    def __init__(self, resource: str = "Recurso", resource_id: int = None):
        message = f"{resource} no encontrado" if not resource_id else f"{resource} con id {resource_id} no encontrado"
        super().__init__(message)


class ValidationError(AppException):
    """Excepción para errores de validación de datos"""
    def __init__(self, message: str = "Error de validación"):
        super().__init__(message)


class BusinessLogicError(AppException):
    """Excepción para errores de lógica de negocio (Service layer)"""
    def __init__(self, message: str = "Error de lógica de negocio"):
        super().__init__(message)
