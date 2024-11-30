import random, os, win32api, win32file, hashlib


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
        return None


class Password:
    def __init__(self, title, dir_, length=8):
        self.title = title
        self.dir_ = dir_
        self.length = length
        self.password = ''
        alphabet = 'abcdefghijklmnopqrstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%&*+,-./:;<=>?@_~'
        for i in range(self.length):
            self.password += random.choice(alphabet)
        os.chdir(f'{drive_letter}:\\')
        if os.path.exists(f'{self.dir_}'):
            os.chdir(self.dir_)
        else:
            os.mkdir(f'{self.dir_}')
            os.chdir(f'{self.dir_}')


    def write(self):
        with open(f'{drive_letter}:/{self.dir_}/{self.title}.txt', 'w') as file:
            file.write(self.password)
            os.startfile(f'{drive_letter}:/{self.dir_}/{self.title}.txt')


drive_letter = get_drive_name()

password = Password(input(f'The current drive is {drive_letter}.\nEnter the title for the password:\n>>> '),
                    input('Enter a directory for passwords:\n>>> '),
                    int(input('Enter the password length:\n>>> ')))
password.write()