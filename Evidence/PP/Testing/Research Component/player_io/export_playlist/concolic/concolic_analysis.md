# Concolic Analysis of `export_playlist` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2, S3, S4)              | Path Taken   | Constraint to Flip                    | New Derived Input                            |
|------------|---------------------------------------------|--------------|---------------------------------------|----------------------------------------------|
| 1          | ([], "test", "", [])                        | PC_2         | Flip (S4 IS Empty)                    | ([], "test", "", [Track])                    |
| 2          | ([], "test", "", [Track])                   | PC_3         | Flip (S1 Contains S2)                 | ([Playlist("test")], "test", "", [])         |
| 3          | ([Playlist("test")], "test", "", [])        | PC_1         | Flip (found_playlist.tracks IS Empty) | ([Playlist("test")], "test", "out", [Track]) |
| 4          | ([Playlist("test")], "test", "X/", [Track]) | PC_4         | None                                  | N/A                                          |