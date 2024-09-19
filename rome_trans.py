def rome_trans(numb):
    rome_dict = {
        'i': 1,
        'v': 5,
        'x': 10,
        'l': 50,
        'c': 100,
        'd': 500,
        'm': 1000
    }
    result = 0
    if len(numb) == 1:
        return rome_dict.get(numb)
    else:
        i = 0
        while i < len(numb) - 1:
            if rome_dict.get(numb[i]) >= rome_dict.get(numb[i+1]):
                result += rome_dict.get(numb[i])
                i += 1
            else:
                result += rome_dict.get(numb[i+1]) - rome_dict.get(numb[i])
                i += 2
        if rome_dict.get(numb[-2]) >= rome_dict.get(numb[-1]):
            result += rome_dict.get(numb[-1])
        return result


while num := input('Enter a rome-number:\n>>> ').lower():
    print(rome_trans(num))