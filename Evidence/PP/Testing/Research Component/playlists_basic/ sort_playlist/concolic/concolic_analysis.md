# Concolic Analysis: `sort_playlist`

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2, S3)                   | Path Taken  | Constraint to Flip               | New Derived Input                 |
|-----------|----------------------------------------------|-------------|----------------------------------|-----------------------------------|
| 1         | (None, "rock", "title")                      | PC_1        | Flip (S1 is None)                | (MockState, "rock", "title")      |
| 2         | (MockState, "", "title")                     | PC_2        | Flip (S2 is Empty)               | (MockState, "valid_sel", "title") |
| 3         | (MockState, "valid_sel", None)               | PC_3        | Flip (S3 is None / NotStr)       | (MockState, "valid_sel", "title") |
| 4         | (MockState, "valid_sel", "title")            | PC_4        | Flip (S4 is None) -> Mock return | (MockState… Pl=Valid)             |
| 5         | (MockState… Pl=Valid, tracks=None)           | PC_5        | Flip (S5 is None) -> Mock attr   | (MockState… Pl.tracks=[])         |
| 6         | (MockState… Pl.tracks=[])                    | PC_6        | Flip (S5 Empty) -> Inject items  | (MockState… Pl.tracks=[Item])     |
| 7         | (MockState… Pl.tracks=[Item], S3="title")    | PC_7        | Flip (S6 == "title")             | (MockState… S3="artist")          |
| 8         | (MockState… Pl.tracks=[Item], S3="artist")   | PC_9        | Flip (S6 == "artist")            | (MockState… S3="duration")        |
| 9         | (MockState… Pl.tracks=[Item], S3="duration") | PC_11       | Flip (S6 == "duration")          | (MockState… S3="genre")           |
| 10        | (MockState… Pl.tracks=[Item], S3="genre")    | PC_13       | None (Branch Exhausted)          | N/A                               |