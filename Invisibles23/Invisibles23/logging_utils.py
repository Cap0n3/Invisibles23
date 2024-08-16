from django.conf import settings
from Invisibles23.logging_config import logger
from typing import Any, Optional
import inspect


def log_debug_info(
    message: str, obj: Optional[Any] = None, inspect_attributes: bool = False
) -> None:
    """
    A versatile debug logging function that can handle both simple messages and detailed object inspection.

    Note: This function is only active in DEBUG mode.

    Parameters
    ----------
    message : str
        The message to log.
    obj : Any, optional
        The object to log. Defaults to None.
    inspect_attributes : bool, optional
        A flag to enable detailed inspection of the object's attributes. Defaults to False.

    Usage
    -----
    Simple message:
        `log_debug_info("Simple debug message")`
    outputs:
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event] Simple debug message`
    Object logging:
        `log_debug_info("Event data", data)` # data is an object
    output:
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.clean] Event data`
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.clean] data`
    Detailed object inspection:
        `log_debug_info("Saving object", self, inspect_attributes=True)`
    outputs:
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.save] Saving object`
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.save] self`
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.save] id: 1`
        `[2021-09-20 20:00:00] [DEBUG] {module -> function} - [Event.save] name: "John Doe"`
    """
    # Get information about the caller
    caller_frame = inspect.currentframe().f_back
    caller_class = (
        caller_frame.f_locals.get("self", None).__class__.__name__
        if "self" in caller_frame.f_locals
        else None
    )
    caller_method = caller_frame.f_code.co_name
    caller_info = (
        f"[{caller_class}.{caller_method}]"
        if caller_class
        else f"[function {caller_method}]"
    )

    logger.debug(f"{caller_info} - {message}")

    if obj is not None:
        try:
            # Log will call __str__ method of class if available
            logger.debug(f"{caller_info} - Object details: {obj}")
        except Exception as e:
            logger.error(f"Error while logging object: {e}")

        if inspect_attributes and hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                logger.debug(f"{caller_info} - {key}: {value}")


# Example usage:
# log_debug_info("Simple message")
# log_debug_info("Event data", data)
# log_debug_info("Saving EventParticipants object", self, inspect_attributes=True)
