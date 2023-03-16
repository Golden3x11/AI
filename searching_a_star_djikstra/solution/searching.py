import pandas as pd

df = pd.read_csv('exercise/connection_graph_2.csv', dtype={"line": str})


df = df[(df['line'] == '33')& (df['end_stop'] == 'most Grunwaldzki') & (df["arrival_time"] == '16:31:00')]

for idx, value in df.iterrows():
    print(value)