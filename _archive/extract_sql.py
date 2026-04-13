import pandas as pd

def clean(txt):
    txt = txt.strip()
    txt = txt.replace("'","")
    return txt

df = pd.DataFrame(columns=['Movie', 'Date', 'Rating', 'Year', 'Director', 'Writer', 'Cast'])

with open('/Users/jonathanventuri/Documents/Python/20241018.txt', 'r') as file:
    for line in file:
        line = line.split("'")
        new_line = []
        for i in [1,3,7,9,11,13,15]:
            new_line.append(clean(line[i]))

        df.loc[len(df)] = new_line
        print(new_line)

df.to_csv("/Users/jonathanventuri/Documents/Python/20241018.csv")


import pandas as pd
df2 = pd.read_csv("/Users/jonathanventuri/Documents/Python/20241018.csv")
print(df2)