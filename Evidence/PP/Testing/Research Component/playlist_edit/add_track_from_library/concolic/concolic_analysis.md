# Concolic Analysis of `add_track_from_library` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3)   | Path Taken  | Constraint to Flip    | New Derived Input           |
|------------|------------------------------|-------------|-----------------------|-----------------------------|
| 1          | (None, "", "")               | PC_1        | S1 != None            | (MockObj, "", "")           |
| 2          | (MockObj, "", "")            | PC_2        | NOT (NOT S2)          | (MockObj, "Favs", "")       |
| 3          | (MockObj, "Favs", "")        | PC_3        | NOT (NOT S3)          | (MockObj, "Favs", "1")      |
| 4          | (MockObj_Empty, "Favs", "1") | PC_4        | S1.tracks exists      | (MockObj_Full, "Favs", "1") |
| 5          | (Mock_Full, "Bad", "1")      | PC_5        | _get_playlist != None | (Mock_Full, "Good", "1")    |
| 6          | (Mock_Full, "Good", "abc")   | PC_6        | is_int(S3)            | (Mock_Full, "Good", "1")    |
| 7          | (Mock_Full, "Good", "99")    | PC_7        | in_bounds(S3)         | (Mock_Full, "Good", "1")    |