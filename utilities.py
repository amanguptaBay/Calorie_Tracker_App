import functools
def tabbedString(stringIn, n):
    if stringIn is None:
        stringIn = ""
    lines = stringIn.split("\n")
    tabbedLines = []
    for line in lines:
        tabbedLine = "\t" * n + line
        tabbedLines.append(tabbedLine)
    return "\n".join(tabbedLines)

def Debug_User_Input(debug_user_input):
    """
        Adds a proprety to the function that is mock user input, used for testing
    """
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.debug_user_input = debug_user_input
        return wrapper
    
    return outer