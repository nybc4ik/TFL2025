import re
import random

# рандомно сгенерировать слово не получится, важно заранее знать принадлежит оно языку или нет поэтому будет два генератора по патернам 
# пока шаблон с дефолтной (нет) генерацией рандомных слов лол... 


def in_language():
    word = ''
    alphabet = ['a', 'b', 'c']
    length = random.randint(0, 100)
    for i in range(length):
        word += random.choice(alphabet)
    return word


def not_in_language():
    word = ''
    alphabet = ['a', 'b', 'c']
    length = random.randint(0, 100)
    for i in range(length):
        word += random.choice(alphabet)
    return word


def generate_tests(count):
    words_in  = []
    words_out  = []
    for i in range(count):
        words_in.append(in_language())
        words_out .append(not_in_language())
    return words_in, words_out 


def test_equivalence(reg1, reg2):   
    in_language, not_in_language = [], [] 
    in_language, not_in_language = generate_tests(100)

    # проверка принадлежащих слов 
    for word in in_language:
        if bool(re.fullmatch(reg1, word)) != bool(re.fullmatch(reg2, word)):
            print(f"Различие на слове '{word}'")
            return False
    
    # проверка не принадлежащих слов 
    for word in not_in_language:
        if bool(re.fullmatch(reg1, word)) != bool(re.fullmatch(reg2, word)):
            print(f"Различие на слове '{word}'")
            return False
    return True


def main():
    reg1 = r'^((?:a|b)*)((?:a|b)*)c(?=\1(\1|\2)+$)\2(\1|\2)+$'
    reg2 = r'^((?:a|b)*)((?:a|b)*)c(?=\1(\1|\2)+$)\2(\1|\2)+$'

    mode = int(input())
    if mode == 1:
        if not test_equivalence(reg1, reg2):
            print("Не эквиваленты")
        else:
            print("Всё сошлось")


main()