isu_list = ([136083, 2420055, 'Алтухов Роман Сергеевич'],
            [135979, 2420056, 'Асанов Михаил Александрович'],
            [135841, 2420057, 'Барышников Марк Антонович'],
            [136245, 2420058, 'Бинеман Никита Александрович'],
            [135786, 2420059, 'Бородаев Роман Игоревич'],
            [135798, 2420060, 'Быстров Владислав Андреевич'],
            [136233, 2420061, 'Гнетковская Мария Андреевна'],
            [136221, 2420062, 'Гонин Станислав Константинович'],
            [136049, 2420063, 'Горовцов Степан Сергеевич'],
            [136032, 2420064, 'Довбыш Александр Николаевич'],
            [136047, 2420065, 'Думбасар Максим Александрович'],
            [129196, 2420066, 'Егерев Роман Кириллович'],
            [135753, 2420067, 'Кучеренко Антон Вячеславович'],
            [135848, 2420068, 'Малышева Ирина Владимировна'],
            [136136, 2420069, 'Осипов Михаил Дмитриевич'],
            [136158, 2420070, 'Путятин Даниил Владимирович'],
            [136243, 2420071, 'Романов Арсений Витальевич'],
            [136255, 2420072, 'Сальников Егор Сергеевич'],
            [135720, 2420073, 'Семенова Алина Александровна'],
            [135775, 2420074, 'Серушков Платон Игоревич'],
            [135030, 2420191, 'Смирнов Иван Николаевич'],
            [136259, 2420075, 'Сырцев Петр'],
            [136186, 2420076, 'Утниченко Михаил Максимович'],
            [135973, 2420077, 'Фещенко Никита Евгеньевич'],
            [132686, 2420192, 'Филиппов Иван Дмитриевич'],
            [136239, 2420078, 'Чупраков Даниил Юрьевич'],
            [135995, 2420079, 'Шейда Олег Игоревич'])

isu_dict = {item[1]: [item[0], item[2]] for item in isu_list}
# print(*isu_dict.items())

# print(list(isu_dict.items()))

def user_shell():
    global isu_dict
    print('To find exact person, you have to enter ether isu ID or passbook number', end='')
    while ans := input(':\n>>> '):
        if ans.isdigit():
            if len(ans) == 7:
                if int(ans) in isu_dict.keys():
                    print(isu_dict.get(int(ans)))
                else:
                    print('Incorrect passbook number, try again', end='')
            elif len(ans) == 6:
                for i in range(len(isu_dict.items())):
                    if int(ans) == list(isu_dict.items())[i][1][0]:
                        print(list(isu_dict.items())[i][0], list(isu_dict.items())[i][1][0],
                              list(isu_dict.items())[i][1][1])
                if not any(int(ans) == list(isu_dict.items())[i][1][0] for i in range(len(isu_dict.items()))):
                    print('Incorrect isu ID, try again', end='')
            elif ans.isdigit():
                print('Incorrect length, ID has 6 chars and passbook number has 7 chars', end='')
            elif all(1072 <= ord(word.lower()) <= 1103 for word in ans.split()):
                pass
        elif ans == '':
            break
    print('Thanks for using my project.')


user_shell()
