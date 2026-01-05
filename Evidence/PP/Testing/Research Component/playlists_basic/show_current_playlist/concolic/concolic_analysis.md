# Concolic Analysis of `show_current_playlist` Function

## Path Exploration Table

| Iteration | Concrete Seed (S1, S2, S3, S4)  | Path Taken      | Constraint to Flip           | New Derived Input                         |
|-----------|---------------------------------|-----------------|------------------------------|-------------------------------------------|
| 1         | (None, N/A, N/A, N/A)           | PC_1 (Error)    | Flip (S1 == None)            | S1 = PlayerState() (Empty)                |
| 2         | (Obj, False, N/A, N/A)          | PC_2 (Error)    | Flip (NOT S2)                | S1 = PlayerState(playlists=[])            |
| 3         | (Obj, True, None, False)        | PC_3 (Guidance) | Flip (S3 == None)            | S1 = PlayerState(index=0, playlists=[])   |
| 4         | (Obj, True, 0, False)           | PC_4 (Guidance) | Flip (NOT S4)                | S1 = PlayerState(index=0, playlists=[pl]) |
| 5         | (Obj, True, 0, True)            | PC_5 (Success)  | None (All branches explored) | N/A                                       |
