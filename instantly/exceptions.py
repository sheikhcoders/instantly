"""
Custom exceptions for the instantly package
"""

class InstantlyError(Exception):
    """Base exception class for Instantly errors."""
    pass

class ConfigurationError(InstantlyError):
    """Raised when there are configuration issues."""
    pass

class APIError(InstantlyError):
    """Raised when there are API communication errors."""
    pass

class ValidationError(InstantlyError):
    """Raised when input validation fails."""
    pass