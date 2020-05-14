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

#filter() - translatR
print(r.filter(data, "'GN/LS' >= 10", "'RESULT' ==", result, "'YARD LN' < 0"))
#filter() - pandas
print(data.loc[(data["GN/LS"] >= 10) & (data["RESULT"] == result) & (data["YARD LN"] < 0)])

#arrange() - translatR
print(r.arrange(data, "desc(GN/LS)", "DN"))
#arrange() - pandas
print(data.sort_values(["GN/LS", "DN"], ascending=[True, False]))

#select() - translatR
print(r.select(data, "ODK", "HASH"))
#select() - pandas
print(data[['ODK','HASH']])

#rename() - translatR
print(r.rename(data, {'ODK':'odk'}, {'HASH':'hash'}))
print(r.rename(data, {'odk':'ODK'}, {'hash':'HASH'}))
#rename() - pandas [rename and then set name back]
print(data.rename(columns={"ODK":"odk"}))
print(data.rename(columns={"odk":"ODK"}))

#mutate()
#transmute()