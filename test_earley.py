import pytest
from earley import Earley


@pytest.mark.parametrize(
    ('rules', 'word', 'expecting_answer'), [
        (["S->aFbF", "F->aFb", "F->1"], 'aabb', True),
        (["S->aSbS", "S->bSaS", "S->1"], 'abb', False),
        (["S->AB", "S->1", "A->a", "B->b", "B->AA"], 'aaa', True),
        (["S->AB", "A->BC", "A->a", "B->b", "C->c"], 'abc', False),
        (["S->AB", "A->a", "B->b", "A->1"], 'ab', True),
        (["S->AB", "A->a", "B->b", "A->1"], 'a', False),
    ]
)
def test_earley(rules, word, expecting_answer):
    earley = Earley(rules, word)
    assert earley.earley() == expecting_answer
