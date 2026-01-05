# Concolic Analysis of `render_progress_bar` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3, S4)   | Path Taken   | Constraint to Flip    | New Derived Input        |
|------------|----------------------------------|--------------|-----------------------|--------------------------|
| 1          | (None, 15, 0, 100)               | PC_1         | Flip (S1 is None)     | (StateObj, 15, 0, 100)   |
| 2          | (StateObj, "high", 0, 100)       | PC_2         | Flip (S2 is NOT int)  | (StateObj, -5, 0, 100)   |
| 3          | (StateObj, -5, 0, 100)           | PC_3         | Flip (S2 <= 0)        | (StateObj, 15, 0, None)  |
| 4          | (StateObj, 15, 0, None)          | PC_4         | Flip (S4 is None)     | (StateObj, 15, 0, "err") |
| 5          | (StateObj, 15, 0, "err")         | PC_5         | Flip (S4 is NOT num)  | (StateObj, 15, 0, 0)     |
| 6          | (StateObj, 15, 0, 0)             | PC_6         | Flip (S4 <= 0)        | (StateObj, 15, 20, 100)  |
| 7          | (StateObj, 15, 20, 100)          | PC_7         | All branches explored | N/A                      |