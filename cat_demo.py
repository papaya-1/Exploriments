import pandas as pd
import ast

df = pd.read_csv("data/SB_publication_categorized.csv")
df['Categories'] = df['Categories'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)
cat = str(input())
filtered = df[df['Categories'].apply(lambda x: isinstance(x, list) and cat in x)]
print("")
print("Category: ", cat)
print("")
print("Articles")
print(filtered['Title'])
#print(type(df['Categories'].iloc[0]))

