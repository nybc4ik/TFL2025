from graphviz import Digraph

'''
((aa|bb)*(ab|ba)(aa|bb)*(ab|ba))*(ab|(bc|cb)(bb)*(cb|bc))*
'''

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
    'q16': {'c': 'q10'},
}
start_state = 'q0'
final_states = {'q0', 'q3', 'q15'}


def check_dfa(dfa, word, start_state, final_states):
    current_state = start_state 
    for symbol in word:     
        if symbol in dfa[current_state]:
            current_state = dfa[current_state][symbol]
        else:
            return False  
    return current_state in final_states


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


def tests():
    test_words = [
        ("aabbb", False),
        ("abb", False),
        ("aababbab", True),
        ("bcbbcbababbccb", True)
    ]

    for word, expected in test_words:
        result = check_dfa(dfa, word, start_state, final_states)
        if result:
            print(word + ": True (ожидалось: " + str(expected) + ")")
        else:
            print(word + ": False (ожидалось: " + str(expected) + ")")


tests()
dot = visualize_dfa(dfa, start_state, final_states)
dot.render('dfa_visualization', format='svg', cleanup=True)
print("Файл 'dfa_visualization.png'")

