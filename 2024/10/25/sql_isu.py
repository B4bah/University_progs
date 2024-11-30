import sqlite3, win32api, win32file, os


def get_drive_name():
    my_drive = []
    DRIVE_REMOVABLE = 2
    drives = win32api.GetLogicalDriveStrings().split('\000')
    for item in drives:
        if win32file.GetDriveType(item) == DRIVE_REMOVABLE:
            my_drive.append(item)
    if my_drive:
        for item in my_drive:
            if win32api.GetVolumeInformation(item[0:3])[0] == 'OSIPOV':
                return item[0]
    print('Cannot find removable drive')
    return False


drive_letter = get_drive_name()

file_path = False
if drive_letter:
    while True:
        file_name = input('Enter isu_database file name:\n>>> ')
        flag = False
        for path, dirs, files in os.walk(f'{drive_letter}:\\'):
            # print(path, dirs)
            if file_name in files:
                print(path, files)
                flag = True
                file_path = os.path.join(path, file_name)
                break
        if flag:
            break
        else:
            print(f'There is no such file as {file_name}')
            if input('If you want to finish program - type Enter:\n>>> ') == '':
                print('Thanks for using my project')
                break

if file_path:

    # while True:
    #     file_name = input('Enter file name with data for database:\n>>> ')
    #     flag = False
    #     for path, dirs, files in os.walk(f'{drive_letter}:\\'):
    #         # print(path, dirs)
    #         if file_name in files:
    #             print(path, files)
    #             flag = True
    #             file_path = os.path.join(path, file_name)
    #             break
    #     if flag:
    #         break
    #     else:
    #         print(f'There is no such file {file_name}')
    #         if input('If you want to finish program - type Enter:\n>>> ') == '':
    #             break





    # Creating database
    conn = sqlite3.connect('isu_database.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS isu_list (
        id INTEGER PRIMARY KEY,
        passbook_number INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    with open(file_path, 'r', encoding='utf-8') as file:
        isu_list = []
        next(file)  # Пропустить первую строку заголовка
        for line in file:
            # Удаление пробелов и разбиение строки по символу '|'
            parts = line.strip().split('|')
            # Приведение к нужному типу
            isu_id = int(parts[0].strip())
            passbook_number = int(parts[1].strip())
            full_name = parts[2].strip()
            password = parts[3].strip()
            isu_list.append([isu_id, passbook_number, full_name, password])

    # Executing data into database
    cursor.executemany('''
    INSERT INTO isu_list (id, passbook_number, full_name, password) VALUES (?, ?, ?, ?)
    ''', isu_list)

    conn.commit()
    cursor.execute("SELECT * FROM isu_list")


    print("Isu ID  | Passbook number | Full name                       | Password")
    # print('Isu ID  | Passbook number | Full name')
    for row in cursor.fetchall():
        print(f'{row[0]:<7} | {row[1]:<15} | {row[2]:<31} | {row[3]}')

    conn.close()





password = id_value + name_value[:2]
password_hash = hashlib.sha256(password.encode()).hexdigest()












conn = sqlite3.connect('isu_database.sqlite3')
cursor = conn.cursor()

with open(file_path, 'r', encoding='utf-8') as file:
    isu_list = []
    next(file)  # Пропустить первую строку заголовка
    for line in file:
        # Удаление пробелов и разбиение строки по символу '|'
        parts = line.strip().split('|')
        # Приведение к нужному типу
        isu_id = int(parts[0].strip())
        passbook_number = int(parts[1].strip())
        full_name = parts[2].strip()
        password = parts[3].strip()
        isu_list.append([isu_id, passbook_number, full_name, password])

# Executing data into database
cursor.executemany('''
INSERT INTO isu_list (id, passbook_number, full_name, password) VALUES (?, ?, ?, ?)
''', isu_list)

conn.commit()