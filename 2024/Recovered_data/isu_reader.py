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
    pass
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