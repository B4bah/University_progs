from random import randint

num = str(randint(1000, 9999))
print(num)
print('Try to guess a four-digit number')
user_ans = ''

while user_ans != num:
    user_ans = input('Type your guess:\n>>> ')
    if len(user_ans) != 4:
        user_ans = input('Incorrect length, try again:\n>>> ')
    for i in range(len(user_ans)):
        if user_ans[i] in num:
            if num[i] == user_ans[i]:
                print(user_ans[i], ': green', sep='')
            elif num.count(user_ans[i]) >= user_ans.count(user_ans[i]) or num.count(user_ans[i]) == 1:
                print(user_ans[i], ': yellow', sep='')
            else:
q
                print(user_ans[i], ': gray', sep='')
        else:
            print(user_ans[i], ': gray', sep='')
print('Well done! My number was', num)