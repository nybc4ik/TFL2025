import random
from collections import deque


def read_rewrite_system(filename):
    rules = []
    with open(filename, 'r', encoding='utf-8') as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue  
            if '->' not in line:
                continue  
            left, right = [part.strip() for part in line.split('->', 1)]
            if not left or not right:
                continue  
            rules.append((left, right))
    return rules


def collector(rules):
    arr = set() 
    for rule in rules: 
        for i in rule:
            if len(i) > 1:
                for char in i:
                    arr.add(char)
            else:
                arr.add(i)
    return arr


def generate_all_transitions(start_word, rules):
    visited = set()
    final_forms = set()
    transitions_acc = []
    queue = deque([start_word])
    
    while queue:
        current = queue.popleft()
        
        if current in visited:
            continue
        visited.add(current)
        
        has_transitions = False
        for left, right in rules:
            start = 0
            while True:
                pos = current.find(left, start)
                if pos == -1:
                    break
                new_word = current[:pos] + right + current[pos + len(left):]
                transitions_acc.append((current, new_word, f"{left} → {right} на позиции {pos+1}"))
                queue.append(new_word)
                start = pos + 1
                has_transitions = True
        
        if not has_transitions:
            final_forms.add(current)
    
    return transitions_acc, final_forms


def random_w_Strich(start, rules): # генерация w', w' не обязательно будет в НФ, ну тут я поставил от 1 до 10 переходов 
    transitions, forms = generate_all_transitions(start, rules)
    outs = {}
    for u, v, a in transitions:
        outs.setdefault(u, []).append(v) # ключ это строка, а значение- в которые можно перейти из неё 
    w = start
    steps = random.randint(1, 10)
    for _ in range(steps):
        neigh = outs.get(w, [])
        if not neigh:
            break
        w = random.choice(neigh)
    return w


def kb_completion_rules(max_n):
    rules = []
    for n in range(1, max_n + 1):
        left = "G" + "F" * n + "G"
        right = "G" + "F" * (n + 1)
        rules.append((left, right))
    return rules


def generator(rules):
    arr = collector(rules) # список всех уникальных символов (я не уверен, что это хорошая идея, пока закоменчу... рандомные символы в слове могут радомно НЕ переписывать его:( )
    result = ''
    left_parts = [rule[0] for rule in rules]
    for i in range (0, random.randint(1,3)): 
        random_left = random.choice(left_parts)
        # print("случайная левая часть", random_left)  
        result += random_left
    """  
        if (random.randint(1,2)/2)==1:
            print("а добавим ка мы символ")
            b = random.choice(list(arr))
            print(b)
            result += b
        else:
            print("или не добавим")"""
    return result


def main():
    filename = 'data.txt'
    filename2 = 'data2.txt'
    rules = read_rewrite_system(filename)
    rules2 = read_rewrite_system(filename2)
    rules2.extend(kb_completion_rules(10)) 

    print("Исходная система T:")
    print(rules)
    print("Система T':")
    print(rules2)

    a = int(input("Введите количество тестов: "))
    errors = []

    for i in range(a):
        w = generator(rules)
        print("w: ", w)

        w_Strich = random_w_Strich(w, rules)
        print("w': ", w_Strich)
        _, final_forms_w = generate_all_transitions(w, rules2) # нормальные формы для w
        print(final_forms_w)
        _, final_forms_wp = generate_all_transitions(w_Strich, rules2) # нормальные формы для w'
        print(final_forms_wp)
        intersection = final_forms_w.intersection(final_forms_wp) # пересечение НФ w и w' если есть -> всё получилось
        #print(intersection)
        if intersection:
            print("Проверка удалась! (пересечение: ", intersection,")")
        else:
            print("Проверка не удалась")
            errors.append((i, w, w_Strich))

    if not errors:
        print("\nВсе тесты успешны")
    else:
        print("\nНеуспешных тестов: ", len(errors))
        print("Список неуспешных тестов:")
        for number, w, w_Strich in errors:
            print("№", number, ":", w, "->", w_Strich)

if __name__ == "__main__":
    main() 
