import itertools


def win(a, b):
    win_count = 0
    assert (len(a) == len(b))
    l = len(a)
    for i in range(l):
        for j in range(l):
            if a[i] > b[j]:
                win_count += 1

    return win_count > l * l / 2


def main():
    result = set()
    for perm in itertools.permutations(range(1, 10)):
        a = perm[0:3]
        b = perm[3:6]
        c = perm[6:9]
        if win(a, b) and win(b, c) and win(c, a):
            a = tuple(sorted(a))
            b = tuple(sorted(b))
            c = tuple(sorted(c))
            result.add(tuple(sorted([a, b, c])))
    for t in sorted(result):
        print(t)


if __name__ == "__main__":
    main()
