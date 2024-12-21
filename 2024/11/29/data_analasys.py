import pandas as pd

data = pd.read_csv('E:\\Data\\yob2010.txt', names=['Name', 'Sex', 'Sum_n'])
#
# max_len_name = data.Name.apply(lambda item: len(item)).max()
#
# max_name = data['Name'].where(len(data['Name']) == max_len_name)
# print(max_name)
print(data['Name'])