import numpy as np
import pandas as pd

data = np.loadtxt('F:\\pythonProject_Tests\\University_progs\\Data\\yob2010.txt', delimiter=',', dtype='U')
data[:,2].astype('i').dtype

first_letter_m = filter(lambda item: item[0] == 'M', data[:,0])
flt = np.array(list(first_letter_m))
data_m = data[np.isin(data[:,0], flt)]
print(data_m)
