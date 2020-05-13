import pandas as pd
import translator as r

pd.set_option("display.max_rows", 1000)

# Change the file name of the Excel sheet of raw data under "input_file_name"
input_file_name = "Linfield2019Data.xlsx"
# Make sure to specify the correct sheet name
sheet = "Linfield Data"

data = pd.read_excel(input_file_name, sheet, index_col = None, header = 0, na_values = " ")
data = data.sort_values("PLAY #")
data = data.reset_index()
del data["index"]
data = data.dropna(how = "all")
data = data.fillna(0)

result = "Complete"

print(r.filter(data, "'GN/LS' >= 10", "'RESULT' ==", result, "'YARD LN' < 0"))
print(data.loc[(data["GN/LS"] >= 10) & (data["RESULT"] == result) & (data["YARD LN"] > 0)])

print(r.arrange(data, "desc(GN/LS)", "DN"))
print(data.sort_values(["GN/LS", "DN"], ascending=[True, False]))