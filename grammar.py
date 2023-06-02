class Grammar:
    alphabet: int = 27
    rules: list

    def __init__(self):
        self.rules = [[] for _ in range(self.alphabet)]

    def __len__(self) -> int:
        return len(self.rules)

    def __getitem__(self, index: int) -> list:
        return self.rules[index]

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        if self.iter_counter < len(self.rules):
            self.iter_counter += 1
            return self.rules[self.iter_counter - 1]
        else:
            raise StopIteration


class Situation:
    rule: str
    point_pos: int
    read_symbols: int
    prev_situation: int

    def __init__(self, rule: str, point_pos: int, read_symbols: int, prev_situation: int):
        self.rule = rule
        self.point_pos = point_pos
        self.read_symbols = read_symbols
        self.prev_situation = prev_situation

    def __eq__(self, other: 'Situation') -> bool:
        return (self.rule == other.rule) and (self.point_pos == other.point_pos) \
            and (self.read_symbols == other.read_symbols) and (self.prev_situation == other.prev_situation)
