import numpy as np
import pandas as pd

data = np.loadtxt('F:\\pythonProject_Tests\\University_progs\\Data\\yob2010.txt', delimiter=',', dtype='U')
# data[:,2].astype('i').dtype

males = filter(lambda item: item[0] == 'M', data[:,1])
flt = np.array(list(males))
data_m = data[np.isin(data[:,1], flt)]
summ = data_m[:, 2].astype('i').sum()
print(summ)


# import numpy as np
#
# # Загрузка данных
# data = np.loadtxt('F:\\pythonProject_Tests\\University_progs\\Data\\yob2010.txt',
#                   delimiter=',', dtype='U')
#
# # Преобразование нужного столбца в числовой формат
# data[:, 2] = data[:, 2].astype(int)
#
# # Фильтрация строк для мужчин (M)
# data_m = data[data[:, 1] == 'M']  # Оставляем только строки, где второй столбец == 'M'
#
# # Суммирование третьего столбца (количество)
# summ = data_m[:, 2].astype(int).sum()
#
# print("Сумма для мужчин:", summ)
