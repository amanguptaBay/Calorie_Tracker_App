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
    return Bind_Arbitrary_Property("debug_user_input", debug_user_input)

def Bind_Arbitrary_Property(pName, pValue):
    """
        Adds a proprety to the function that is mock user input, used for testing
    """
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(wrapper, pName, pValue)
        return wrapper
    
    return outer