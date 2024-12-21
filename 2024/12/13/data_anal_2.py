import pandas as pd

file_path = 'E:\\Osipov_Michael_20150\\PythonProject\\University_progs\\output.txt'

data = pd.read_csv(file_path, delimiter=';', names=['group', 'isu_id', 'passbook_number', 'form', 'full_name'], encoding='windows-1251')

symbols = 'аеёиоуыэюя'
exep_names = ['Илья', 'Емеля', 'Савва', 'Лука', 'Кузьма', 'Фока', 'Фома', 'Зосима', 'Добрыня', 'Данила', 'Гаврила', 'Никита']
data_2 = list(filter(lambda x: len(x.split()) == 2, data['full_name']))


def check_sex_2(full_name):
    name = full_name.split()[1]
    if not name in exep_names:
        return name[-1] in symbols


data_2_f = list(filter(check_sex_2, data_2))
print(data_2_f)


def check_sex_3(full_name):
    second_name = full_name.split()[2]
    return second_name[-3:] == 'вна'


data_3 = list(filter(lambda x: len(x.split()) == 3, data['full_name']))
data_3_f = list(filter(check_sex_3, data_3))
print(data_3_f[:100])

# data_ = list(filter(lambda x: len(x.split()) > 3, data['full_name']))
#
# print(data_)
'''
Draft
'''