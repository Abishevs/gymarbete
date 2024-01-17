import pandas as pd
from randomness.sim_stats import Column


df = pd.read_csv('Result/table.csv')

filtered = df[df[Column.ISSIGNIFICANT.value].isin(['Nej'])]

sorted_df = filtered.sort_values(by=Column.CHI2_STAT.value, ascending=False)

lowes_iterations = sorted_df.sort_values(by=Column.ITERATIONS.value,
                                         ascending=True)

print(lowes_iterations)
