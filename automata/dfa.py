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

        # helping variable, to join compound state
        str = ""
        
        alphabet = a1.alphabet.copy()
        states = set([])
        final = set([])
        new_start_consists_of = (a1.start, a2.start)  # new start state is join of both automata's start state
        start = str.join(new_start_consists_of)
        delta = set([])
        working_list = set((new_start_consists_of,))
        # interesting above is how to initialize a set of tuples with one member (a single tuple). be careful!
        while working_list != set([]):
            pick = working_list.pop()

            # add current pick as a single string to new set of states
            states.add(str.join(pick))

            # depending on the operation, a new final state is chosen here
            if op == 'and':
                if pick[0] in a1.final and pick[1] in a2.final:
                    final.add(str.join(pick))
            elif op == 'or':
                if pick[0] in a1.final or pick[1] in a2.final:
                    final.add(str.join(pick))
            elif op == 'min':
                if pick[0] in a1.final and pick[1] not in a2.final:
                    final.add(str.join(pick))
            elif op == 'xor':
                if (pick[0] in a1.final and pick[1] not in a2.final) or (pick[0] not in a1.final and pick[1] in a2.final):
                    final.add(str.join(pick))

            # completing the transition function for each new state
            for symbol in alphabet:
                q1 = a1.delta_function(pick[0], symbol)
                q2 = a2.delta_function(pick[1], symbol)
                new_state_consists_of = (q1,q2)
                if str.join(new_state_consists_of) not in states:
                    working_list.add(new_state_consists_of)
                delta.add((str.join(pick), symbol, str.join(new_state_consists_of)))

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
        partition = {tuple(final), tuple(not_final)}  # set of tuples, ideally set of sets but it is not allowed

        # initializing working_list
        if len(final) <= len(not_final):
            working_list = set((tuple(final),y) for y in self.alphabet)
            # print "initial working_list= ",working_list
        else:
            working_list = set((tuple(not_final),y) for y in self.alphabet)
            # print "initial working_list= ",working_list

        while working_list != set([]):
            splitter = working_list.pop()
            # print "partition= ",partition
            # print "splitter= ",splitter
            split_state = self.__split(splitter, partition)
            # print "split_state =  ", split_state
            working_list.discard(splitter)  # ->it raised KeyError when using .remove(el)
            
            partition_copy = partition.copy()
                    
            for apart in partition_copy:
                one_part = ()
                other_part = ()
                for x in split_state:
                    if x in apart:
                        one_part += (x,)

                other_part = tuple(x for x in apart if x not in one_part)
                        
                # update partition, if one apart is affected
                if one_part != () and other_part != ():
                    partition.discard(apart)
                    partition.add(one_part)
                    partition.add(other_part)

                    # update working_list
                    for symbol in self.alphabet:
                        if (apart, symbol) in working_list:
                            working_list.discard((apart,symbol))
                            working_list.add((one_part,symbol))
                            working_list.add((other_part,symbol))
                        else:
                            working_list.add((one_part,symbol))

        # establish the minimum automata obtained
        str = ""  # helping variable to join compound state
        new_alphabet = self.alphabet.copy()
        new_states = set([])
        new_start = self.start
        new_final = self.final.copy()
        new_delta = self.delta.copy()
        partition_copy = partition.copy()
        new_delta_copy = new_delta.copy()

        for tup_of_states in partition_copy:
            new_state = str.join(tup_of_states)
            if len(tup_of_states) > 1:
                if self.start in tup_of_states:
                    new_start = new_state
                if self.final.intersection(set(tup_of_states)) != set([]):
                    new_final.difference_update(set(tup_of_states))
                    new_final.add(new_state)
                for tup in new_delta_copy:
                    if tup[0] in tup_of_states:
                        new_delta.discard(tup)
                        if (new_state, tup[1], tup[2]) not in new_delta:
                            new_delta.add((new_state, tup[1], tup[2]))
                    elif tup[2] in tup_of_states:
                        new_delta.discard(tup)
                        if (tup[0], tup[1], new_state) not in new_delta:
                            new_delta.add((tup[0], tup[1], new_state))

            new_states.add(new_state)

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

    def is_complete(self):
        """
        check if for every state p and every alphabet a, there is exactly one state q such that (p,a,q)
        :rtype: bool
        """

        for symbol in self.alphabet:
            for state in self.states:
                if self.delta_function(state, symbol) != 's':
                    continue
                return False
        return True

    def make_it_complete(self):
        """
        most minimization algorithms assume automata to be complete. Calling this function to complete automata before
        it is minimized by any minimization algorithm.
        :rtype: Dfa
        """

        new_states = self.states.copy()
        new_alphabet = self.alphabet.copy()
        new_start = self.start
        new_final = self.final.copy()
        new_delta = self.delta.copy()

        if self.is_complete():
            return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)
        else:
            new_states.add('s')
            for symbol in new_alphabet:
                for state in new_states:
                    if self.delta_function(state, symbol) == 's':
                        new_delta.add((state, symbol, 's'))
            return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)

    # TODO
    def minimize_by_moore(self):
        """
        first, assume that the dfa is complete
        the idea is using complete graph (states as nodes) as starting step. Then mark all edges between final and
        non-final nodes. As long as there exist marked edges, repeat the following step. Choose (arbitrarily) a marked
        edge (p',q'). Mark all unmarked edges (p,q) where (p.a, q.a) = (p',q') for some a in alphabet.
        :rtype: Dfa
        """

        new_dfa = self.make_it_complete()
        complete_graph = set([])
        states = new_dfa.states.copy()
        while states != set([]):
            a_state = states.pop()
            for state in states:
                complete_graph.add((a_state, state))
        print complete_graph
        
        final = new_dfa.final.copy()
        not_final = new_dfa.states.difference(new_dfa.final)
        marked = set(tup for tup in complete_graph if tup[0] in final and tup[1] in not_final or tup[0] in not_final and
                     tup[1] in final)
        unmarked = complete_graph.difference(marked)
        print "marked: ", marked
        print "unmarked: ", unmarked
        unmarked_copy = unmarked.copy()
        while marked != set([]):
            a_marked = marked.pop()
            for tup in unmarked_copy:
                for symbol in new_dfa.alphabet:
                    if new_dfa.delta_function(tup[0], symbol) == a_marked[0] and \
                                    new_dfa.delta_function(tup[1], symbol) == a_marked[1] or \
                                            new_dfa.delta_function(tup[0], symbol) == a_marked[1] and \
                                            new_dfa.delta_function(tup[1], symbol) == a_marked[0]:
                        marked.discard(a_marked)
                        marked.add(tup)
                        unmarked.discard(tup)
                        break

        print "marked: ", marked
        print "unmarked: ", unmarked
        # helping variable
        str = ""

        # establish new DFA
        # if any, we return a new DFA without sink state
        new_dfa.states.discard('s')
        for delta in new_dfa.delta.copy():
            if delta[2] == 's':
                new_dfa.delta.discard(delta)

        if unmarked == set([]):
            return Dfa(new_dfa.states, new_dfa.alphabet, new_dfa.delta, new_dfa.start, new_dfa.final)
        else:
            new_alphabet = new_dfa.alphabet.copy()
            new_states = set([])
            new_delta = new_dfa.delta.copy()
            new_start = new_dfa.start
            new_final = set([])

            unmarked_states = set([])
            unmarked_copy = unmarked.copy()

            # check for states which are marked and which are unmarked
            for tup in unmarked_copy:
                unmarked_states.add(tup[0])
                unmarked_states.add(tup[1])

            marked_states = new_dfa.states.difference(unmarked_states)

            print "mark: ", marked_states
            print "unmark: ", unmarked_states

            # marked states directly added to new_states
            new_states = new_states.union(marked_states)

            # may marked states contain a final state
            for state in marked_states:
                if state in new_dfa.final:
                    new_final.add(state)

            # join unmarked states
            while unmarked_copy != set([]):  # imagine a case: {(1,2), (3,4), (4,5)}
                tup = unmarked_copy.pop()
                new_state = str.join(tup)
                unmarked_copy.discard(tup)
                for other_tup in unmarked_copy:
                    if other_tup[0] in tup:
                        new_state =+ other_tup[1]
                        unmarked_copy.discard(other_tup)
                    elif other_tup[1] in tup:
                        new_state =+ other_tup[0]
                        unmarked_copy.discard(other_tup)

                    # check if the start state is also joined with other state
                    if new_dfa.start in tup or new_dfa.start in other_tup:
                        new_start = new_state

                # look for final states from unmarked states
                for state in new_dfa.final:

                    # it's not possible that a non-final state joins with a final state
                    if state in tup:
                        new_final.add(new_state)

                unmarked_copy.discard(tup)

                # add the joined state to new_state
                new_states.add(new_state)

            # remove transitions from states those are joined, and add the new one
            for state in unmarked_states:
                for symbol in new_alphabet:
                    new_delta.discard((state, symbol, new_dfa.delta_function(state, symbol)))
                    new_delta.add((new_state, symbol, new_dfa.delta_function(state, symbol)))

            # update incoming transition of the new joined states
            new_delta_copy = new_delta.copy()
            for delta in new_delta_copy:
                if delta[2] in unmarked_states:
                    new_delta.discard(delta)
                    new_delta.add((delta[0], delta[1], new_state))

            return Dfa(new_states, new_alphabet, new_delta, new_start, new_final)

    # TODO
    def minimize_by_brzozowski(self):
        """

        :rtype: Dfa
        """
        pass

    # TODO
    def convert_to_regex(self):
        """
        our regular expression will only need symbols in alphabet, operator +, *,concatenation that has no shape,
        and parentheses to against priority.(* > . > +)
        :rtype: str
        """
        pass
