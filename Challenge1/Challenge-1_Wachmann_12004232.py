################################################################################
# Python challenge 1
# Your task is to find out whether a certain input is a boolean, a string or a number below/above 12.
#
# Name: Wachmann Elias
# Matriculation number: 12004232
################################################################################

# your code below here


def get_type(userin):
    """Function to get the type of the input; also if int checks if the number 
    is above 12 or lower or equal; 
    Returns userin, type and for number >12 or <=12"""
    userintype = type(userin)  # get the type of the input
    if userin.isnumeric():
        userin = int(userin)
        if userin > 12:
            comp = "above 12"
        else:
            comp = "lower or equal 12"
        return [str(userin), "number", comp]
    else:
        if userin == "True" or userin == "False":
            return [userin, "boolean"]
        elif userintype == str:
            return [userin, "string"]


# get input from the user
userin = input("Enter a text: ")
outtext = get_type(userin)
try:
    print("{} is a {} {}".format(outtext[0], outtext[1], outtext[2]))
except IndexError:
    print("{} is a {}".format(outtext[0], outtext[1]))
