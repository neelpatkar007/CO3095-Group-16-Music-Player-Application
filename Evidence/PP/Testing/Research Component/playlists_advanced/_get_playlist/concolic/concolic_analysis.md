# Concolic Analysis of `_get_playlist` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3)  | Path Taken           | Constraint to Flip       | New Derived Input          |
|-------------|-----------------------------|----------------------|--------------------------|----------------------------|
| 1           | (None, "1", [])             | PC_1 (Error)         | Flip (S1 == None)        | (ValidState, "1", [])      |
| 2           | (ValidState, "", [])        | PC_2 (Error)         | Flip (NOT S2.strip)      | (ValidState, "1", [])      |
| 3           | (ValidState, "1", [])       | PC_3 (Out of Bounds) | Flip (idx >= len S3)     | (ValidState, "1", [P1])    |
| 4           | (ValidState, "1", [P1])     | PC_4 (Index Success) | Flip (S2.isdigit)        | (ValidState, "Rock", [P1]) |
| 5           | (ValidState, "Rock", [P1])  | PC_6 (Name Fail)     | Flip (S2 in S3)          | (ValidState, "P1", [P1])   |
| 6           | (ValidState, "P1", [P1])    | PC_5 (Name Success)  | None (Explored)          | N/A                        |