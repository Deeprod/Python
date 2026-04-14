import pandas as pd

new_column_name = "Awards"
name_of_column_to_go_after = "Runtime"

path = r"C:\\temp\\github\\act-python\\Jonathan\\Movies\\"
df = pd.read_csv(path + "df.csv")
df = df.iloc[:, 1:] #We remove the first column which is the index

df.insert(df.columns.get_loc(name_of_column_to_go_after) + 1, new_column_name, pd.NA)
df.to_csv(path + "df.csv")