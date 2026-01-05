# Concolic Analysis of switch_profile Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S4)          | Path Taken  | Constraint to Flip    | New Derived Input                     |
|-------------|-----------------------------------------|-------------|-----------------------|---------------------------------------|
| 1           | (None, "Guest", {}, "")                 | PC_1        | Flip(PC_1)            | (Obj, "Guest", {}, "Admin")           |
| 2           | (Obj, "Guest", {}, "Admin")             | PC_2        | Flip(S2 != "default") | (Obj, "default", {}, "Admin")         |
| 3           | (Obj, "default", {}, "Admin")           | PC_5        | Flip(S2 in S3)        | (Obj, "Admin", {"Admin": {}}, "User") |
| 4           | (Obj, "Admin", {"Admin": {}}, "User")   | PC_4        | Flip(S2 == S4)        | (Obj, "User", {"User": {}}, "User")   |
| 5           | (Obj, "User", {"User": {}}, "User")     | PC_3        | None                  | N/A                                   |