from grammar import Grammar, Situation


class Earley:
    grammar: Grammar
    word: str
    
    def __init__(self, rules: list[str], word: str):
        self.word = word
        self.build_grammar(rules)

    @staticmethod
    def is_non_terminal(rule: str, index: int) -> bool:
        return ord('A') <= ord(rule[index]) <= ord('Z') if index < len(rule) else False

    @staticmethod
    def is_letter(rule: str, index: int) -> bool:
        return (ord('a') <= ord(rule[index]) <= ord('z') or ord('A') <= ord(rule[index]) <= ord('Z')
                or rule[index] == '1') if index < len(rule) else False

    def complete(self, various_rules_opening: list[list[Situation]], num_situation: int, start: int):
        size = len(various_rules_opening[num_situation])
        for i in range(start, size):
            rule = various_rules_opening[num_situation][i].rule
            position_where_now = various_rules_opening[num_situation][i].point_pos
            if position_where_now >= len(rule):
                self.complete_helper(various_rules_opening, num_situation, i)

    def complete_helper(self, various_rules_opening: list[list[Situation]], num_situation: int, index: int):
        len_output_prefix = various_rules_opening[num_situation][index].read_symbols
        prev_situation = various_rules_opening[num_situation][index].prev_situation
        for j in range(len(various_rules_opening[len_output_prefix])):
            rule_prev = various_rules_opening[len_output_prefix][j].rule
            pos_prev = various_rules_opening[len_output_prefix][j].point_pos
            if self.is_non_terminal(rule_prev, pos_prev) and (prev_situation == (ord(rule_prev[pos_prev]) - ord('A'))):
                cur = Situation(
                    rule=rule_prev,
                    point_pos=pos_prev + 1,
                    read_symbols=various_rules_opening[len_output_prefix][j].read_symbols,
                    prev_situation=various_rules_opening[len_output_prefix][j].prev_situation
                )
                if cur != various_rules_opening[num_situation][index]:
                    various_rules_opening[num_situation].append(cur)

    def predict(self,  various_rules_opening: list[list[Situation]], num_situation: int, start: int):
        size = len(various_rules_opening[num_situation])
        for i in range(start, size):
            rule = various_rules_opening[num_situation][i].rule
            position_where_now = various_rules_opening[num_situation][i].point_pos
            if self.is_non_terminal(rule, position_where_now):
                for gr_rule in self.grammar[ord(rule[position_where_now]) - ord('A')]:
                    various_rules_opening[num_situation].append(Situation(
                        rule=gr_rule,
                        point_pos=0,
                        read_symbols=num_situation,
                        prev_situation=ord(rule[position_where_now]) - ord('A')
                    ))

    def scan(self, various_rules_opening: list[list[Situation]], num_situation: int):
        if num_situation == 0:
            return
        size = len(various_rules_opening[num_situation - 1])
        for i in range(size):
            self.scan_helper(various_rules_opening, num_situation, i)

    def scan_helper(self, various_rules_opening: list[list[Situation]], num_situation: int, index: int):
        cur_situation = num_situation - 1
        rule = various_rules_opening[cur_situation][index].rule
        position_where_now = various_rules_opening[cur_situation][index].point_pos
        prev_situation = various_rules_opening[cur_situation][index].prev_situation
        if position_where_now == len(rule):
            return
        if rule[position_where_now] == self.word[cur_situation]:
            various_rules_opening[num_situation].append(Situation(
                rule=rule,
                point_pos=position_where_now + 1,
                read_symbols=various_rules_opening[cur_situation][index].read_symbols,
                prev_situation=prev_situation
            ))

    def build_grammar(self, rules: list):
        self.grammar = Grammar()
        for i in range(len(rules)):
            position_where_now = ord(rules[i][0]) - ord('A')
            for j in range(1, len(rules[i])):
                if self.is_letter(rules[i], j):
                    rule = rules[i][j:len(rules[i])]
                    if rule == '1':
                        rule = ''
                    self.grammar[position_where_now].append(rule)
                    break

    def earley(self) -> bool:
        word_size = len(self.word)
        various_rules_opening = [[] for _ in range(word_size + 1)]
        various_rules_opening[0].append(Situation(
            rule='S',
            point_pos=0,
            read_symbols=0,
            prev_situation=-1
        ))
        self.earley_parser(various_rules_opening, word_size)
        word_in_grammar = Situation(
            rule='S',
            point_pos=1,
            read_symbols=0,
            prev_situation=-1
        )
        for i in range(len(various_rules_opening[word_size])):
            if various_rules_opening[word_size][i] == word_in_grammar:
                return True
        return False

    def earley_parser(self, various_rules_opening: list[list[Situation]], word_size: int):
        for i in range(word_size + 1):
            start = 0
            self.scan(various_rules_opening, i)
            while True:
                various_rules_opening_size = len(various_rules_opening[i])
                self.complete(various_rules_opening, i, start)
                self.predict(various_rules_opening, i, start)
                start = various_rules_opening_size
                if len(various_rules_opening[i]) <= various_rules_opening_size:
                    break
