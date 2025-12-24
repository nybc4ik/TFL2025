import random
import re
from graphviz import Digraph


# Блок с регулярным выражением
def generate_random_word(alphabet):
    word  = ''   
    length = random.randint(0, 100)
    for i in range(length):
        word += random.choice(alphabet)
    return word


def check_regex(regex, word):
    return bool(re.fullmatch(regex, word))


# Блок с DFA (отрисовка генерация проверка)
def visualize_dfa(dfa, start_state, final_states):
    dot = Digraph()
    dot.attr(rankdir='LR', size='10,0')

    for state in dfa:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')

    dot.node('start', shape='none', label='')
    dot.edge('start', start_state)

    for state, transitions in dfa.items():
        for symbol, next_state in transitions.items():
            dot.edge(state, next_state, label=symbol)

    return dot


def check_dfa(word, visualize=True):
    dfa = {
        'q0': {'a': 'q1', 'b': 'q12', 'c': 'q15'},
        'q1': {'a': 'q2', 'b': 'q11'},
        'q2': {'a': 'q3', 'b': 'q4'},
        'q3': {'a': 'q2', 'b': 'q5'},
        'q4': {'a': 'q5', 'b': 'q2'},
        'q5': {'a': 'q6', 'b': 'q7'},
        'q6': {'a': 'q8', 'b': 'q10'},
        'q7': {'a': 'q10', 'b': 'q9'},
        'q8': {'a': 'q6', 'b': 'q7'},
        'q9': {'a': 'q6', 'b': 'q7'},
        'q10': {'a': 'q1', 'b': 'q12', 'c': 'q15'},
        'q11': {'a': 'q14', 'b': 'q23', 'c': 'q15'},
        'q12': {'a': 'q5', 'b': 'q13', 'c': 'q16'},
        'q13': {'a': 'q3', 'b': 'q4'},
        'q14': {'a': 'q5', 'b': 'q10'},
        'q15': {'b': 'q16'},
        'q16': {'b': 'q18', 'c': 'q19'},
        #'q17': {'b': 'q13'},
        'q18': {'b': 'q16', 'c': 'q20'},
        'q19': {'b': 'q20'},
        'q20': {'a': 'q21', 'b': 'q22', 'c': 'q15'},
        'q21': {'b': 'q20'},
        'q22': {'c': 'q16'},
        'q23':{'a': 'q10', 'b':'q9', 'c':'q16'}
    }
    start_state = 'q0'
    final_states = {'q0', 'q10', 'q11', 'q20'}

    if visualize:
        dot = visualize_dfa(dfa, start_state, final_states)
        dot.render('dfa_visualization', format='svg', cleanup=True)
        print("Файл 'dfa_visualization.svg'")

    current_state = start_state 
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


def test_equivalence(regex, alphabet, num_tests=100):
    failed_words = [] 
    for i in range(num_tests):
        word = generate_random_word(alphabet)
        regex_result = check_regex(regex, word)
        dfa_result = check_dfa(word)
        #nfa_result = check_nfa(word) 
        #pka_result = check_pka(word) 
        #if not (regex_result == dfa_result == nfa_result == pka_result):
        if regex_result != dfa_result:
            print("Ошибка в слове:", word)
            print("Регулярка:", regex_result, "DFA:", dfa_result)
            failed_words.append(word)   
    if failed_words == [] :
        return True
    else:
        return failed_words 


def main():
    regex = '((aa|bb)*(ab|ba)(aa|bb)*(ab|ba))*(ab|(bc|cb)(bb)*(cb|bc))*'
    alphabet = ['a', 'b', 'c']
    print("1 - Автоматические тесты")
    print("2 - Ручное тестирование")
    print("3 - Тестирование из Error.txt")
    mode = input("Выберите режим: ")
    
    if mode == "1":
        count = int(input("Введите количество тестов: "))
        result = test_equivalence(regex, alphabet, count)  
        if result == True:  
            print("Все тесты успешны!")
        else:
            failed_words = result  
            print("Найдено", len(failed_words), "ошибок:")
            for word in failed_words:
                print(word)


    elif mode == "2":
        word = input("Введите слово для тестирования: ")    
        regex_result = check_regex(regex, word)
        dfa_result = check_dfa(word)
        print("Слово:", word)
        print("Регулярка:", regex_result)
        print("DFA:", dfa_result)
        if regex_result == dfa_result:
            print("Результаты совпадают")
        else:
            print("Результаты не совпадают!")

    elif mode =="3":
        with open("Error.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
                
            words = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("- "):
                    word = line[2:].strip()
                    if word:
                        words.append(word)
                elif " - " in line and line.startswith("  "):
                    parts = line.split(" - ")
                    if len(parts) > 1:
                        word = parts[1].strip()
                        if word:
                            words.append(word)
                else:
                    words.append(line)
                
            print(f"Найдено {len(words)} слов для тестирования")
                
        errors = []
        for word in words:
            regex_result = check_regex(regex, word)
            dfa_result = check_dfa(word, visualize=False)
            
            if regex_result != dfa_result:
                errors.append(word)
                print("Ошибка:", word, "- Регулярка:", regex_result, "DFA:", dfa_result)
            #else:
                #print(f"OK: '{word}'")
        if errors:
            print("\nВсего ошибок:", len(errors), "из", len(words))
        else:
            print("\nВсе", len(words), "слов прошли проверку")
    else:
        print("Неправильный выбор")

main()