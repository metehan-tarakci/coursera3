"""

| Problem               | What are we aligning?                           | First column  | First row     | Where is optimum found?               | Where does backtracking start? | Where does backtracking stop? |
| --------------------- | ----------------------------------------------- | ------------- | ------------- | ------------------------------------- | ------------------------------ | ----------------------------- |
| **Global Alignment**  | **Entire `v` + entire `w`**                     | Gap penalties | Gap penalties | **Bottom-right cell** `dp[n][m]`      | `(n, m)`                       | `(0, 0)`                      |
| **Local Alignment**   | **Any substring of `v` + any substring of `w`** | `0`           | `0`           | **Maximum anywhere in table**         | Cell containing maximum        | First cell with score `0`     |
| **Fitting Alignment** | **Substring of `v` + entire `w`**               | `0`           | Gap penalties | **Maximum in last column** `dp[i][m]` | Maximum cell in last column    | `j = 0`                       |
| **Overlap Alignment** | **Suffix of `v` + prefix of `w`**               | `0`           | Gap penalties | **Maximum in last row** `dp[n][j]`    | Maximum cell in last row       | `j = 0`                       |

"""

def overlap_alignment(v, w, match_reward, mismatch_penalty, indel_penalty):

    n = len(v)
    m = len(w)

    # Create DP table
    # dp[i][j] = best score for aligning
    # the first i characters of v
    # with the first j characters of w
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Create backtrack table
    backtrack = [[""] * (m + 1) for _ in range(n + 1)]

    # INITIALIZATION

    # First column is 0.
    # We are allowed to ignore the beginning of v.
    # This allows the alignment to start at any position in v.
    for i in range(1, n + 1):
        dp[i][0] = 0

    # First row gets gap penalties.
    # w must be aligned from its beginning.
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] - indel_penalty
        backtrack[0][j] = "→"

    # FILL DP TABLE
    """                w
          ""   G    A    T
v       ┌────┬────┬────┬────┐
""      │  0 │ -2 │ -4 │ -6 │
        ├────┼────┼────┼────┤
G       │  0 │  1 │ -1 │ -3 │
        ├────┼────┼────┼────┤
A       │  0 │ -1 │  2 │  0 │
        ├────┼────┼────┼────┤
G       │  0 │  1 │  0 │  1 │
        ├────┼────┼────┼────┤
A       │  0 │ -1 │  2 │  0 │
        └────┴────┴────┴────┘
    """
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # Align v[i-1] with a gap
            from_up = dp[i - 1][j] - indel_penalty

            # Align w[j-1] with a gap
            from_left = dp[i][j - 1] - indel_penalty

            # Align v[i-1] with w[j-1]
            if v[i - 1] == w[j - 1]:
                from_diagonal = dp[i - 1][j - 1] + match_reward
            else:
                from_diagonal = dp[i - 1][j - 1] - mismatch_penalty

            # Choose the best option
            if from_up >= from_left and from_up >= from_diagonal:
                dp[i][j] = from_up
                backtrack[i][j] = "↓"

            elif from_left >= from_up and from_left >= from_diagonal:
                dp[i][j] = from_left
                backtrack[i][j] = "→"

            else:
                dp[i][j] = from_diagonal
                backtrack[i][j] = "↘"

    # FIND BEST ENDING POSITION

    # The alignment must finish at the END of v,
    # because we need a suffix of v.
    #
    # Therefore, look for the maximum value
    # in the LAST ROW.
    best_score = dp[n][0]
    best_j = 0

    for j in range(1, m + 1):
        if dp[n][j] > best_score:
            best_score = dp[n][j]
            best_j = j

    # BACKTRACK

    # Start at the best cell in the last row
    i = n
    j = best_j

    alignment_v = ""
    alignment_w = ""

    # Stop when j reaches 0.
    # This means we have reached the beginning of w,
    # so the aligned part of w is a PREFIX of w.
    while j > 0:

        if backtrack[i][j] == "↓":

            alignment_v = v[i - 1] + alignment_v
            alignment_w = "-" + alignment_w

            i -= 1

        elif backtrack[i][j] == "→":

            alignment_v = "-" + alignment_v
            alignment_w = w[j - 1] + alignment_w

            j -= 1

        elif backtrack[i][j] == "↘":

            alignment_v = v[i - 1] + alignment_v
            alignment_w = w[j - 1] + alignment_w

            i -= 1
            j -= 1

    return best_score, alignment_v, alignment_w

# INPUT
match_reward = 1
mismatch_penalty = 1
indel_penalty = 2

v = "GAGA"
w = "GAT"

# Solve
score, alignment_v, alignment_w = overlap_alignment(
    v,
    w,
    match_reward,
    mismatch_penalty,
    indel_penalty
)

print(score)
print(alignment_v)
print(alignment_w)