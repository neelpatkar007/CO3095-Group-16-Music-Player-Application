# Concolic Testing Analysis: `is_busy` Function

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3, S4)  | Path Taken  | Constraint to Flip              | New Derived Input          |
|-----------|---------------------------------|-------------|---------------------------------|----------------------------|
| 1         | (True, False, False, True)      | PC_1        | Flip (S1)                       | (False, False, False, N/A) |
| 2         | (False, True, False, N/A)       | PC_2        | Flip (S2 AND NOT S3) → False    | (False, False, False, N/A) |
| 3         | (False, False, False, N/A)      | PC_2        | None (Branch Coverage Complete) | N/A                        |