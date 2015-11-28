# Deterministic Finite Automata

class Dfa(object):

    def __init__(self, states, alphabet, delta, start, final):
        """
        :type states: set
        :type alphabet: set
        :type delta: set of tuple
        :type start: str
        :type final: set
        """
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start = start
        self.final = final

    def is_dfa(self):
        """
        by definition somewhere, dfa is characterized by its transition function, where each state only has outcoming
        transition reading exactly one of every symbol in alphabet. Even the transition goes to dead state.
        Considering that dead state doesn't necessarily appear.
        :rtype: bool
        """
        # later this function should be set to private, and is used to ensure validity of the instance of this class?

        set_symbols = set([])
        for state in self.states:
            for trans in self.delta:
                if state == trans[0]:
                    if trans[1] not in set_symbols:
                        set_symbols.add(trans[1])
                    else:
                        return False
            set_symbols.clear()
        else:
            return True

    def print_out(self):
        """
        to display the component of automata   
        """
        
        print "States = ",
        for q in self.states:
            print q,

        print ""

        print "Alphabet = ",
        for a in self.alphabet:
            print a,

        print ""

        print "Start state = ", self.start

        print "Final state = ",
        for q in self.final:
            print q,

        print ""

        print "Transition = "
        for d in self.delta:  # it was OK even when I forgot to ignore keyword self. why?
            print "(",
            for el in d:
                print el,
            print ")"

    def delta_function(self, state, symbol):
        """
        what state is now when you are from a state and reading a symbol.
        :param state: str
        :param symbol: str
        :rtype: str
        """
        
        for d in self.delta:
            if d[0] == state and d[1] == symbol:
                return d[2]
        else:
            return 's' 


    def is_accepted(self, word):
        """
        to check whether a given word is recognized (accepted) by the language or not. Recognized means
        the word is a member of language formed by the automata
        :param word: str
        :rtype: bool
        """
        
        current_state = self.start
        for symbol in range(0,len(word)):
            next_state = self.delta_function(current_state, word[symbol])
            if next_state == 's':
                return False
            else:
                current_state = next_state
                symbol += 1
        else:
            for q in self.final:
                if current_state == q:
                    return True
                    break
            else:
                return False


    def complement(self):
        """
        by definition somewhere, the complement of dfa can be obtained by changing all its non final states to
        final states and vice versa
        :rtype: Dfa
        """
        
        final = self.states.difference(self.final)
        return Dfa(self.states, self.alphabet, self.delta, self.start, final)
        
    def intersection(self, automata):
        """

        :param automata: Dfa
        :rtype: Dfa
        """
        return self.__bin_op(self, automata, 'and')

    def union(self, automata):
        """

        :param automata: Dfa
        :rtype: Dfa
        """
        return self.__bin_op(self, automata, 'or')

    def set_difference(self, automata):
        """

        :param automata: Dfa
        :rtype: Dfa
        """
        return self.__bin_op(self, automata, 'min')

    def sym_difference(self, automata):
        """

        :param automata: Dfa
        :rtype: Dfa
        """
        return self.__bin_op(self, automata, 'xor')

    def __bin_op(self, a1, a2, op):
        """
        this function is used by union, intersection, difference, and symmetric different operations. That because they
        differ only on how to determine the final states.
        :param a1: Dfa
        :param a2: Dfa
        :param op: str
        :rtype: Dfa
        """
        
        alphabet = a1.alphabet.copy()
        states = set([])
        final = set([])
        start = (a1.start, a2.start)
        delta = set([])
        working_list = set((start,))
        # interesting above is how to initialize a set of tuples with one member (a single tuple). be careful!
        while working_list != set([]):
            pick = working_list.pop()
            states.add(pick)
            if op == 'and':
                if pick[0] in a1.final and pick[1] in a2.final:
                    final.add(pick)
            elif op == 'or':
                if pick[0] in a1.final or pick[1] in a2.final:
                    final.add(pick)
            elif op == 'min':
                if pick[0] in a1.final and pick[1] not in a2.final:
                    final.add(pick)
            elif op == 'xor':
                if (pick[0] in a1.final and pick[1] not in a2.final) or (pick[0] not in a1.final and pick[1] in a2.final):
                    final.add(pick)

            for symbol in alphabet:
                q1 = a1.delta_function(pick[0], symbol)
                q2 = a2.delta_function(pick[1], symbol)
                if (q1,q2) not in states:
                    working_list.add((q1,q2))
                delta.add((pick, symbol, (q1,q2)))
        return Dfa(states, alphabet, delta, start, final)

    def is_universal(self):
        """
        dfa is universal if all states are final state, excluding unreachable states. as for dead state?? should be yes!
        then it need to check if dfa has 'complete' transition.
        :rtype: bool
        """
        
        reachable = set([])
        for state in self.states:
            if self.is_reachable(state):
                reachable.add(state)
        if reachable.difference(self.final) == set([]):
            return True
        else:
            return False

    def is_empty(self):
        """
        dfa is empty if there is no final state, excluding unreachable states.
        doesn't need to check the dead state. the dead state doesn't appear means it is not a final state.
        :rtype: bool
        """
        
        if self.final == set([]):
            return True
        else:
            for state in self.final:
                if self.is_reachable(state):
                    return False
                else:
                    continue
            else:
                return True

    # TODO
    def is_included(self, automata):
        """

        :param automata: Dfa
        :rtype: bool
        """
        pass

    # TODO
    def is_equal(self, automata):
        """

        :param automata: Dfa
        :rtype: bool
        """
        pass

    def is_reachable(self, state):
        """
        reachable state means that such state can be reached from start state by running some transition
        :param state: str
        :rtype: bool
        """
        working_list = set([state])
        # print working list
        if state == self.start:
            return True
            
        while working_list != ([]):
            previous_states = set([])
            current_state = working_list.pop()
            # print current_state
            for symbol in self.alphabet:
                temp = set(states for states in self.states if self.delta_function(states, symbol) == current_state)
                previous_states = previous_states.union(temp)
            previous_states.discard('s')
            # print "previous states to", current_state, "=", previous_states
            if previous_states == set([]) or previous_states == set([state]):
                return False
            else:
                working_list = working_list.union(previous_states)
                # print "all states reach", state, "=", working_list
                working_list.discard(current_state)
                if self.start in working_list:
                    return True

    def minimize_by_hopcroft(self):
        """
        Hopcroft algorithm to minimize this DFA
        :rtype: Dfa
        """
        
        final = self.final
        not_final = self.states.difference(self.final)
        partition = {tuple(final), tuple(not_final)}  # ->set of tuples, ideally set of sets but it is not allowed
        # ->initializing working_list
        if len(final) <= len(not_final):
            # ->{((),''),((),''),..} --> use .pop to empty the set
            working_list = set((tuple(final),y) for y in self.alphabet)
            print "initial working_list= ",working_list
            
        else:
            working_list = set((tuple(not_final),y) for y in self.alphabet)
            print "initial working_list= ",working_list

        print "----------------------------------------------"

        while working_list != set([]):
            splitter = working_list.pop()
            print "partition= ",partition
            print "splitter= ",splitter
            split_state = self.__split(splitter, partition)
            print "split_state =  ", split_state
            working_list.discard(splitter)  # ->it raised KeyError when using .remove(el)
            
            partition_copy = partition.copy()
                    
            for apart in partition_copy:
                one_part = ()
                other_part = ()
                for x in split_state:
                    if x in apart:
                        one_part += (x,)

                other_part = tuple(x for x in apart if x not in one_part)
                print "one_part = ", one_part
                print "other_part = ", other_part
                        
                # #update partition, if one apart is affected
                if one_part != () and other_part != ():
                    partition.discard(apart)
                    partition.add(one_part)
                    partition.add(other_part)

                    # #update working_list
                    for symbol in self.alphabet:
                        if (apart, symbol) in working_list:
                            working_list.discard((apart,symbol))
                            working_list.add((one_part,symbol))
                            working_list.add((other_part,symbol))
                        else:
                            working_list.add((one_part,symbol))
                    
            print "partition after once split = ", partition
            print "working_list after once split = ", working_list
            print "----------------------------------------------"

        # #establish the resulted minimum automata
        new_alphabet = self.alphabet
        new_states = set([])
        new_start = self.start
        new_final = self.final
        new_delta = self.delta
        partition_copy = partition.copy()
        new_delta_copy = new_delta.copy()
        for tup_of_states in partition_copy:
            if len(tup_of_states) > 1:
                temp = tup_of_states[0]+"*"
                if self.start in tup_of_states:
                    new_start = temp
                if self.final.intersection(set(tup_of_states)) != set([]):
                    new_final.difference_update(set(tup_of_states))
                    new_final.add(temp)
                for tup in new_delta_copy:
                    if tup[0] in tup_of_states:
                        new_delta.discard(tup)
                        new_delta.add((temp,tup[1],tup[2]))
                    if tup[2] in tup_of_states:
                        new_delta.discard(tup)
                        new_delta.add((tup[0],tup[1],temp))
                tup_of_states = (temp,)
                
            for state in tup_of_states:
                new_states.add(state)

        return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)

    def __split(self, splitter, partition):
        """
        this function is used by hopcroft algorithm, that is introducing the function to split partition,
        given both set of states and symbol incoming to them.
        :param splitter: str
        :param partition: set
        :rtype: tuple
        """
        
        split_state = ()  # tuple
        for apart in partition:  # apart is tuple, partition is set
            split_state += tuple(x for x in apart if self.delta_function(x,splitter[1]) in splitter[0])
        return split_state

    
    def minimize_by_moore(self):
        """
        the idea is using complete graph (states as nodes) as starting step. Then mark all edges between final and
        non-final nodes. As long as there exist marked edges, repeat the following step. Choose (arbitrarily) a marked
        edge (p',q'). Mark all unmarked edges (p,q) where (p.a, q.a) = (p',q') for some a in alphabet.
        :rtype: Dfa
        """
        complete_graph = set([])
        states = self.states.copy()
        while states != set([]):
            a_state = states.pop()
            for state in states:
                complete_graph.add((a_state, state))
        print complete_graph
        
        final = self.final
        not_final = self.states.difference(self.final)
        marked = set(tup for tup in complete_graph if tup[0] in final and tup[1] in not_final or tup[0] in not_final and
                     tup[1] in final)
        unmarked = complete_graph.difference(marked)
        unmarked_copy = unmarked.copy()
        while marked != set([]):
            a_marked = marked.pop()
            for tup in unmarked_copy:
                for symbol in self.alphabet:
                    if self.delta_function(tup[0], symbol) == a_marked[0] and \
                                    self.delta_function(tup[1], symbol) == a_marked[1] or \
                                            self.delta_function(tup[0], symbol) == a_marked[1] and \
                                            self.delta_function(tup[1], symbol) == a_marked[0]:
                        marked.discard(a_marked)
                        marked.add(tup)
                        unmarked.discard(tup)
                        break

        # establish new dfa
        new_alphabet = self.alphabet
        new_states = self.states
        new_delta = self.delta
        new_start = self.start
        new_final = self.final
        if unmarked == set([]):
            return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)
        else:
            temp = set([])
            unmarked_copy = unmarked.copy()
            for tup in unmarked:  # unmarked might contain more than one edges
                unmarked_copy.discard(tup)
                for tup2 in unmarked_copy:
                    if tup2[0] in tup:
                        if tup2[1] in tup:
                            temp.add(tup)
                        else:
                            temp.add(tup + tup2[1])
                    else:
                        if tup2[1] in tup:
                            temp.add(tup + tup2[0])
                        else:
                            temp.add(tup)  # may be true

            if new_start in temp:
                new_start =+"*"
            if new_final.intersection(temp) != set([]):
                temp2 = new_final.intersection(temp)
                new_final.difference_update(temp2)
                new_final_state = temp2.pop()+"*"
                new_final.add(new_final_state)
                new_states = new_states.difference(temp2)
            new_states = new_states.difference(temp)
            new_states.add(new_start)
            new_states = new_states.union(new_final)

            # next: new delta
            new_delta_copy = new_delta.copy()
            for tup in new_delta_copy:
                if tup[0] or tup[2] in temp:
                    pass
            return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)

    def minimize_by_brzozowski(self):
        """

        :rtype: Dfa
        """
        pass
        
    def convert_to_regex(self):
        """
        our regular expression will only need symbols in alphabet, operator +, *,concatenation that has no shape,
        and parentheses to against priority.(* > . > +)
        :rtype: str
        """

        regex = ''
        working_list = set([])
        for tup in self.delta:
            if tup[0] == tup[2]:
                regex += tup[1], '*'
            else:
                regex += tup[1]

