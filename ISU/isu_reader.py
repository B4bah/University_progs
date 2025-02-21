import win32api
import win32file
import os
import hashlib

def get_drive_name():
    my_drive = []
    DRIVE_REMOVABLE = 2
    drives = win32api.GetLogicalDriveStrings().split('\000')[::-1]
    for item in drives:
        if win32file.GetDriveType(item) == DRIVE_REMOVABLE:
            my_drive.append(item)
    if my_drive:
        for item in my_drive:
            if win32api.GetVolumeInformation(item[0:3])[0] == 'OSIPOV':
                return item[0]
    else:
        print('Cannot find removable drive')
        return False


def file_checker(path_):
    with open(path_, encoding='UTF-8') as file_:
        data = []
        for line_ in file_.readlines()[1:]:
            line1 = line_.replace(' ', '.').split('.')
            if len(line1[0]) == 6 and line1[0].isdigit():
                if len(line1[1]) == 7 and line1[1].isdigit():
                    if all(1072 <= ord(lt.lower()) <= 1103 or lt == ' ' for lt in ' '.join(line1[2:])):
                        data.append(line1)
    return data


drive_letter = get_drive_name()

if drive_letter:
    while file_name := input('Enter file name you are looking for:\n>>> '):
        flag = False
        for path, dirs, files in os.walk(f'{drive_letter}:'):
            if file_name in files:
                print(path, files)
                flag = True
                # data = file_checker(f'{path}\\{file_name}')
                data = [line.strip() for line in open(f'{path}\\{file_name}')]
                with open(f'{path}\\{file_name}', 'w', encoding='UTF-8') as new_file:
                    new_file.write('Isu ID | Passbook number | Surname, Name, Second name\n')
                    for item in data:
                        new_file.write(f'{data}\n')
                with open(f'{path}\\{file_name}', encoding='UTF-8') as file:
                    for line in file.readlines():
                        print(line.strip())
                    name = input('Enter your name:\n>>> ')
                    if name in file.readlines():
                        data_copy = []
                        data_copy_ = []
                        flag = False
                        for line in file.readlines():
                            if (not name in line) and not flag:
                                data_copy.append(line)
                            else:
                                flag = True
                                data_copy_.append(line)

                        password = input('Enter a password:\n>>> ')
                        password_hash = hashlib.sha256(password.encode()).hexdigest()

                        with open(f'{path}\\{file_name}', 'w', encoding='UTF-8') as file:
                            for item in data_copy:
                                file.write(item)
                            file.write(f'{data_copy_[0][:-2]} | {password_hash}')
                            for item in data_copy_[1:]:
                                file.write(item)
                    else:
                        print('There is not the name you have entered in this file')
                break
        if not flag:
            print('There is no file which name you have entered')