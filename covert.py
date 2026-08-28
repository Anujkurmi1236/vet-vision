import pandas as pd

df = pd.read_excel('data/csv/INCIDENCE_OF_LIVESTOCK_DISEASES_IN_INDIA.xls')

df.to_csv('data/csv/INCIDENCE_OF_LIVESTOCK_DISEASES_IN_INDIA.csv', index=False, encoding='utf-8')
print("Conversion complete!")