from graphviz import Digraph

nfa = {
    'q0': {'ε': {'q1', 'q7'}},
    'q1': {'a': 'q2', 'b': 'q4'},
    'q2': {'a': 'q1', 'b': 'q3'},
    'q4': {'a': 'q3', 'b': 'q1'},
    'q3': {'a': 'q5', 'b': {'q6'}},
    'q5': {'a': 'q3', 'b': 'q0'},
    'q6': {'a': 'q0', 'b': 'q3'},
    'q7': {'a': 'q8', 'b': 'q9', 'c': 'q11'},
    'q8': {'b': 'q7'},
    'q9': {'c': 'q10'},
    'q10': {'b': 'q11', 'c': 'q8'},
    'q11': {'b': 'q10', 'c': 'q7'}
}

start_state = 'q0'
final_states = {'q7'}


def check_nfa(nfa, word, start_state, final_states):
    current_states = get_epsilon_closure(nfa, {start_state})

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
    return any(state in final_states for state in current_states)


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


def visualize_nfa(nfa, start_state, final_states):
    dot = Digraph()
    dot.attr(rankdir='LR', size='10,0')

    for state in nfa:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')

    dot.node('start', shape='none', label='')
    dot.edge('start', start_state)

    for state, transitions in nfa.items():
        for symbol, next_states in transitions.items():
            if isinstance(next_states, str):
                next_states = {next_states}
            for next_state in next_states:
                dot.edge(state, next_state, label=symbol)

    return dot


def tests():
    test_words = [
        ("aababbab", True),
        ("abb", False),
        ("bcbbcbababbccb", True),
        ("aabbb", False),
    ]

    for word, expected in test_words:
        result = check_nfa(nfa, word, start_state, final_states)
        print(f"{word}: {result} (ожидалось: {expected})")

tests()

dot = visualize_nfa(nfa, start_state, final_states)
dot.render('nfa_visualization', format='svg', cleanup=True)
print("Граф НКА сохранён в 'nfa_visualization.svg'")
