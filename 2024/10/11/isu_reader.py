import win32api
import win32file
import os
import hashlib


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


def file_output(file_path):
    with open(file_path, encoding='UTF-8') as file_:
        print(f'----------------{file_.name}----------------')
        for line_ in file_.readlines():
            print(line_.strip())
        print(f'----------------{file_.name}----------------')


drive_letter = get_drive_name()
print(drive_letter)

if drive_letter:
    while True:
        file_name = input('Enter file name you are looking for:\n>>> ')
        flag = False
        for path, dirs, files in os.walk(f'{drive_letter}:\\'):
            if file_name in files:
                print(path, files)
                flag = True
                file_path = os.path.join(path, file_name)
                file_output(file_path)

                with open(file_path, encoding='UTF-8') as file:
                    lines = file.readlines()
                    if lines:
                        id_width = 8
                        code_width = 16
                        name_width = 32
                        password_width = 64

                for i, line in enumerate(lines[1:], start=1):
                    current_entry = [col.strip() for col in line.strip().split('|')]
                    if len(current_entry) >= 3:
                        id_value = current_entry[0]
                        code_value = current_entry[1]
                        name_value = current_entry[2]

                        password = id_value + name_value[:2]
                        password_hash = hashlib.sha256(password.encode()).hexdigest()

                        if len(current_entry) == 3:
                            current_entry.append(password_hash)
                        elif len(current_entry) == 4:
                            current_entry[3] = password_hash

                        lines[i] = (
                            f"{current_entry[0]:<{id_width}}| "
                            f"{current_entry[1]:<{code_width}}| "
                            f"{current_entry[2]:<{name_width}}| "
                            f"{current_entry[3]:<{password_width}}\n"
                        )

                with open(file_path, 'w', encoding='UTF-8') as file:
                    file.writelines(lines)
                file_output(file_path)
                break

        if flag:
            print('Thanks for using my project')
            break
        else:
            print('There is no file which name you have entered')