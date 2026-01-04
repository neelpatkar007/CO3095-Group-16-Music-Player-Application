# Research Analysis: Concolic Testing of `pause()`

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3)  | Path Taken              | Constraint to Flip              | New Derived Input         |
|-----------|-----------------------------|-------------------------|---------------------------------|---------------------------|
| 1         | (False, False, True)        | PC_1 (Early Return)     | Flip (NOT S1) to force entry    | (True, False, True)       |
| 2         | (True, False, True)         | PC_2 (_pause_real)      | Flip (S3 == True)               | (True, False, False)      |
| 3         | (True, False, False)        | PC_3 (Simulated)        | None (All branches explored)    | N/A                       |