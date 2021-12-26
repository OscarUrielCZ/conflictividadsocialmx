def get_exception_message(e):
    if hasattr(e, 'message'):
        return e.message
    else:
        return e