import pandas as pd
import operator
import random
import math

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
	
# Select certain columns 
def select(*args):
	#the first argument must be the data frame
	df = args[0]
	# the following arguments are the various column names
	# grab only those columns
	df = df.loc[:, args[1:len(args)]]
	return(df)
	
# Rename any number of select columns
def rename(*args):
	df = args[0]
	#the following arguments are the various column names with what they are to be substituted with
	conditions = args[1:] 
	#create a local dictionary to hold the renaming variables
	argStr = {} 
	for col in conditions:
		#update the dictionary
		argStr.update(col) 
	#go through renaming process
	df = df.rename(columns=argStr) 
	return(df)
	
# Mutate - Add columns and populate with data from existing columns. In can use a column just generated to create a new one in all one call
def mutate(*args):
	# The first argument must be the dataframe
	df = args[0]
	
	# https://stackoverflow.com/a/2983144/9968135
	ops = {
        "+" : operator.add,
        "-" : operator.sub,
        "*" : operator.mul,
        "/" : operator.truediv,
    }

	i = 1
	while i < len(args):
		# Split a condition into it's four parts, the new column name, the operator, and the two terms to be mutated
        # All column names and values must be surrounded by '' -> e.g. 'my column', '10'
		terms = args[i].split("'")
		new = terms[1]

		# If a term is an int we want to cast it to an int, but if it's not we want to keep it as a column
		if isinstance(tryInt(terms[3]), int):
			term1 = int(terms[3])
		else:
			term1 = df[terms[3]]
		if isinstance(tryInt(terms[5]), int):
			term2 = int(terms[5])
		else:
			term2 = df[terms[5]]

		op = ops[terms[4].strip()]

		# Assign each new column to the mutation of the two terms with respect to the operator
		df = df.assign(temp = op(term1, term2))
		# Rename the new column to what the developer wanted it to be
		df = df.rename(columns={"temp" : new})
		i += 1
	return df
	
def transmute(*args):
	# The first argument must be the dataframe
	df = args[0]
	names = []
	# https://stackoverflow.com/a/2983144/9968135
	ops = {
        "+" : operator.add,
        "-" : operator.sub,
        "*" : operator.mul,
        "/" : operator.truediv,
    }

	i = 1
	while i < len(args):
		# Split a condition into it's four parts, the new column name, the operator, and the two terms to be mutated
        # All column names and values must be surrounded by '' -> e.g. 'my column', '10'
		terms = args[i].split("'")
		new = terms[1]

		# If a term is an int we want to cast it to an int, but if it's not we want to keep it as a column
		if isinstance(tryInt(terms[3]), int):
			term1 = int(terms[3])
		else:
			term1 = df[terms[3]]
		if isinstance(tryInt(terms[5]), int):
			term2 = int(terms[5])
		else:
			term2 = df[terms[5]]

		op = ops[terms[4].strip()]

		# Assign each new column to the mutation of the two terms with respect to the operator
		df = df.assign(temp = op(term1, term2))
		# Rename the new column to what the developer wanted it to be
		df = df.rename(columns={"temp" : new})
		names.append(new)
		i += 1
	df = df[names]
	return df
	
#summarise 
def summarise(*args):
	df = args[0]
	i = 1
	while i < len(args):
		terms = args[i].split("'")
		new = terms[1]
		func = terms[3]
		col = terms[5]
		#determine which statistical analysis tool is to be used
		if func == "mean":
			temp = df[col].mean()
		elif func == "median":
			temp = df[col].median()		
		elif func == "sd":
			temp = df[col].std()		
		elif func == "IQR":
			Q1 = df[col].quantile(0.25)
			Q3 = df[col].quantile(0.75)
			temp = Q3 - Q1	
		elif func == "mad":
			temp = df[col].mad()
		elif func == "min":
			temp = df[col].min()		
		elif func == "max":
			temp = df[col].max()		
		elif func == "quantile":
			temp = df[col].quantile()
		elif func == "first":
			temp = df[col].first()	
		elif func == "last":
			temp = df.last(col)				
		elif func == "nth":
			temp = df[col].nth()
		elif func == "n":
			temp = df[col].count()		
		elif func == "n_distinct":
			temp = df[col].n_distinct()
		elif func == "any":
			temp = df[col].any()
		elif func == "all":
			temp = df[col].all()					
		i+=1
	temp = str(new) + " " + str(temp)
	return temp

#sample_n() - take a random sample of rows [size of sample specified in args]
def sample_n(*args):
	df = args[0]
	sampleSize = args[1]
	length = df.shape[0]
	sample = random.sample(range(0, length), sampleSize)
	df = df.iloc[sample]
	return df
	
#sample_f()
def sample_f(*args):
	df = args[0]
	percentageSize = args[1]
	length = df.shape[0]
	numOfSample = math.ceil(percentageSize * length)
	sample = random.sample(range(0, length), numOfSample)
	df = df.iloc[sample]
	return df
	
		
		
		
		
		
		
		
		
		
		
	