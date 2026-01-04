# Concolic Analysis of `view_albums_table` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3)               | Path Taken          | Constraint to Flip   | New Derived Input                        |
|------------|------------------------------------------|---------------------|----------------------|------------------------------------------|
| 1          | (None, N/A, N/A)                         | PC_1 (Early Return) | Flip (NOT S1)        | (PlayerState(), [], N/A)                 |
| 2          | (PlayerState(), [], N/A)                 | PC_1 (Early Return) | Flip (NOT S2)        | (PlayerState(), [Track()], Track)        |
| 3          | (PlayerState(), [Track], Track(S4=None)) | PC_2 (Default Name) | Flip (NOT S4)        | (PlayerState, [Track], Track(S4="Jazz")) |
| 4          | (PlayerState, [Track], Track(S4="Jazz")) | PC_2 (Valid Name)   | None                 | N/A                                      |