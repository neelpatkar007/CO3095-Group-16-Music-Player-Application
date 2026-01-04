# Concolic Analysis of search_library Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3)   | Path Taken   | Constraint to Flip   | New Derived Input   |
|------------|------------------------------|--------------|----------------------|---------------------|
| 1          | (None, "rock", N/A)          | PC_1         | Flip (S1 is None)    | (Obj, "rock", N/A)  |
| 2          | (Obj, "", N/A)               | PC_2         | Flip (NOT S2)        | (Obj, "rock", N/A)  |
| 3          | (Obj, "rock", Missing)       | PC_3         | Flip (No Attr)       | (Obj, "rock", Int)  |
| 4          | (Obj, "rock", 123)           | PC_4         | Flip (Not List)      | (Obj, "rock", [])   |
| 5          | (Obj, "rock", [])            | PC_5         | Flip (S3 Empty)      | (Obj, "rock", [S4]) |
| 6          | (Obj, "rock", [S4_Match])    | PC_7         | None (Leaf Node)     | N/A                 |