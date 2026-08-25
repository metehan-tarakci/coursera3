def read_strings(file):
    with open(file, "r") as f:
        strings = [line.rstrip() for line in f if line.rstrip() != ""]
    return strings


def multiple_lcs(v, w, u):
    n, m, l = len(v), len(w), len(u)

    # dp[i][j][k] = length of best multiple alignment using
    # v[:i], w[:j], u[:k]
    dp = [[[0] * (l + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    parent = [[[None] * (l + 1) for _ in range(m + 1)] for _ in range(n + 1)]

    # All 7 ways to step backward: decrement any
    # non-empty subset of {i, j, k} by 1
    # Each tuple (di, dj, dk) represents "how much to step backward" in each of the three dimensions to reach a predecessor cell.
    moves = [
        (1, 1, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 0, 0), (0, 1, 0), (0, 0, 1)
    ]

    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(l + 1):
                if i == 0 and j == 0 and k == 0: # Skip the base case (0,0,0) — it's correctly pre-initialized to 0 (empty prefixes of all three strings trivially have a shared alignment of length 0), and there's no valid backward move from it anyway.
                    continue

                best = -1
                best_move = None

                for di, dj, dk in moves:
                    pi, pj, pk = i - di, j - dj, k - dk
                    if pi < 0 or pj < 0 or pk < 0:
                        continue

                    add = 0
                    # only a fully-diagonal move (all three strings
                    # advance together) can score a point, and only
                    # if all three characters actually match
                    if di == 1 and dj == 1 and dk == 1:
                        if v[i - 1] == w[j - 1] == u[k - 1]:
                            add = 1

                    val = dp[pi][pj][pk] + add
                    if val > best:
                        best = val
                        best_move = (di, dj, dk)

                dp[i][j][k] = best
                parent[i][j][k] = best_move

    # Traceback from (n, m, l) back to (0, 0, 0)
    i, j, k = n, m, l
    aligned_v, aligned_w, aligned_u = [], [], []

    while not (i == 0 and j == 0 and k == 0):
        di, dj, dk = parent[i][j][k]
        aligned_v.append(v[i - 1] if di else "-")
        aligned_w.append(w[j - 1] if dj else "-")
        aligned_u.append(u[k - 1] if dk else "-")
        i -= di
        j -= dj
        k -= dk

    aligned_v.reverse()
    aligned_w.reverse()
    aligned_u.reverse()

    return dp[n][m][l], "".join(aligned_v), "".join(aligned_w), "".join(aligned_u)


strings = read_strings("week3_4.txt")
v, w, u = strings[0], strings[1], strings[2]

score, av, aw, au = multiple_lcs(v, w, u)

print(score)
print(av)
print(aw)
print(au)