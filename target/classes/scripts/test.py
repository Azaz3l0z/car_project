import pandas as pd
d: dict = {}

for k in range(15):
    d[k] = [x * k for x in list(range(10))]

df = pd.DataFrame(d)
print(df)
for k, val in enumerate(df[1]):
    if val == 2:
        df = df.drop([k])

d = df.to_dict('list')
print(d)