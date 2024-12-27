# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, FormatStrFormatter)
# from pandas.core.interchange.dataframe_protocol import DataFrame
#
# file_path = 'E:\\pythonProject_Tests\\University_progs\\flot-05022024.csv'
# data = pd.read_csv(file_path, delimiter=';', encoding='windows-1251')
#
# data['decade'] = data['5'].apply(lambda item: item.split('.')[2][:3]) + '0s'
# data_grouped = data.groupby('decade').size()
# # print(data_grouped)
#
# plt.bar(data_grouped.index, data_grouped.values)
# plt.title("Some shit")
# plt.xlabel("Decades")
# plt.ylabel("Ships")
# plt.show()
#
# data['17'] = data['17'].apply(lambda item: item.replace(',', '.'))
# data['17'] = data['17'].astype('float64')
# data_grouped_2 = data.groupby('decade')['17'].sum()
# # print(data_grouped_2)
#
# plt.bar(data_grouped_2.index, data_grouped_2.values)
# plt.title("Some shit")
# plt.xlabel("Decades")
# plt.ylabel("Water stuff")
# plt.show()

