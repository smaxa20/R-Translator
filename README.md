# translatR

This library is designed to allow Python developers to manipulate data using [Pandas](https://pandas.pydata.org/docs/), but with syntax from the R library [dplyr](https://dplyr.tidyverse.org/articles/dplyr.html#single-table-verbs) with a focus on dplyr's 9 single table verbs. The computations and manipulations are eventually done using Pandas, but the syntax is as close to dplyr as we could get them.

### `filter(*args)` 
• Allows you to select a subset of rows in a data frame.

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are magic strings representing conditions that the rows that you'd like to filter for must meet.

• All column names must be in single quotes.

• In order to compare against a variable, end the string after the operator and the next argument must be the variable.

• Example:
```python
result = "Complete"
# translatR code
r.filter(data, "'GN/LS' >= 10", "'RESULT' ==", result, "'YARD LN' < 0")

# pandas code
data.loc[(data["GN/LS"] >= 10) & (data["RESULT"] == result) & (data["YARD LN"] < 0)]

-->

   ODK  PLAY NUM  DN  DIST HASH  YARD LN PLAY TYPE  GN/LS    RESULT OFF FORM  OFF PLAY  QTR
6    O        20   3   8.0    R      -41      Pass   14.0  Complete     TRIO   HYUNDAI    1
15   O        49   3  14.0    R      -39      Pass   15.0  Complete  DOUBLES      UTAH    1
19   O        63   1  10.0    L       -5      Pass   13.0  Complete  DOUBLES        B1    2
29   O        79   2  12.0    L       -5      Pass   13.0  Complete  DOUBLES       KIA    2
34   O        84   2   4.0    L      -34      Pass   31.0  Complete     TRIO   ROCKETS    2
43   O       107   3   5.0    R      -33      Pass   20.0  Complete  DOUBLES      JAZZ    3
59   O       140   3  12.0    L       -3      Pass   15.0  Complete     TRIO   HYUNDAI    3
71   O       173   1  10.0    R      -25      Pass   10.0  Complete  DOUBLES      UTAH    4
80   O       187   1  10.0    L      -27      Pass   13.0  Complete  DOUBLES      ZONA    4
81   O       188   1  10.0    L      -40      Pass   12.0  Complete  DOUBLES       KIA    4
86   O       196   1  10.0    L      -31      Pass   17.0  Complete    TRIPS  COLORADO    4
```

### `Arrange(*args)`
• Sort the dataframe by the specified columns.

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are column names that you'd like to sort by.

• Sorts by the first column first, then subsequent columns within that sort.

• If you want the column to be arranged in descending order you must wrap it in `desc()`.

• Example:
```python
# translatR code
r.arrange(data, "desc(GN/LS)", "DN")

# pandas code
data.sort_values(["GN/LS", "DN"], ascending=[True, False])

-->

   ODK  PLAY NUM  DN  DIST HASH  YARD LN  PLAY TYPE  GN/LS         RESULT   OFF FORM  OFF PLAY  QTR
17   O        51   2  10.0    M       46       Pass   46.0   Complete, TD      BUNCH    BAYLOR    1
25   O        73   2   6.0    R      -22        Run   41.0           Rush      TRIPS      ARMY    2
34   O        84   2   4.0    L      -34       Pass   31.0       Complete       TRIO   ROCKETS    2
8    O        22   1  10.0    L       33       Pass   23.0       Complete       TREY      HEAT    1
38   O        88   1  10.0    L       20       Pass   20.0   Complete, TD      TIGER   RAINBOW    2
43   O       107   3   5.0    R      -33       Pass   20.0       Complete    DOUBLES      JAZZ    3
86   O       196   1  10.0    L      -31       Pass   17.0       Complete      TRIPS  COLORADO    4
36   O        86   2  10.0    L       35       Pass   15.0       Complete    DOUBLES     LARRY    2
15   O        49   3  14.0    R      -39       Pass   15.0       Complete    DOUBLES      UTAH    1
59   O       140   3  12.0    L       -3       Pass   15.0       Complete       TRIO   HYUNDAI    3
                                        •       •       •
```

### `select(*args)`
• Select certain columns.

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are column names that you'd like to select.

• Example:
```python
# translatR code
r.select(data, "GN/LS", "OFF PLAY")

# pandas code
data[['GN/LS','OFF PLAY']]

-->

    GN/LS  OFF PLAY
0     0.0      MAUI
1     1.0      ARMY
2     0.0   ROCKETS
3     2.0      MINI
4     0.0    PIRATE
5    14.0   HYUNDAI
6    12.0        A1
7    23.0      HEAT
8    10.0    OREGON
9    -2.0      ARMY
10    0.0      POST
```

### `rename(*args)`
• Rename any number of columns

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are magic strings with this form: 'old column name' = 'new column name'.

• Example:
```python
# translatR code
r.rename(data, "'ODK' = 'odk'", "'HASH' = 'hash'")

# pandas code
data.rename(columns={"ODK":"odk", "HASH":"hash"})

-->

   odk  PLAY NUM  DN  DIST hash  YARD LN  PLAY TYPE  GN/LS         RESULT   OFF FORM  OFF PLAY  QTR
0    O        10   1  10.0    L      -36       Pass    0.0     Incomplete    DOUBLES      MAUI    1
1    O        11   2  10.0    L      -36        Run    1.0           Rush    DOUBLES      ARMY    1
2    O        12   3   9.0    L      -37       Pass    0.0     Incomplete      TRIPS   ROCKETS    1
3    O        18   1  10.0    L      -39       Pass    2.0       Complete      TRIPS      MINI    1
4    O        19   2   8.0    R      -41       Pass    0.0     Incomplete     HAMMER    PIRATE    1
5    O        20   3   8.0    R      -41       Pass   14.0       Complete       TRIO   HYUNDAI    1
6    O        21   1  10.0    M       45        Run   12.0           Rush    DOUBLES        A1    1
7    O        22   1  10.0    L       33       Pass   23.0       Complete       TREY      HEAT    1
8    O        23   1  10.0    R       10       Pass   10.0   Complete, TD    DOUBLES    OREGON    1
9    O        38   1  10.0    L      -29        Run   -2.0           Rush    TRIGGER      ARMY    1
10   O        39   2  12.0    L      -27       Pass    0.0   Interception     HAMMER      POST    1
                                        •       •       •
```

### `mutate(*args)`
• Add columns and populate with data from existing columns. 

• Can use a column just generated to create a new one in all one call.

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are magic strings with this form: 'new column name' = 'column or literal' 'operator' 'column or literal'

• All column names must be in single quotes.

• Example:
```python
# translatR code
r.mutate(data, "'1ST MRK' = 'YARD LN' - 'DIST'", "'YDLN' = '1ST MRK' + 'DIST'", "'MEGA GAIN' = 'GN/LS' * '10'")

# pandas code
data.assign(test = lambda x: x.DN - x.DIST).assign(test1 = lambda x: x.test + x.DIST).assign(test2 = lambda x: x.DN * 10)

-->

   ODK  PLAY NUM  DN  DIST HASH  YARD LN  PLAY TYPE  GN/LS         RESULT   OFF FORM  OFF PLAY  QTR  1ST MRK  YDLN  MEGA GAIN
0    O        10   1  10.0    L      -36       Pass    0.0     Incomplete    DOUBLES      MAUI    1    -46.0 -36.0        0.0
1    O        11   2  10.0    L      -36        Run    1.0           Rush    DOUBLES      ARMY    1    -46.0 -36.0       10.0
2    O        12   3   9.0    L      -37       Pass    0.0     Incomplete      TRIPS   ROCKETS    1    -46.0 -37.0        0.0
3    O        18   1  10.0    L      -39       Pass    2.0       Complete      TRIPS      MINI    1    -49.0 -39.0       20.0
4    O        19   2   8.0    R      -41       Pass    0.0     Incomplete     HAMMER    PIRATE    1    -49.0 -41.0        0.0
5    O        20   3   8.0    R      -41       Pass   14.0       Complete       TRIO   HYUNDAI    1    -49.0 -41.0      140.0
6    O        21   1  10.0    M       45        Run   12.0           Rush    DOUBLES        A1    1     35.0  45.0      120.0
7    O        22   1  10.0    L       33       Pass   23.0       Complete       TREY      HEAT    1     23.0  33.0      230.0
8    O        23   1  10.0    R       10       Pass   10.0   Complete, TD    DOUBLES    OREGON    1      0.0  10.0      100.0
9    O        38   1  10.0    L      -29        Run   -2.0           Rush    TRIGGER      ARMY    1    -39.0 -29.0      -20.0
10   O        39   2  12.0    L      -27       Pass    0.0   Interception     HAMMER      POST    1    -39.0 -27.0        0.0
                                        •       •       •
```

### `transmutate(*args)`

• Same as `mutate()` but only the new columns are kept.

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are magic strings with this form: 'new column name' = 'column or literal' 'operator' 'column or literal'

• All column names must be in single quotes.

• Example:
```python
# translatR code
r.transmute(data, "'1ST MRK' = 'YARD LN' - 'DIST'", "'YDLN' = '1ST MRK' + 'DIST'", "'MEGA GAIN' = 'GN/LS' * '10'")

# pandas code
data = data.assign(col1 = lambda x: x.DN - x.DIST).assign(col2 = lambda x: x.test + x.DIST).assign(col3 = lambda x: x.DN * 10)
data[['col1', 'col2', 'col3']]

-->

    1ST MRK  YDLN  MEGA GAIN
0     -46.0 -36.0        0.0
1     -46.0 -36.0       10.0
2     -46.0 -37.0        0.0
3     -49.0 -39.0       20.0
4     -49.0 -41.0        0.0
5     -49.0 -41.0      140.0
6      35.0  45.0      120.0
7      23.0  33.0      230.0
8       0.0  10.0      100.0
9     -39.0 -29.0      -20.0
10      3.0   3.0        0.0
      •       •       •
```

### `summarise(*args)`
• Summarise the data using a statistical analysis tool

• Tools supported: mean, median, sd, IQR, mad, min, max, quantile, first, last, nth, n, n_distinct, any, all

• The first argument is the Pandas dataframe you'd like to manipulate.

• All other arguments are magic strings with this form: 'new column name' = 'tool'('column to use').

• All terms (column names and tools) must be in single quotes

• Example:
```python
# translatR code
r.summarise(data, "'mean_of_DIST' = 'mean'('DIST')")

# pandas code
"mean_of_DIST = " + str(data['DIST'].mean())

-->

mean_of_DIST 9.178947368421053
```

### `sample_n(data, size)`
• Take a random sample of n rows

• The first argument is the Pandas dataframe you'd like to manipulate.

• The second argument is the size of the sample you'd like.

• Example:
```python
# translatR code
r.sample_n(data, 10)

# pandas code
data.sample(n=10, random_state=1)

-->

   ODK  PLAY #  DN  DIST HASH  YARD LN PLAY TYPE  GN/LS      RESULT OFF FORM OFF PLAY  QTR  1ST MRK  YDLN  MEGA GAIN
76   O     178   2  12.0    M      -45      Pass  -10.0     Penalty     TRIO  HYUNDAI    4    -10.0   2.0         20
83   O     190   2  10.0    L       48      Pass    1.0    Complete  DOUBLES     JAZZ    4     -8.0   2.0         20
27   O      75   1  10.0    L      -37       Run    6.0      Fumble        0        0    2     -9.0   1.0         10
7    O      21   1  10.0    M       45       Run   12.0        Rush  DOUBLES       A1    1     -9.0   1.0         10
34   O      84   2   4.0    L      -34      Pass   31.0    Complete     TRIO  ROCKETS    2     -2.0   2.0         20
28   O      78   1  10.0    M       -7       Run   -2.0        Rush  DOUBLES     NAVY    2     -9.0   1.0         10
44   O     108   1  10.0    M       47      Pass    7.0    Complete  DOUBLES       A2    3     -9.0   1.0         10
61   O     142   2  10.0    L      -18       Run    3.0        Rush  DOUBLES     NAVY    3     -8.0   2.0         20
77   O     179   2  22.0    M      -35      Pass    0.0  Incomplete     TREY  GANDALF    4    -20.0   2.0         20
32   O      82   3   6.0    L      -22      Pass    6.0    Complete     TRIO  ROCKETS    2     -3.0   3.0         30
```

### `sample_f(data, frac)`
• Take a random sample of rows equal to a fraction of the total size of the dataframe

• The first argument is the Pandas dataframe you'd like to manipulate.

• The second argument is the fraction you'd like to use to get the sample size.

• Example:
```python
# translatR code
r.sample_f(data, 0.1)

# pandas code
print(data.sample(frac=0.1))

-->

   ODK  PLAY #  DN  DIST HASH  YARD LN PLAY TYPE  GN/LS      RESULT OFF FORM OFF PLAY  QTR  1ST MRK  YDLN  MEGA GAIN
83   O     190   2  10.0    L       48      Pass    1.0    Complete  DOUBLES     JAZZ    4     -8.0   2.0         20
84   O     191   3   9.0    R       47      Pass    0.0  Incomplete     TRIO  HYUNDAI    4     -6.0   3.0         30
32   O      82   3   6.0    L      -22      Pass    6.0    Complete     TRIO  ROCKETS    2     -3.0   3.0         30
4    O      18   1  10.0    L      -39      Pass    2.0    Complete    TRIPS     MINI    1     -9.0   1.0         10
71   O     173   1  10.0    R      -25      Pass   10.0    Complete  DOUBLES     UTAH    4     -9.0   1.0         10
3    K      13   4   9.0    L      -37      Punt    0.0      Downed        0        0    1     -5.0   4.0         40
40   O     104   1  10.0    R      -28       Run    1.0        Rush     TRIO        0    3     -9.0   1.0         10
62   O     143   1  10.0    L      -36      Pass    1.0    Scramble  DOUBLES      AF2    3     -9.0   1.0         10
67   O     160   1  10.0    R      -35       Run    2.0        Rush   HAMMER    GREEN    4     -9.0   1.0         10
22   O      66   3   6.0    R      -22      Pass    0.0  Incomplete   HAMMER   PIRATE    2     -3.0   3.0         30
```