import pandas as pd

df = pd.read_csv('Result/table.csv')

latex_table = df.to_latex(index=False, longtable=True)

with open('mytable.tex', 'w') as file:
    file.write(latex_table)

