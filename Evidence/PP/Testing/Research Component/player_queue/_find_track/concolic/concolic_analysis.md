# Concolic Analysis of `_find_track` Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2)                 | Path Taken                     | Constraint to Flip           | New Derived Input                                  |
|:------------|:---------------------------------------|:-------------------------------|:-----------------------------|:---------------------------------------------------|
| 1           | (S1={}, S2="abc")                      | PC_3 (String Fail)             | Flip (S2.isdigit() == False) | (S1={}, S2="1")                                    |
| 2           | (S1={}, S2="1")                        | PC_3 (Num Fail -> String Fail) | Flip (S1 has library_tracks) | (S1={library_tracks:[]}, S2="1")                   |
| 3           | (S1={library_tracks:[]}, S2="1")       | PC_3 (Idx Bounds Fail)         | Flip (idx < len(S1.tracks))  | (S1={library_tracks:[Obj]}, S2="1")                |
| 4           | (S1={library_tracks:[TrkA]}, S2="1")   | PC_1 (Numeric Success)         | Backtrack, Flip Name Match   | (S1={library_tracks:[TrkB(name="abc")]}, S2="abc") |
| 5           | (S1={library_tracks:[TrkB]}, S2="abc") | PC_2 (String Success)          | Force Exception              | (S1=None, S2=None)                                 |
| 6           | (S1=None, S2=None)                     | PC_4 (Exception)               | None (All branches explored) | N/A                                                |