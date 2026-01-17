import random
import re
from graphviz import Digraph


# Блок с регулярным выражением
def generate_random_word(alphabet):
    word = ''   
    length = random.randint(0, 100)
    for i in range(length):
        word += random.choice(alphabet)
    return word


def check_regex(regex, word):
    return bool(re.fullmatch(regex, word))


# Блок с отрисовкой автомата
def visualize_automaton(automaton, start_state, final_states, automaton_type):
    dot = Digraph()
    dot.attr(rankdir='LR', size='10,0')

    for state in automaton:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')

    dot.node('start', shape='none', label='')
    dot.edge('start', start_state)

    for state, transitions in automaton.items():
        for symbol, next_states in transitions.items():
            if isinstance(next_states, str):
                next_states = {next_states}
            for next_state in next_states:
                dot.edge(state, next_state, label=symbol)

    filename = f"{automaton_type}_visualization"
    dot.render(filename, format='svg', cleanup=True)
    print(filename + ".svg")


# Блок с DFA (отрисовка генерация проверка)
def check_dfa(word, visualize=False):
    dfa = {
        'q0': {'a': 'q1', 'b': 'q2', 'c': 'q9'},
        'q1': {'a': 'q4', 'b': 'q3'},
        'q2': {'a': 'q11', 'b': 'q4', 'c': 'q10'},
        'q3': {'a': 'q7', 'b': 'q5', 'c': 'q9'},
        'q4': {'a': 'q6', 'b': 'q8'},
        'q5': {'a': 'q0', 'b': 'q11', 'c': 'q10'},
        'q6': {'a': 'q4', 'b': 'q11'},
        'q7': {'a': 'q11', 'b': 'q0'},
        'q8': {'a': 'q11', 'b': 'q4'},
        'q9': {'b': 'q10'},
        'q10': {'b': 'q13', 'c': 'q14'},
        'q11': {'a': 'q7', 'b': 'q12'},
        'q12': {'a': 'q0', 'b': 'q11'},
        'q13': {'b': 'q10', 'c': 'q15'},
        'q14': {'b': 'q15'},
        'q15': {'a': 'q14', 'b': 'q16', 'c': 'q9'},
        'q16': {'c': 'q10'}
    }
    start_state = 'q0'
    final_states = {'q0', 'q3', 'q15'}

    if visualize:
        visualize_automaton(dfa, start_state, final_states, "DFA") 

    current_state = start_state 
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


# Блок с NFA (отрисовка, генерация, проверка)
def get_epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if 'ε' in nfa.get(state, {}):
            for next_state in nfa[state]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure

def check_nfa(word, visualize=False):
    nfa = {
    'q0': {'ε': {'q1', 'q7'}},
    'q1': {'a': 'q2', 'b': 'q4'},
    'q2': {'a': 'q1', 'b': 'q3'},
    'q4': {'a': 'q3', 'b': 'q1'},
    'q3': {'a': 'q5', 'b': 'q6'},
    'q5': {'a': 'q3', 'b': 'q0'},
    'q6': {'a': 'q0', 'b': 'q3'},
    'q7': {'a': 'q8', 'b': 'q9', 'c': 'q11'},
    'q8': {'b': 'q7'},
    'q9': {'c': 'q10'},
    'q10': {'b': {'q11', 'q12'}, 'c': 'q8'},
    'q11': {'b': 'q10'},
    'q12': {'c': 'q7'}
    }
    nfa_start_state = 'q0'
    nfa_final_states = {'q7'}

    if visualize:
        visualize_automaton(nfa, nfa_start_state, nfa_final_states, "NFA")


    current_states = get_epsilon_closure(nfa, {nfa_start_state})

    for symbol in word:
        next_states = set()
        for state in current_states:
            if symbol in nfa.get(state, {}):
                transitions = nfa[state][symbol]
                if isinstance(transitions, str):
                    next_states.add(transitions)
                else:
                    next_states.update(transitions)
        current_states = get_epsilon_closure(nfa, next_states)
        if not current_states:
            return False
    return any(state in nfa_final_states for state in current_states)


## Дополнительные автоматы для ПКА 
# 1 количество букв с тоже должно быть чётным 
def dfa_c_count(word):
    dfa = {
        'C0': {'a': 'C0', 'b': 'C0', 'c': 'C1'},
        'C1': {'a': 'C1', 'b': 'C1', 'c': 'C0'}
    }
    start_state = 'C0'      
    final_states = {'C0'}

    current_state = start_state
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


# 2 чётная длина всего слова 
def dfa_count(word):
    dfa = {
        'Q0': {'a': 'Q1', 'b': 'Q1', 'c': 'Q1'},
        'Q1': {'a': 'Q0', 'b': 'Q0', 'c': 'Q0'}
    }
    start_state = 'Q0'      
    final_states = {'Q0'}

    current_state = start_state
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states
    

# 3 хотя бы одна буква б
def dfa_has_b(word):
    dfa = {
        'B0': {'a': 'B1', 'b': 'B2', 'c': 'B1'},
        'B1': {'a': 'B1', 'b': 'B2', 'c': 'B1'},
        'B2': {'a': 'B2', 'b': 'B2', 'c': 'B2'}
    }
    start_state = 'B0'      
    final_states = {'B0', 'B2'}

    current_state = start_state
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


# 4 после с не может идти а 
def dfa_no_c_a(word):
    dfa = {
        'AC0': {'a': 'AC0', 'b': 'AC0', 'c': 'AC1'},
        'AC1': {'a': 'AC2', 'b': 'AC1', 'c': 'AC1'},
        'AC2': {'a': 'AC3', 'b': 'AC1', 'c': 'AC3'},
        'AC3': {'a': 'AC3', 'b': 'AC3', 'c': 'AC3'}
    }
    start_state = 'AC0'      
    final_states = {'AC0', 'AC1'}

    current_state = start_state
    for symbol in word:
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


# Блок с SFA - ПКА (отрисовка, генерация, проверка) 
def check_sfa(word, visualize = False):
    dfa_ok = check_dfa(word, visualize=False)
    c_count_ok = dfa_c_count(word)
    even_length_ok = dfa_count(word)
    has_b_ok = dfa_has_b(word)
    no_c_a_ok = dfa_no_c_a(word)
    if visualize:
        visualize_automaton_SFA()
    return dfa_ok and c_count_ok and even_length_ok and has_b_ok and no_c_a_ok


# отрисовка ПКА 
def visualize_automaton_SFA():
    sfa_automaton = {}
    start_sfa = 'start_sfa'
    # основной автомат
    dfa = {
        'q0': {'a': 'q1', 'b': 'q2', 'c': 'q9'},
        'q1': {'a': 'q4', 'b': 'q3'},
        'q2': {'a': 'q11', 'b': 'q4', 'c': 'q10'},
        'q3': {'a': 'q7', 'b': 'q5', 'c': 'q9'},
        'q4': {'a': 'q6', 'b': 'q8'},
        'q5': {'a': 'q0', 'b': 'q11', 'c': 'q10'},
        'q6': {'a': 'q4', 'b': 'q11'},
        'q7': {'a': 'q11', 'b': 'q0'},
        'q8': {'a': 'q11', 'b': 'q4'},
        'q9': {'b': 'q10'},
        'q10': {'b': 'q13', 'c': 'q14'},
        'q11': {'a': 'q7', 'b': 'q12'},
        'q12': {'a': 'q0', 'b': 'q11'},
        'q13': {'b': 'q10', 'c': 'q15'},
        'q14': {'b': 'q15'},
        'q15': {'a': 'q14', 'b': 'q16', 'c': 'q9'},
        'q16': {'c': 'q10'}
    }
    sfa_automaton.update(dfa)

    dfa_c_count = {
        'C0': {'c': 'C1', 'a, b': 'C0'},
        'C1': {'c': 'C0', 'a, b': 'C1'}
    }
    sfa_automaton.update(dfa_c_count)

    dfa_count = {
        'Q0': {'a, b, c': 'Q1'},
        'Q1': {'a, b, c': 'Q0'}
    }
    sfa_automaton.update(dfa_count)

    dfa_has_b = {
        'B0': {'a, c': 'B1', 'b': 'B2'},
        'B1': {'a, c': 'B1', 'b': 'B2'},
        'B2': {'a, b, c': 'B2'}
    }
    sfa_automaton.update(dfa_has_b)

    dfa_no_c_a = {
        'AC0': {'a, b': 'AC0', 'c': 'AC1'},
        'AC1': {'a': 'AC2', 'b, c': 'AC1'},
        'AC2': {'a, c': 'AC3', 'b': 'AC1'},
        'AC3': {'a, b, c': 'AC3'}
    }
    sfa_automaton.update(dfa_no_c_a)

    # переходы из самого начального состояния 
    sfa_automaton[start_sfa] = {'ε': {'q0', 'C0', 'Q0', 'B0', 'AC0'}}

    # финальные состояния ПКА
    final_states = {
        'q0', 'q3', 'q15',  
        'C0',               
        'Q0',               
        'B0', 'B2',              
        'AC0', 'AC1'        
    }
    visualize_automaton(sfa_automaton, start_sfa, final_states, "SFA")


# Блок с расширенным регулярным выражением
def check_extended_regex(word):
    extended_regex = r"""
    ^(
    (
    ((aa)?(bb)?)+
        (	((?=(ab))[^c][^c])
        |
        ((?=(ba))[^c][^c])
        )
    ((aa)?(bb)?)+
        (	([^c][^c](?<=(ab)))
        |
        ([^c][^c](?<=(ba)))
        )
    )?
    )+(
    (
        ((?=ab)[^c][^c])
        |
        ( (((?=(bc))[^a][^a])
        |
        ((?=(cb))[^a][^a])
        )
        ((bb)?)+
        ( ([^a][^a](?<=(bc)))
        |
        ([^a][^a](?<=(cb)))
        )
    )
    )? 
    )+$
    """
    return bool(re.fullmatch(extended_regex, word)) 


def test_equivalence(regex, alphabet, num_tests=100):
    failed_words = [] 
    for i in range(num_tests):
        word = generate_random_word(alphabet)
        regex_result = check_regex(regex, word)
        dfa_result = check_dfa(word)
        nfa_result = check_nfa(word) 
        sfa_result = check_sfa(word) 
        extended_regex_result = check_extended_regex(word)
        if not (regex_result == dfa_result == nfa_result == sfa_result == extended_regex_result):
            print("Ошибка в слове:", word)
            print("Регулярка:", regex_result, "DFA:", dfa_result, "NFA:", nfa_result, "ПКА:", sfa_result, "Расширенная регулярка:", extended_regex_result)
            failed_words.append(word)   
    if failed_words == []:
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
        nfa_result = check_nfa(word)
        sfa_result = check_sfa(word) 
        extended_regex_result = check_extended_regex(word)
        print("Слово:", word)
        print("Регулярка:", regex_result)
        print("DFA:", dfa_result)
        print("NFA:", nfa_result)
        print("ПКА:", sfa_result)
        print("Расширенная регулярка:", extended_regex_result)
        if (regex_result == dfa_result == nfa_result == sfa_result == extended_regex_result): 
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
            dfa_result = check_dfa(word)
            nfa_result = check_nfa(word)
            sfa_result = check_sfa(word)
            extended_regex_result = check_extended_regex(word)
            if not (regex_result == dfa_result == nfa_result == sfa_result == extended_regex_result):
                errors.append(word)
                print("Ошибка:", word, "- Регулярка:", regex_result, "DFA:", dfa_result, "NFA:", nfa_result, "ПКА:", sfa_result,"Расширенная регулярка:", extended_regex_result)    
        if errors:
            print("\nВсего ошибок:", len(errors), "из", len(words))
        else:
            print("\nВсе", len(words), "слов прошли проверку")
    else:
        print("Неправильный выбор")

main()