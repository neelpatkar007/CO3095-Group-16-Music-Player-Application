# Concolic Analysis of `format_mm_ss` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1)           | Path Taken  | Constraint to Flip  | New Derived Input  |
|-------------|------------------------------|-------------|---------------------|--------------------|
| 1           | None                         | PC_1        | NOT (S1 is None)    | 125.5              |
| 2           | 125.5                        | PC_2        | NOT (S1 >= 0)       | -5.0               |
| 3           | None (All branches explored) | N/A         | N/A                 | N/A                |