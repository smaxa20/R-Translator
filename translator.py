import pandas as pd
import operator


# https://stackoverflow.com/a/2262424/9968135
# Decorator for ignoring exception from a function
# e.g.   @ignore_exception(DivideByZero)
# e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

# If the value parsable into an int, we return that value by default
# In this way we can get both an int and a non-int
def tryInt(value):
    return(ignore_exception(ValueError, value)(int)(value))


# Only give rows in the dataframe that adhere to all the conditions
def filter(*args):

    # https://stackoverflow.com/a/2983144/9968135
    ops = {
        "==" : operator.eq,
        "<" : operator.lt,
        ">" : operator.gt,
        "<=" : operator.le,
        ">=" : operator.ge,
        "!=" : operator.ne
    }

    df = args[0]
    i = 1
    while (i < len(args)):
        # Split a condition into it's three parts, the column name, the operator, and the value
        # All column names must be surrounded by '' -> e.g. 'my column'
        if "'" not in args[i]:
            return("Invalid column name: All column names must be surrounded by '' -> e.g. 'my column'")
        separateCol = args[i].split("'")
        condition = []
        condition.append(separateCol[1])
        condition = condition + separateCol[2].strip().split(" ")
        # If the condition string is of an invalid length, fail out
        if len(condition) > 3 or len(condition) < 2:
            return("Invalid argument length: " + str(len(condition)) + " -> " + args[i])
        op = ops[condition[1]]
        col = df[condition[0]]
        # If the condition string is of length 2, look for a variable as the next argument and take that as the value
        if len(condition) == 2:
            i += 1
            val = args[i]
        else:
            val = tryInt(condition[2])
        # Wittle down the original dataframe based on the first condition
        df = df.loc[ op(col, val) ]
        i += 1
        
    return(df)


# Sort the dataframe by the specified columns
# It will sort by the first column first, then subsequent columns within that sort
def arrange(*args):
    # The first argument must be the dataframe
    df = args[0]
    # All subsequent arguments must be the columns you'd like to sort by
    conditions = args[1:len(args)]
    columns = []
    orders = []
    for col in conditions:
        # If you want the column to be arranged in descending order you must wrap it in desc() -> e.g. desc(my column)
        if "(" in col and ")" in col and col[0:4] == "desc":
            orders.append(False)
            columns.append(col[5:len(col)-1])
        else:
            orders.append(True)
            columns.append(col)

    # both arguments take lists which we've build side-by-side
    df = df.sort_values(columns, ascending=orders)
    return(df)