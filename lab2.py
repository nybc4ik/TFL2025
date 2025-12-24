import random
import re
from graphviz import Digraph


# Блок с регулярным выражением
def generate_random_word(alphabet):
    word  = ''   
    length = random.randint(0, 10)
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


def check_dfa(word):
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
        'q11': {'a': 'q14', 'b': 'q12', 'c': 'q15'},
        'q12': {'a': 'q5', 'b': 'q13', 'c': 'q16'},
        'q13': {'a': 'q3', 'b': 'q17'},
        'q14': {'a': 'q5', 'b': 'q10'},
        'q15': {'b': 'q16'},
        'q16': {'b': 'q18', 'c': 'q19'},
        'q17': {'b': 'q13'},
        'q18': {'b': 'q16', 'c': 'q20'},
        'q19': {'b': 'q20'},
        'q20': {'a': 'q21', 'b': 'q22', 'c': 'q15'},
        'q21': {'b': 'q20'},
        'q22': {'c': 'q16'}
    }
    start_state = 'q0'
    final_states = {'q0', 'q10', 'q11', 'q20'}

    
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
    for i in range(num_tests):
        print("Тест №", i+1)
        word = generate_random_word(alphabet)
        regex_result = check_regex(regex, word)
        dfa_result = check_dfa(word)
        #nfa_result = check_nfa(word) 
        #pka_result = check_pka(word) 
        #if not (regex_result == dfa_result == nfa_result == pka_result):
        if regex_result != dfa_result:
            print(f"Ошибка в слове: {word}")
            print(f"Регулярка: {regex_result}, DFA: {dfa_result}")
            return False
        print(f"Слово: {word}, Результат: {regex_result}")
    return True

def main():
    regex = '((aa|bb)*(ab|ba)(aa|bb)*(ab|ba))*(ab|(bc|cb)(bb)*(cb|bc))*'
    alphabet = ['a', 'b', 'c']
    failed_tests = []
    count = int(input("Введите количество тестов: "))
    if test_equivalence(regex, alphabet, count): 
        print("Все тесты успешны!")
    else:

        print("Ошибка!")
        failed_tests.append(regex)
    print(check_dfa("ab"))
    print("список ошибочных тестов", failed_tests)


main()
