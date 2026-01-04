# Concolic Testing Analysis: `resume` Function

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2) | Path Taken          | Constraint to Flip           | New Derived Input |
|-----------|------------------------|---------------------|------------------------------|-------------------|
| 1         | (False, False)         | PC_1 (Early Return) | Flip (NOT S1) → S1           | (True, False)     |
| 2         | (True, False)          | PC_3 (Simulated)    | Flip (NOT S2) → S2           | (True, True)      |
| 3         | (True, True)           | PC_2 (_resume_real) | None (All branches explored) | N/A               |