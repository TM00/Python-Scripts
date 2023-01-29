import pandas as pd
from pathlib import Path, PureWindowsPath

## prints the name of all the sheets in a workbook to console

xls = pd.ExcelFile("Check_template rev 00.xlsx")
#xls = pd.ExcelFile(filename.name)

# Now you can list all sheets in the file
sheetNames = xls.sheet_names
# ['house', 'house_extra', ...]

# to read just one sheet to dataframe:
#df = pd.read_excel(file_name, sheet_name="house")

# print in new line
print("printing lists in new line")
  
print(*sheetNames, sep = "\n")

for sheetName in sheetNames:
    var = sheetName
    print(var)

for sheetName in sheetNames:
    var = "='"+sheetName+"'!$P$47"
    print(var)   