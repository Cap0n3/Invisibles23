from Invisibles23.logging_config import logger


def createFormErrorContext(form) -> dict:
    """
    Create a context to display form errors in the template (used in MembershipView and EventRegistrationView)
    
    Returns
    -------
    dict
        A dictionary containing the form, the error inputs and the error messages
    """
    # Get error data from the form
    error_data = form.errors.as_data()

    # convert error_data to a dict and message to a string
    error_dict = {}
    for key, value in error_data.items():
        error_dict[key] = str(value[0].message)

    # Log error
    logger.error(f"Form is not valid ! Error dict: {error_dict}")

    # Create error_ul from error_dict to display in the template
    errors_list = [
        f"<strong>{key}</strong> : {val}" for (key, val) in error_dict.items()
    ]
    error_ul = "<ul><li>" + "</li><li>".join(errors_list) + "</li></ul>"

    # pass error_ul to the template as html
    error_context = {
        "form": form,
        "error_inputs": error_dict.keys(),
        "error_messages": error_ul,
    }

    return error_context
