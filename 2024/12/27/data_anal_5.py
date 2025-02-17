import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, FormatStrFormatter)
from pandas.core.interchange.dataframe_protocol import DataFrame

file_path1 = 'E:\\pythonProject_Tests\\University_progs\\Data\\yob2009.txt'
file_path2 = 'E:\\pythonProject_Tests\\University_progs\\Data\\yob2010.txt'
data1 = pd.read_csv(file_path1, delimiter=',', names=['Name', 'Sex', 'Amount'], encoding='windows-1251')
data2 = pd.read_csv(file_path2, delimiter=',', names=['Name', 'Sex', 'Amount'], encoding='windows-1251')

males_names_amount1 = data1.where(data1['Sex'] == 'M').groupby('Name')['Amount'].sum()
males_names_amount2 = data2.where(data2['Sex'] == 'M').groupby('Name')['Amount'].sum()
male_data = pd.merge(males_names_amount1, males_names_amount2, how='outer', on='Name')
males_data = male_data.fillna(0)
males_data['Amount'] = abs(males_data['Amount_x'] - males_data['Amount_y'])
male_max_diff = males_data.loc[males_data['Amount'] == males_data['Amount'].max()]
print(male_max_diff)

females_names_amount1 = data1.where(data1['Sex'] == 'F').groupby('Name')['Amount'].sum()
females_names_amount2 = data2.where(data2['Sex'] == 'F').groupby('Name')['Amount'].sum()
female_data = pd.merge(females_names_amount1, females_names_amount2, how='outer', on='Name')
females_data = female_data.fillna(0)
females_data['Amount'] = abs(females_data['Amount_x'] - females_data['Amount_y'])
female_max_diff = females_data.loc[females_data['Amount'] == females_data['Amount'].max()]
print(female_max_diff)


# with no separation by sex
# names_amount1 = data1.groupby('Name')['Amount'].sum()
# names_amount2 = data2.groupby('Name')['Amount'].sum()
# print(names_amount1, names_amount2)
#
# data = pd.merge(names_amount1, names_amount2, how='outer', on='Name')
# data = data.fillna(0)
# data['Amount'] = abs(data['Amount_x'] - data['Amount_y'])
# max_name = data.loc[data['Amount'] == data['Amount'].max()]
#
# print(max_name)
# data_grouped = data.groupby('decade').size()
# print(data_grouped)

# plt.bar(data_grouped.index, data_grouped.values)
# plt.title("Some shit")
# plt.xlabel("Decades")
# plt.ylabel("Ships")
# plt.show()
