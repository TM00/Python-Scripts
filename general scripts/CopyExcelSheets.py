import pandas as pd
from pathlib import Path, PureWindowsPath
import xlwings as xw

path = "FirstExcelFile.xlsx"
path2 = "SecondExcelFile rev3.xlsx"

wb1 = xw.Book(path)
wb2 = xw.Book(path2)

for sheet in wb1.sheets:
    # Copy to second Book requires to use before or after
    sname = sheet.name
    bottomX = sname + " Bot_X"
    sheet.copy(after=wb2.sheets[0], name=bottomX)
    bottomY = sname + " Bot_Y"
    sheet.copy(after=wb2.sheets[0], name=bottomY)
    topX = sname + " Top_X"
    sheet.copy(after=wb2.sheets[0], name=topX)
    topY = sname + " Top_Y"
    sheet.copy(after=wb2.sheets[0], name=topY)



print("done")
