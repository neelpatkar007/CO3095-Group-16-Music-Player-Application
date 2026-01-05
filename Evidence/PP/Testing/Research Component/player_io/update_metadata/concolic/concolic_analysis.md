# Concolic Analysis for update_metadata Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3)  | Path Taken   | Constraint to Flip                      | New Derived Input     |
|-------------|-----------------------------|--------------|-----------------------------------------|-----------------------|
| 1           | ("", "title", "Val")        | PC_1         | Flip (S1 == "")                         | ("1", "title", "Val") |
| 2           | ("99", "title", "Val")      | PC_2         | Flip (idx < len(S4))                    | ("1", "title", "Val") |
| 3           | ("1", "title", "")          | PC_3         | Flip (S3 == "")                         | ("1", "genre", "Val") |
| 4           | ("1", "genre", "Val")       | PC_4         | Flip (S2 != "title" AND S2 != "artist") | ("1", "title", "Val") |

