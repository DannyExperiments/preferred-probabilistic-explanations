"""Exact small-instance census for preferred probabilistic abduction."""

from fractions import Fraction
from itertools import product


def truth(table, x, y):
    return bool(table & (1 << (2 * x + y)))


def selectors(mask):
    return bool(mask & 1) + 2 * bool(mask & 4)


def contains(term, selectors_mask, fallback, fallback_bit=16):
    return (term & 15 & selectors_mask) == (term & 15) and (not term & fallback_bit or fallback)


def query(table):
    return any(all(truth(table, x, y) for y in (0, 1)) for x in range(4))


def check_one_assessment():
    worlds = list(product(range(16), range(2), range(2)))
    theory = [(mask, s, y) for mask, s, y in worlds if (mask & 3) in (1, 2) and (mask & 12) in (4, 8)]
    dummy = [(mask, s, y) for mask, s, y in worlds if mask == 15 and not s]
    assert dummy and set(dummy).isdisjoint(theory)
    assert all(contains(term, *world[:2]) for world in dummy for term in range(16))
    assert not any(contains(16, *world[:2]) for world in dummy)
    assert any(contains(16, *world[:2]) for world in theory)
    for table in range(256):
        solutions = []
        for term in range(32):
            models = [(mask, s, y) for mask, s, y in theory if contains(term, mask, s)]
            if models and all(s or truth(table, selectors(mask), y) for mask, s, y in models):
                # A witness in the theory can carry the residual one-third mass.
                solutions.append(term)
        assert 16 in solutions
        assert all(contains(16, *world[:2]) for term in solutions if term & 16
                   for world in worlds if contains(term, *world[:2]))
        assert any(term < 16 for term in solutions) == query(table)
    print("One assessment: all 256 truth tables, 32 terms and 64 valuations.")


def obs(table, mask, s, u, y):
    if s or u:
        return True
    if not (mask & 3 and mask & 12):
        return False
    return mask & 3 == 3 or mask & 12 == 12 or truth(table, selectors(mask), y)


def check_listed():
    worlds = list(product(range(16), range(2), range(2), range(2)))
    support = [(0, 1, 1, 0)] + [(15 ^ (1 << j), 0, 1, 0) for j in range(4)]
    masses = [Fraction(sum(contains(term, mask, s) for mask, s, _, _ in support), 5)
              for term in range(32)]
    assert masses[0] == 1 and masses[16] == Fraction(1, 5)
    for term in range(1, 16):
        assert masses[term] == Fraction(4 - bin(term).count("1"), 5)
    exemplar = (1 << 2) | (1 << 3)  # x = 1, both y values
    for table in range(256):
        entails = [
            all(not contains(term, mask, s) or obs(table, mask, s, u, y) for mask, s, u, y in worlds)
            for term in range(32)
        ]
        assert entails[16] and all(obs(table, *w) for w in support)
        assert any(entails[t] and masses[t] > masses[16] for t in range(32)) == query(table)
        if table == exemplar:
            assert (masses[1], entails[1]) == (Fraction(3, 5), False)
            assert (masses[9], entails[9]) == (Fraction(2, 5), True)
            assert (masses[7], entails[7]) == (Fraction(1, 5), True)
    print("Listed distribution: all 256 truth tables, 32 terms and 128 valuations.")
    print("Illustration: 3/5 without entailment; 2/5 with entailment; 1/5 tie.")


def check_fixed():
    worlds = list(product((0, 1), repeat=5))
    support = ((1, 0, 1, 0, 0), (0, 1, 1, 0, 0))
    weights = (Fraction(1, 3), Fraction(2, 3))

    def holds(term, w):
        return all(w[j] for j in range(2) if term & (1 << j))

    for f, g in product(range(4), repeat=2):
        def counter(w):
            s, t, u, x, y = w
            observation = (s and (u or not g & (1 << y))) or (
                not s and t and (u or not f & (1 << x)))
            return not (s and t) and not observation

        def entails(term):
            return not any(counter(w) and holds(term, w) for w in worlds)

        def mass(term):
            return sum(weight for point, weight in zip(support, weights) if holds(term, point))

        assert all(not counter(w) for w in support)
        better = any(mass(term) > mass(1) and entails(term) for term in range(4))
        complete_support_terms = []
        for mask in range(1, 4):
            indices = [j for j in range(2) if mask & (1 << j)]
            if sum(weights[j] for j in indices) > mass(1):
                complete_support_terms.append(sum(1 << i for i in range(2)
                                                  if all(support[j][i] for j in indices)))
        assert better == any(entails(term) for term in complete_support_terms)
        assert (entails(1) and not better) == (f != 0 and g == 0)
    print("Two positive points: all 16 paired SAT–UNSAT truth tables and subset certificates.")


if __name__ == "__main__":
    check_one_assessment()
    check_listed()
    check_fixed()
