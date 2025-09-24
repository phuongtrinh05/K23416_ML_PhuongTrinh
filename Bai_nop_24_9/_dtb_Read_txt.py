import pandas as pd
df=pd.read_csv("../databases/SalesTransactions/SalesTransactions.csv",encoding = 'utf-8', dtype = 'unicode', sep = '\t')
print(df)