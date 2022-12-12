import pytest
import earley


@pytest.mark.parametrize(
    ('rules', 'word', 'expecting_answer'), [
        (["S->aFbF", "F->aFb", "F->1"], 'aabb', True),
        (["S->aSbS", "S->bSaS", "S->1"], 'abb', False),
        (["S->AB", "S->1", "A->a", "B->b", "B->AA"], 'aaa', True),
        (["S->AB", "A->BC", "A->a", "B->b", "C->c"], 'abc', False),
    ]
)
def test_earley(rules, word, expecting_answer):
    assert earley.earley(rules, word) == expecting_answer