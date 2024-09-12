from random import randint

num = str(randint(1000, 9999))  # Creating a random four-digit number
# print(num)
print("Try to guess a four-digit number.\nRules:\n"
      "1) If digit isn't in the target: gray.\n"
      "2) If it's in and it's on right place: green.\n"
      "3) If digit is in target, but not on the right place: yellow")
user_ans = ''  # A string of user input

while user_ans != num:
    user_ans = input('Type your guess:\n>>> ')
    if len(user_ans) != 4:
        user_ans = input('Incorrect length, try again:\n>>> ')
    for i in range(len(user_ans)):  # Iterating user answer digit by digit to check its correctness
        if user_ans[i] in num:
            if num[i] == user_ans[i]:
                print(f'{user_ans[i]}: green')
            elif num.count(user_ans[i]) >= user_ans.count(user_ans[i]) or user_ans.count(user_ans[i]) == 1:
                print(f'{user_ans[i]}: yellow')
            else:
                print(f'{user_ans[i]}: gray')
        else:
            print(f'{user_ans[i]}: gray')
print('Well done! My number was', num)