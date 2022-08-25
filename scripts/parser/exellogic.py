import openpyxl

book = openpyxl.open("OLX.xlsx", read_only=True)
sheet = book.active


print(sheet[1][2].value)
