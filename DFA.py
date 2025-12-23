from graphviz import Digraph

'''
((aa|bb)*(ab|ba)(aa|bb)*(ab|ba))*(ab|(bc|cb)(bb)*(cb|bc))*
'''
dfa = {
    'q0': {'a': 'q1', 'b': 'q4', 'c': 'q10'}, 
    'q1': {'a': 'q2', 'b': 'q3'},
    'q2': {'a': 'q1', 'b': 'q4'},
    'q3': {'a': 'q6', 'b': 'q8', 'c': 'q10'}, 
    'q4': {'a': 'q3', 'b': 'q5', 'c': 'q11'},
    'q5': {'a': 'q1', 'b': 'q4'},
    'q6': {'a': 'q7', 'b': 'q0'},
    'q7': {'a': 'q6', 'b': 'q8'},
    'q8': {'a': 'q0', 'b': 'q9'},
    'q9': {'a': 'q6', 'b': 'q8'},
    'q10': {'b': 'q11'},
    'q11': {'b': 'q12', 'c': 'q13'},
    'q12': {'b': 'q11', 'c': 'q0'}, 
    'q13': {'b': 'q0'}
}
start_state = 'q0'
final_states = {'q0', 'q3'}


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
    dot.attr(rankdir='LR', size='8,5')

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
        ("aababbab", True)
    ]

    for word, expected in test_words:
        result = check_dfa(dfa, word, start_state, final_states)
        if result:
            print(word + ": True (ожидалось: " + str(expected) + ")")
        else:
            print(word + ": False (ожидалось: " + str(expected) + ")")


tests()
dot = visualize_dfa(dfa, start_state, final_states)
dot.render('dfa_visualization', format='png', cleanup=True)
print("Файл 'dfa_visualization.png'")

