# Concolic Analysis of Close Playlist Function

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3)   | Path Taken  | Constraint to Flip           | New Derived Input         |
|-----------|------------------------------|-------------|------------------------------|---------------------------|
| 1         | S1=False (Missing Attr)      | PC_1        | Flip (NOT S1)                | S1=True, S2=ObjA, S3=ObjB |
| 2         | S1=True, S2=ObjA, S3=ObjA    | PC_2        | Flip (S2 IS S3)              | S1=True, S2=ObjA, S3=ObjB |
| 3         | S1=True, S2=ObjA, S3=ObjB    | PC_3        | None (All branches explored) | N/A                       |