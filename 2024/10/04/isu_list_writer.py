import win32api
import win32file


def isu_write():
    print('First enter ID then passbook number then name, surname and second name, all divided by Enter')
    isu_dict = dict()
    while True:
        print('Enter ID', end='')
        while inp := input(':\n>>> '):
            print(isu_dict.keys())
            if not inp in isu_dict.keys():
                if len(inp) == 6:
                    if inp.isdigit():
                        isu_dict[inp] = None
                        break
                    else:
                        print('ID has to contain only arabic digits. Try again', end='')
                else:
                    print('Incorrect length of ID, it has to be 6 digits. Try again', end='')
            else:
                print('This ID is already taken. Try again', end='')
        print('Enter passbook number', end='')
        while pbn := input(':\n>>> '):
            if not pbn in isu_dict.values():
                if len(pbn) == 7:
                    if pbn.isdigit():
                        isu_dict[inp] = [pbn]
                        break
                    else:
                        print('Passbook number has to contain only arabic digits. Try again', end='')
                else:
                    print('Incorrect length of passbook number, it has to be 7 digits. Try again', end='')
            else:
                print('This passbook number is already taken. Try again', end='')
        print('Enter surname, name, second name', end='')
        while name := input(':\n>>> '):
            if not name in isu_dict.values():
                if any(1072 <= ord(letter.lower()) <= 1103 for letter in name):
                    if all(1072 <= ord(letter.lower()) <= 1103 or letter == ' ' for letter in name):
                        name = ' '.join([word.capitalize() for word in name.split()])
                        isu_dict[inp] += [name]
                        break
                    else:
                        print('Name, surname and second name have to contain only russian letters and spaces between words. Try again', end='')
            else:
                print('This name is already taken. Try again', end='')
        if not (input('To continue entering members of group 20150 enter space:\n>>> ') == ' '):
            return isu_dict
    return isu_dict


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


drive_letter = get_drive_name()


def file_output(file_path):
    global drive_letter
    with open(file_path, encoding='UTF-8') as file:
        print(f'------------{file.name}------------')
        for line in file.readlines():
            print(line.strip())
        print(f'------------{file.name}------------')


def isu_file():
    file_output(f'{drive_letter}:/Osipov_Michael_20150/pythonProject/University_progs/20150_members.txt')

    while not (file_mode := input('If you wanna append lines in group 20150, enter a. Else enter w:\n>>> ')) in ('a', 'w'):
        print("File mode can only be 'a' (append) or 'w' (write)")

    isu_dict = isu_write()

    with open(f'{drive_letter}:/Osipov_Michael_20150/pythonProject/University_progs/20150_members.txt', file_mode, encoding='UTF-8') as file:
        if file_mode == 'w':
            file.write('Isu ID | Passbook number | Full name\n')
        for line in isu_dict.items():
            line_str = f'{line[0]} | {line[1][0]}         | {line[1][1]}\n'
            file.write(line_str)

    file_output(f'{drive_letter}:/Osipov_Michael_20150/pythonProject/University_progs/20150_members.txt')


isu_file()
