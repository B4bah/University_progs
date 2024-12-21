import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, FormatStrFormatter)
from pandas.core.interchange.dataframe_protocol import DataFrame

file_path = 'E:\\Osipov_Michael_20150\\pythonProject\\University_progs\\list_1007.csv'
data = pd.read_csv(file_path, delimiter=';', encoding='windows-1251')


def func(item):
    item = str(item)
    summ = 0
    if len(item) != 3:
        if ',' in item:
            # print(item)
            item_ = item.split(', ')
            for x in item_:
                summ += int(x[5:]) * 2**(4 - int(x[1]))
        else:
            summ += int(item[5:]) * 2**(4 - int(item[1]))
    return summ


data['paper_count'] = data['papers'].apply(func)
data['month'] = data['date_pub'].apply(lambda item: int(item[3:5]))
# data_count = data.groupby('month')['paper_count'].sum()
#
#
#
# print(data_count)
#
# plt.bar(data_count.index, data_count.values)
# plt.title("Papers count")
# plt.xlabel("Month")
# plt.ylabel("Papers")
# plt.show()
grouped_data = data.groupby(['month', 'department'])['paper_count'].sum().reset_index()

pivot_table = grouped_data.pivot(index='month', columns='department', values='paper_count')


pivot_table.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title("Papers Count by Month and Department")
plt.xlabel("Month")
plt.ylabel("Papers")
plt.xticks(range(12), [f'Month {i}' for i in range(1, 13)], rotation=45)
plt.legend(title="Department")
plt.tight_layout()
plt.show()

