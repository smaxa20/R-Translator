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


#filter() - translatR
result = "Complete"
print("Filter **********\n")
print(r.filter(data, "'GN/LS' >= 10", "'RESULT' ==", result, "'YARD LN' < 0"))
print()

#filter() - pandas
print(data.loc[(data["GN/LS"] >= 10) & (data["RESULT"] == result) & (data["YARD LN"] < 0)])



#arrange() - translatR
print("\n\nArrange **********\n")
print(r.arrange(data, "desc(GN/LS)", "DN"))
print()

#arrange() - pandas
print(data.sort_values(["GN/LS", "DN"], ascending=[True, False]))



#select() - translatR
print("\n\nSelect **********\n")
print(r.select(data, "GN/LS", "OFF PLAY"))
print()

#select() - pandas
print(data[['GN/LS','OFF PLAY']])
print()



#rename() - translatR
print("\n\nRename **********\n")
print(r.rename(data, "'ODK' = 'odk'", "'HASH' = 'hash'"))
print()

#rename() - pandas [rename and then set name back]
print(data.rename(columns={"ODK":"odk", "HASH":"hash"}))
print()



#mutate()
print("\n\nMutate **********\n")
print(r.mutate(data, "'1ST MRK' = 'YARD LN' - 'DIST'", "'YDLN' = '1ST MRK' + 'DIST'", "'MEGA GAIN' = 'GN/LS' * '10'"))
print()

#mutate() - pandas
print(data.assign(test = lambda x: x.DN - x.DIST).assign(test1 = lambda x: x.test + x.DIST).assign(test2 = lambda x: x.DN * 10))
print()



#transmute() - translatR
print("\n\nTransmute **********\n")
print(r.transmute(data, "'1ST MRK' = 'YARD LN' - 'DIST'", "'YDLN' = '1ST MRK' + 'DIST'", "'MEGA GAIN' = 'GN/LS' * '10'"))
print()

#transmute() - pandas
tempdata = data
data = data.assign(test = lambda x: x.DN - x.DIST).assign(test1 = lambda x: x.test + x.DIST).assign(test2 = lambda x: x.DN * 10)
tempData = data.rename(columns={"test":"1ST MRK", "test1":"YDLN", "test2":"MEGA GAIN"}) #rename
print(tempData[['1ST MRK', 'YDLN', 'MEGA GAIN']])
print()



#summarise() - translatR
print("\n\nSummarise **********\n")
print(r.summarise(data, "'mean_of_DIST' = 'mean'('DIST')")) #ORDER: dataframe, new column name, command, column with the data
print()

#summarise() - pandas
print("mean_of_DIST = " + str(data['DIST'].mean()))
print()



#sample_n() - translatR
print("\n\nsample_n **********\n")
print(r.sample_n(data, 10))
print()

#sample_n() = pandas
print(data.sample(n=10, random_state=1))
print()



#sample_f() - translatR
print("\n\nsample_f **********\n")
print(r.sample_f(data, 0.1))
print()

#sample_f() - pandas
print(data.sample(frac = .1))
print()