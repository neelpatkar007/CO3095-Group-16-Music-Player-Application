# Concolic Analysis: copy_playlist Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3)            | Path Taken   | Constraint to Flip            | New Derived Input                     |
|------------|---------------------------------------|--------------|-------------------------------|---------------------------------------|
| 1          | (None, "rock", 123)                   | PC_1         | Flip (isinstance S3, str)     | (None, "rock", "help")                |
| 2          | (None, "rock", "help")                | PC_2         | Flip (S3 NOT IN reserved)     | (None, "rock", "NewPl")               |
| 3          | (None, "rock", "NewPl")               | PC_3         | Flip (S1 is Valid)            | (StateObj, "rock", "NewPl")           |
| 4          | (StateObj[0], "rock", "NewPl")        | PC_4         | Flip (S1.playlists NOT empty) | (StateObj[1], "rock", "NewPl")        |
| 5          | (StateObj[1], "rock", "  ")           | PC_5         | Flip (S3.strip NOT empty)     | (StateObj[1], "rock", "A")            |
| 6          | (StateObj[1], "rock", "A")            | PC_6         | Flip (len S3 >= 3)            | (StateObj[1], "rock", "LongName" * 5) |
| 7          | (StateObj[1], "rock", "LongName" * 5) | PC_7         | Flip (len S3 <= 20)           | (StateObj[1], "rock", "New!@#")       |
| 8          | (StateObj[1], "rock", "New!@#")       | PC_8         | Flip (S3 is alnum)            | (StateObj[1], "rock", "admin")        |
| 9          | (StateObj[1], "rock", "admin")        | PC_9         | Flip (S3 NOT IN admin_list)   | (StateObj[1], "invalid", "ValidName") |
| 10         | (StateObj[1], "invalid", "ValidName") | PC_10        | Flip (Source IS NOT None)     | (StateObj[1], "rock", "Existing")     |
| 11         | (StateObj[1], "rock", "Existing")     | PC_11        | Flip (S3 NOT IN state)        | (StateObj[1], "rock", "UniqueName")   |
| 12         | (StateObj[1], "rock", "UniqueName")   | PC_12        | None                          | N/A                                   |