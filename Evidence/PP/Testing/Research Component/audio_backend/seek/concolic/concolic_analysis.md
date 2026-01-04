# Concolic Analysis: `_seek`

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3)  | Path Taken                 | Constraint to Flip           | New Derived Input   |
|-----------|-----------------------------|----------------------------|------------------------------|---------------------|
| **1**     | (False, False, 10.0)        | **PC_1** (Early Return)    | Flip (NOT S1) → S1           | (True, False, 10.0) |
| **2**     | (True, False, 10.0)         | **PC_3** (_seek_simulated) | Flip (NOT S2) → S2           | (True, True, 10.0)  |
| **3**     | (True, True, 10.0)          | **PC_2** (_seek_real)      | None (All branches explored) | N/A                 |