import os, win32api, win32file
from datetime import datetime


def get_drive_name():
    my_drive = []
    DRIVE_REMOVABLE = 2
    drives = win32api.GetLogicalDriveStrings().split('\000')[::-1]
    for item in drives:
        if win32file.GetDriveType(item) == DRIVE_REMOVABLE:
            my_drive.append(item)
    if my_drive:
        for item in my_drive:
            if win32api.GetVolumeInformation(item[0:3])[0] == 'FLASH_DRIVE':
                return item[0]
    else:
        print('Cannot find removable drive')
        return None


def new_dirs():
    drive_letter = get_drive_name()
    os.chdir(f'{drive_letter}:\\pythonProject_Tests\\University_progs')
    date = datetime.today().strftime('%Y/%m/%d').split('/')
    os.chdir(f'{drive_letter}:\\pythonProject_Tests\\University_progs')
    for item in date:
        if os.path.exists(dir := f'{item}'):
            os.chdir(dir)
        else:
            os.mkdir(dir)
            os.chdir(dir)


new_dirs()