# Concolic Analysis of the `handle_keypress` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S4)   | Path Taken   | Constraint to Flip  | New Derived Input          |
|-------------|----------------------------------|--------------|---------------------|----------------------------|
| 1           | (None, [], False, 50)            | PC_1         | Flip (NOT S1)       | ('p', [], False, 50)       |
| 2           | ('p', [], False, 50)             | PC_2         | Flip (NOT S2)       | ('p', ['trk1'], False, 50) |
| 3           | ('p', ['trk1'], False, 50)       | PC_4         | Flip (NOT S3)       | ('p', ['trk1'], True, 50)  |
| 4           | ('p', ['trk1'], True, 50)        | PC_3         | Flip (S1 == 'p')    | ('s', [], True, 50)        |
| 5           | ('s', [], True, 50)              | PC_5         | Flip (S3)           | ('s', [], False, 50)       |
| 6           | ('s', [], False, 50)             | PC_6         | Flip (S1 == 's')    | ('m', [], False, 50)       |
| 7           | ('m', [], False, 50)             | PC_7         | Flip (S1 == 'm')    | ('+', [], False, 90)       |
| 8           | ('+', [], False, 90)             | PC_8         | Flip (S4 < 100)     | ('+', [], False, 100)      |
| 9           | ('+', [], False, 100)            | PC_9         | Flip (S1 == '+')    | ('-', [], False, 10)       |
| 10          | ('-', [], False, 10)             | PC_10        | Flip (S4 > 0)       | ('-', [], False, 0)        |
| 11          | ('-', [], False, 0)              | PC_11        | Flip (S1 == '-')    | ('x', [], False, 50)       |
| 12          | ('x', [], False, 50)             | PC_12        | None                | N/A                        |