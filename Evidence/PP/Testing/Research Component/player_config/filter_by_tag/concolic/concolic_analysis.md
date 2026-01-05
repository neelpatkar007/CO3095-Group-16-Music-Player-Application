# Concolic Analysis for `filter_by_tag` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1, S2)                                  | Path Taken            | Constraint to Flip               | New Derived Input                                       |
|------------|---------------------------------------------------------|-----------------------|----------------------------------|---------------------------------------------------------|
| 1          | (None, "rock")                                          | PC_1 (State Error)    | Flip (S1 == None)                | (Obj{}, "rock")                                         |
| 2          | (Obj{}, "rock")                                         | PC_2 (Tag Attr Error) | Flip (S1.song_tags Invalid)      | (Obj{song_tags: {}}, "rock")                            |
| 3          | (Obj{song_tags: {}}, "rock")                            | PC_3 (Lib Attr Error) | Flip (S1.library_tracks Invalid) | (Obj{song_tags: {}, library_tracks: []}, "rock")        |
| 4          | (Obj{tags: {}, lib: []}, None)                          | PC_4 (Tag None Error) | Flip (S2 == None)                | (Obj{tags: {}, lib: []}, "rock")                        |
| 5          | (Obj{tags: {}, lib: []}, "rock")                        | PC_5 (No Matches)     | Flip (Matches == Empty)          | (Obj{tags: {"p1": ["rock"]}, lib: [Track(p1)]}, "rock") |
| 6          | (Obj{tags: {"p1": ["rock"]}, lib: [Track(p1)]}, "rock") | PC_6 (Success)        | None (All branches explored)     | N/A                                                     |