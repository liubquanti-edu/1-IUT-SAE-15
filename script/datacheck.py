import pandas as pd

csv_file = r'data\ADECal.csv'

data = pd.read_csv(csv_file)

unique_groups = data['Group'].unique()
unique_groups = sorted(map(str, unique_groups))

for group in unique_groups:
    print(group)