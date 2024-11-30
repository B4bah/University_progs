import sqlite3, win32api, win32file


def get_drive_name():
    my_drive = []
    DRIVE_REMOVABLE = 2
    drives = win32api.GetLogicalDriveStrings().split('\000')[::-1]
    for item in drives:
        if win32file.GetDriveType(item) == DRIVE_REMOVABLE:
            my_drive.append(item)
    if my_drive:
        for item in my_drive:
            if win32api.GetVolumeInformation(item[0:3])[0] == drive_name:
                return item[0]
    else:
        print('Cannot find removable drive')
        return None


drive_name = 'OSIPOV'

file_path = 'E:\\Osipov_Michael_20150/pythonProject/University_progs/20150_members.txt'
db_file_path = 'E:\\Osipov_Michael_20150/pythonProject/University_progs/isu_database.sqlite3'
# Creating database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS isu_list (
#     id INTEGER PRIMARY KEY,
#     passbook_number INTEGER NOT NULL,
#     full_name TEXT NOT NULL,
#     password TEXT NOT NULL
# )
# ''')
#
# with open(file_path, 'r', encoding='utf-8') as file:
#     isu_list = []
#     next(file)  # Пропустить первую строку заголовка
#     for line in file:
#         # Удаление пробелов и разбиение строки по символу '|'
#         parts = line.strip().split('|')
#         # Приведение к нужному типу
#         isu_id = int(parts[0].strip())
#         passbook_number = int(parts[1].strip())
#         full_name = parts[2].strip()
#         password = parts[3].strip()
#         isu_list.append([isu_id, passbook_number, full_name, password])
#
# # Executing data into database
# cursor.executemany('''
# INSERT INTO isu_list (id, passbook_number, full_name, password) VALUES (?, ?, ?, ?)
# ''', isu_list)
#
# conn.commit()

print('Isu ID | Passbook number | Full name                       | Password                                                         | Photo')
# print('Isu ID  | Passbook number | Full name')
for row in cursor.execute('SELECT * FROM isu_list ORDER BY full_name').fetchall():
    print(f'{row[0]:<6} | {row[1]:<15} | {row[2]:<31} | {row[3]} | photo_{row[0]}')

# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write('Isu ID | Passbook number | Full name                       | Password                                                         | Photo')
#     for row in cursor.execute('SELECT * FROM isu_list ORDER BY full_name').fetchall():
#         f.write(f'\n{row[0]:<6} | {row[1]:<15} | {row[2]:<31} | {row[3]} | photo_{row[0]}')
conn.close()