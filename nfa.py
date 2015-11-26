from types import *
from dfa import Dfa


class Nfa(object):
    def __init__(self, states, alphabet, delta, start, final):
        # states, alphabet, final are set of string.
        # delta is set of tuple
        # start is string
        assert type(states) is set, "%r is not a set" % states
        assert type(alphabet) is set, "%r is not a set" % alphabet
        assert type(delta) is set, "%r is not a set" % delta
        assert type(start) is StringType, "%r is not a string" % start
        assert type(final) is set, "%r is not a set" % final

        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start = start
        self.final = final

    def is_nfa(self):
        '''
        To check whether the instance is a correct NFA
        :return: boolean
        '''
        # assert isinstance(self.delta, set), "%r is not a set" % self.delta
        # delta_function = self.delta.copy()
        # noinspection PyCallByClass
        d = Dfa(self.states, self.alphabet, self.delta, self.start, self.final)
        if not (d.is_dfa()):
            return True
        else:
            return False

    def delta_function(self, state, symbol):
        '''What states are now when you are from a state and reading a symbol.'''

        next_states = set([])
        for d in self.delta:
            if d[0] == state and d[1] == symbol:
                next_states.add(d[2])
        if next_states == ([]):
            return {'s'}
        else:
            return next_states

    def is_accepted(self, word):

        '''Return true or false
        To check whether the given word is recognized by this NFA or not. Unlike those in DFA, NFA may need to backtrack.
        :param word:string
        :return:boolean
        '''

        current_state = self.start
        for symbol in range(0, len(word)):
            next_states = self.delta_function(current_state, word[symbol])
            for state in next_states:
                current_state = state
                if current_state == 's':
                    return False

    def convert_to_dfa(self):
        '''
        convert NFA to DFA, using subset construction
        :return:Dfa
        '''

        # initialize the components of DFA
        new_start = self.start
        new_alphabet = self.alphabet
        new_states = set([new_start])
        new_final = set([])
        new_delta = set([])

        # helping variables
        is_in_final = False
        is_not_existed = False
        new_state = ''
        state_to_states = {}  # to store a name of compound state and the states arrange it
        new_state_consists_of = set([])

        # start with the NFA's start state as a start state of DFA
        working_list = {new_start}
        state_to_states[new_start] = {new_start}

        # loop until we have all states transition to by reading exactly one of each symbol
        while working_list != set([]):
            current_state = working_list.pop()
            for symbol in self.alphabet:

                # states to where we go from the current state by reading the symbol.
                # the current state might be a compound state
                for state in state_to_states[current_state]:
                    new_state_consists_of = new_state_consists_of.union(self.delta_function(state, symbol))

                # to make set of states become readable as one state
                for state in new_state_consists_of:
                    new_state += state

                # add to new_delta
                new_delta.add((current_state, symbol, new_state))

                # CAUTION: it might happen that 2 'new_state_consists_of's resulting 2 different states although they
                # are actually the same. Ex: {'q2', 'q3'} -> 'q2q3' AND {'q3', 'q2'} -> 'q3q2'
                # Hence, we need to ensure that new_state_consists_of doesn't exist in new_states
                for key in state_to_states:
                    if state_to_states[key] == new_state_consists_of:
                        is_not_existed = False

                if is_not_existed:
                    for state in new_state_consists_of:
                        # if one of the states in NFA's set of states, then they will be added as a final state in DFA
                        if state in self.final:
                            is_in_final = True

                    # we need this when it becomes the current state and we have to find its transition
                    state_to_states[new_state] = new_state_consists_of

                    # add to new_states
                    new_states.add(new_state)

                    # add to final states if meet the conditions
                    if is_in_final:
                        new_final.add(new_state)
                        is_in_final = False

                    # finally, add new_state to working_list and remove the state that has just been proceeded
                    working_list.add(new_state)
                    is_not_existed = False
                    new_state = ''

            working_list.discard(current_state)

        return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)
