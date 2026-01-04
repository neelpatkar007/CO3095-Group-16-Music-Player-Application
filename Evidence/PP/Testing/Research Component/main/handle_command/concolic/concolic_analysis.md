# Concolic Execution Path Exploration Table for `main` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S4)    | Path Taken            | Constraint to Flip             | New Derived Input               |
|-------------|-----------------------------------|-----------------------|--------------------------------|---------------------------------|
| 1           | ("", False, False, 0.0)           | PC_1 (Empty)          | Flip NOT S1                    | ("p", False, False, 0.0)        |
| 2           | ("p", False, False, 0.0)          | PC_2 (Shortcut)       | Flip base == /quit             | ("/quit", False, False, 0.0)    |
| 3           | ("/quit", False, False, 0.0)      | PC_3 (Quit)           | Flip base == /play             | ("/play", False, False, 0.0)    |
| 4           | ("/play", False, False, 0.0)      | PC_6 (Play Standard)  | Flip S2 AND S3                 | ("/play", True, True, 0.0)      |
| 5           | ("/play", True, True, 0.0)        | PC_5 (Resume No Seek) | Flip S4 > 0                    | ("/play", True, True, 10.0)     |
| 6           | ("/play", True, True, 10.0)       | PC_4 (Resume Seek)    | Backtrack & Flip base == /seek | ("/seek", False, False, 0.0)    |
| 7           | ("/seek", False, False, 0.0)      | PC_13 (Seek Error)    | Flip args Empty                | ("/seek 30", False, False, 0.0) |
| 8           | ("invalid", False, False, 0.0)    | PC_21 (Unknown)       | None (Leaves explored)         | N/A                             |