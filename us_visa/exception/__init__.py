import os
import sys

"""
from: 
*_ https://docs.python.org/3/tutorial/errors.html
"""
def error_message_detail(error, error_detail: sys):
    """
    Constructs a detailed error message including the script name, line number,
    and the error message that occurred.

    Args:
        error (Exception): The error object that was raised.
        error_detail (sys): The sys module, used to access detailed traceback information.

    Returns:
        str: A formatted error message containing the script name, line number, and error description.
    """
    # Extract traceback information to identify where the error occurred
    _, _, exc_tb = error_detail.exc_info()

    # Get the filename where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Construct the error message with script name, line number, and error details
    error_message = "Error occurred in python script: [{0}] at line number [{1}] with error message: [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class USvisaException(Exception):
    """
    Custom Exception class for handling errors in the US visa application processing script.

    Attributes:
        error_message (str): The detailed error message including script name and line number.
    """

    def __init__(self, error_message, error_detail: sys):
        """
        Initializes the USvisaException with a detailed error message.

        Args:
            error_message (Exception): The original error message that was raised.
            error_detail (sys): The sys module to access detailed traceback information.
        """
        # Call the base class constructor to initialize the exception with the error message
        super().__init__(error_message)

        # Create a detailed error message using the helper function
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        """
        Returns the string representation of the exception, which is the detailed error message.

        Returns:
            str: The detailed error message.
        """
        return self.error_message
