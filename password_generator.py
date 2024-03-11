import random
from random import randint


def generate_password(*, letters=True, symbols=False, numbers=False, duplicates=False, pass_length=8):
    """ Generates password
      letters
        whether to use uppercase letters, default True.
      symbols
        whether to use special symbols, default False.
      numbers
        whether to use numbers, default False.
      duplicates
        whether to use duplicates, default False.
      pass_length
        length of generated password, default 8.
    """
    if pass_length < 8:
        print("Password can't be less than 8 symbols!")
        return None
    result_list = []
    symbols_list = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']',
                    '^', '_', '`', '{', '}', '~']
    letters_list = list(map(chr, range(97, 123)))
    symbols_num = 0
    if symbols:
        if pass_length <= len(symbols_list):
            symbols_num = randint(1, pass_length // 3)
        else:
            symbols_num = randint(1, len(symbols_list) // 2)
    numbers_num = randint(1, pass_length // 3) if numbers else 0
    letters_num = pass_length - symbols_num - numbers_num
    lower_letters_num = randint(1, letters_num - 1)
    upper_letters_num = letters_num - lower_letters_num
    if not letters:
        lower_letters_num = letters_num
        upper_letters_num = 0

    if symbols_num > 0:
        for i in range(symbols_num):
            result_list.append(random.choice(symbols_list))
    if numbers_num > 0:
        for i in range(numbers_num):
            result_list.append(randint(0, 9))
    if upper_letters_num > 0:
        for i in range(upper_letters_num):
            result_list.append(str(random.choice(letters_list)).upper())
    if not duplicates:
        result_set = set(result_list)
        while len(result_set) < pass_length:
            result_set.add(random.choice(letters_list))
        result_list = list(result_set)
    else:
        for i in range(lower_letters_num):
            result_list.append(random.choice(letters_list))
        if len(set(result_list)) == len(result_list):
            for item in result_list:
                if str(item) in letters_list:
                    result_list.remove(item)
                    break
            index = randint(0, len(result_list) - 1)
            result_list.append(result_list[index])
    random.shuffle(result_list)
    if duplicates:
        for i in range(pass_length - 1):
            if result_list[i] == result_list[i + 1]:
                item = result_list[i]
                if i != pass_length - 2:
                    result_list.remove(item)
                    result_list.append(item)
                else:
                    for j in range(pass_length - 3):
                        if item != result_list[j] and item != result_list[j + 1]:
                            result_list.insert(item, j)
                            break
    return "".join([str(elem) for elem in result_list])
