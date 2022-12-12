from grammar import Grammar, Situation


def is_non_terminal(rule: str, index: int) -> bool:
    return ord('A') <= ord(rule[index]) <= ord('Z') if index < len(rule) else False


def complete(various_rules_opening: list[list[Situation]], num_situation: int, start: int):
    size = len(various_rules_opening[num_situation])
    for i in range(start, size):
        rule = various_rules_opening[num_situation][i].rule
        position_where_now = various_rules_opening[num_situation][i].point_pos
        len_output_prefix = various_rules_opening[num_situation][i].read_symbols
        prev_situation = various_rules_opening[num_situation][i].prev_situation
        if position_where_now >= len(rule):
            for j in range(len(various_rules_opening[len_output_prefix])):
                rule_prev = various_rules_opening[len_output_prefix][j].rule
                pos_prev = various_rules_opening[len_output_prefix][j].point_pos
                if is_non_terminal(rule_prev, pos_prev) and (prev_situation == (ord(rule_prev[pos_prev]) - ord('A'))):
                    cur = Situation(
                        rule=rule_prev,
                        point_pos=pos_prev+1,
                        read_symbols=various_rules_opening[len_output_prefix][j].read_symbols,
                        prev_situation=various_rules_opening[len_output_prefix][j].prev_situation
                    )
                    if cur != various_rules_opening[num_situation][i]:
                        various_rules_opening[num_situation].append(cur)


def predict(grammar: Grammar, various_rules_opening: list[list[Situation]], num_situation: int, start: int):
    size = len(various_rules_opening[num_situation])
    for i in range(start, size):
        rule = various_rules_opening[num_situation][i].rule
        position_where_now = various_rules_opening[num_situation][i].point_pos
        if is_non_terminal(rule, position_where_now):
            for gr_rule in grammar[ord(rule[position_where_now]) - ord('A')]:
                various_rules_opening[num_situation].append(Situation(
                    rule=gr_rule,
                    point_pos=0,
                    read_symbols=num_situation,
                    prev_situation=ord(rule[position_where_now])-ord('A')
                ))


def scan(various_rules_opening: list[list[Situation]], num_situation: int, word: str):
    if num_situation == 0:
        return
    cur_situation = num_situation - 1
    size = len(various_rules_opening[cur_situation])
    for i in range(size):
        rule = various_rules_opening[cur_situation][i].rule
        position_where_now = various_rules_opening[cur_situation][i].point_pos
        prev_situation = various_rules_opening[cur_situation][i].prev_situation
        if position_where_now == len(rule):
            continue
        if rule[position_where_now] == word[cur_situation]:
            various_rules_opening[num_situation].append(Situation(
                rule=rule,
                point_pos=position_where_now + 1,
                read_symbols=various_rules_opening[cur_situation][i].read_symbols,
                prev_situation=prev_situation
            ))


def is_letter(rule: str, index: int) -> bool:
    return (ord('a') <= ord(rule[index]) <= ord('z') or ord('A') <= ord(rule[index]) <= ord('Z') \
            or rule[index] == '1') if index < len(rule) else False


def build_grammar(rules: list[str], grammar: Grammar):
    for i in range(len(rules)):
        position_where_now = ord(rules[i][0]) - ord('A')
        for j in range(1, len(rules[i])):
            if is_letter(rules[i], j):
                rule = rules[i][j:len(rules[i])]
                if rule == '1':
                    rule = ''
                grammar[position_where_now].append(rule)
                break


def earley(rules: list[str], word: str) -> bool:
    grammar = Grammar()
    build_grammar(rules, grammar)
    word_size = len(word)
    various_rules_opening = [[] for _ in range(word_size + 1)]
    various_rules_opening[0].append(Situation(
        rule='S',
        point_pos=0,
        read_symbols=0,
        prev_situation=-1
    ))
    for i in range(word_size + 1):
        start = 0
        scan(various_rules_opening, i, word)
        while True:
            various_rules_opening_size = len(various_rules_opening[i])
            complete(various_rules_opening, i, start)
            predict(grammar, various_rules_opening, i, start)
            start = various_rules_opening_size
            if len(various_rules_opening[i]) <= various_rules_opening_size:
                break
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
