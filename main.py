from tika import parser
import pprint
from collections import defaultdict
import re
import pandas as pd

pp = pprint.PrettyPrinter(indent=3)
parsedPDF = parser.from_file("final-test.pdf")

content = parsedPDF['content']
contentlist = content.split('\n')

contentlist = list(filter(lambda a: a != '', contentlist))
iterateContent = iter(contentlist)
data = defaultdict(dict)
cntr = 0
line = 1

while True:
    try:
        string = next(iterateContent)
    except StopIteration:
        break

    if re.match('^[A-Z\s]+$', string):
        cntr += 1           

        data[cntr]['Name'] = string
        line = 2
        print('matched')

    elif line == 2:
        data[cntr]['Address'] = string
        line += 1

    elif line == 3:
        data[cntr]['Website'] = string
        line += 1

print("Total data:", len(data.keys()))
df = pd.DataFrame(data.values())
df.index += 1
print(df)

writer = pd.ExcelWriter("dataframe.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name='output', index=False)
writer.save()