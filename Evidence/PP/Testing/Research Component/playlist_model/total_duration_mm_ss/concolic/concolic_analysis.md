# Concolic Testing Analysis: `total_duration_mm_ss`

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2)   | Path Taken          | Constraint to Flip           | New Derived Input  |
|-------------|--------------------------|---------------------|------------------------------|--------------------|
| 1           | ([], 0)                  | PC_1 (Early Return) | Flip (NOT S1)                | ([TrackObj], 120)  |
| 2           | ([TrackObj], 120)        | PC_2 (Format Call)  | None (All branches explored) | N/A                |