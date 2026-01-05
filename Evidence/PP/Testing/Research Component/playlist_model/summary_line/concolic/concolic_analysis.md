# Concolic Analysis of `summary_line` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2)   | Path Taken  | Constraint to Flip           | New Derived Input   |
|-------------|--------------------------|-------------|------------------------------|---------------------|
| 1           | (None, False)            | PC_4        | Flip (S2 is False)           | (None, True)        |
| 2           | (None, True)             | PC_3        | Flip (NOT S1 is int)         | (1, True)           |
| 3           | (1, True)                | PC_1        | Flip (S2 is True)            | (1, False)          |
| 4           | (1, False)               | PC_2        | None (All branches explored) | N/A                 |