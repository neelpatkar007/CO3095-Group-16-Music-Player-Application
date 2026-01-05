# Concolic Analysis of the `nudge` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3)  | Path Taken  | Constraint to Flip           | New Derived Input       |
|------------|-----------------------------|-------------|------------------------------|-------------------------|
| 1          | (None, 0.0, 5.0)            | PC_1        | Flip (S1 == None)            | (Object, "string", 5.0) |
| 2          | (Object, "string", 5.0)     | PC_2        | Flip (NOT (S2 is float/int)) | (Object, 10.0, 5.0)     |
| 3          | (Object, 10.0, 5.0)         | PC_3        | None (Full Coverage)         | N/A                     |