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


def kb_completion_rules(max_n):
    rules = []
    for n in range(1, max_n + 1):
        left = "G" + "F" * n + "G"
        right = "G" + "F" * (n + 1)
        rules.append((left, right))
    return rules


def generator(rules):
    result = ''
    left_parts = [rule[0] for rule in rules]
    right_parts = [rule[1] for rule in rules]
    for i in range (0, random.randint(1,5)): 
        random_left = random.choice(left_parts) 
        if random.randint(0,1) == 1:
            random_right = random.choice(right_parts)
            result += random_right
        result += random_left
    return result


def invariant_q_count(word):
    return word.count('Q')


def invariant_parity_linear_1(word):
    A = word.count('A')
    B = word.count('B')
    C = word.count('C')
    D = word.count('D')
    J = word.count('J')
    return (A + B + C + D + J) % 2


def check_invariants(w, w_Strich):
    results = {}
    
    # 1 инвариант количество Q сохраняется
    q_count_w = invariant_q_count(w)
    q_count_w_Strich = invariant_q_count(w_Strich)
    if q_count_w == q_count_w_Strich:
        results['q_count'] = True
    else: 
        results['q_count'] = False
       
    # 2 сумма чисел всегда остается чётной или нечётной A, B, C, D и J 
    if (invariant_parity_linear_1(w) == invariant_parity_linear_1(w_Strich)):
        results['summ_latters'] = True
    else:
        results['summ_latters'] = False
    return results


def metamorphic_test_single_word(word, rules):
    for step in range(3):
        transitions, _ = generate_all_transitions(word, rules)
        if not transitions:
            return True 
        next_transition = random.choice(transitions)
        next_word = next_transition[1]
        print("Шаг " + str(step + 1) + ": " + word + " -> " + next_word + " (" + next_transition[2] + ")")
        results = check_invariants(word, next_word)

        if any(v is False for v in results.values()):
            return False  

        word = next_word

    return True 


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
    
    print("Инварианты для тестирования:")
    print("1 количество символов Q неизменно")
    print("2 сумма чисел всегда остается чётной или нечётной")

    a = int(input("Введите количество тестов: "))
    counter = []
    for i in range(a): 
        w = generator(rules)
        print("№: ", i)  
        print("тестовое слово:", w)
        
        results = metamorphic_test_single_word(w, rules2)
        
        if results:
            print("Инварианты сохранились!")
        else: 
            print("что-то пошло не так")
            counter.append(i)

    if counter != []:
        print("Ошибка!")
    else:
        print("Ок")


if __name__ == "__main__":
    main()