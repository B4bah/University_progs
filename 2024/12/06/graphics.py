import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.core.interchange.dataframe_protocol import DataFrame

file_path = 'E:\\Osipov_Michael_20150\\PythonProject\\University_progs\\output.txt'
# data = pd.read_csv(file_path, names=['Name', 'Sex', 'Amount'])
#
# ls_amount = []
# for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
#     ls_amount.append(data['Amount'][data['Name'].str.startswith(letter)].sum())
#data_1 = data[data['group'] == form_count]
# # Построение графика
# plt.figure(figsize=(12, 6))
# plt.bar(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), ls_amount, color='skyblue', edgecolor='black')
# plt.title('Total Amount of Names Starting with Each Letter', fontsize=16)
# plt.xlabel('Letter', fontsize=14)
# plt.ylabel('Total Amount', fontsize=14)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()

data = pd.read_csv(file_path, delimiter=';', names=['group', 'isu_id', 'passbook_number', 'form', 'full_name'], encoding='windows-1251')
del data['passbook_number']
del data['isu_id']
del data['full_name']
print(data)

forms_count = data.groupby('form').group.count()
print(forms_count)
# Подсчёт количества записей для каждой формы
# form_count = [data[data['form'] == form].shape[0] for form in forms]
# print(form_count)

# Построение графика
plt.figure(figsize=(12, 6))
plt.bar(forms_count.index, forms_count, color='skyblue', edgecolor='black')
plt.title('Количество записей для каждой формы', fontsize=16)
plt.xlabel('Форма', fontsize=14)
plt.ylabel('Количество', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()