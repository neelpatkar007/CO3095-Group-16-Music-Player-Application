# Concolic Analysis of `print_now_playing` Function

## Path Exploration Table
| Iteration  | Concrete Seed (S1..S6)               | Path Taken   | Constraint to Flip           | New Derived Input                         |
|------------|--------------------------------------|--------------|------------------------------|-------------------------------------------|
| 1          | (None, –, –, –, –, –)                | PC_1         | Flip (S1 == None)            | (StateObj, None, –, –, –, –)              |
| 2          | (StateObj, None, –, –, –, –)         | PC_2         | Flip (S2 == None)            | (StateObj, Track, False, –, –, –)         |
| 3          | (StateObj, Track, False, –, –, –)    | PC_3         | Flip (NOT S3)                | (StateObj, Track, True, False, –, –)      |
| 4          | (StateObj, Track, True, False, –, –) | PC_4         | Flip (NOT S4)                | (StateObj, Track, True, True, True, True) |
| 5          | (…, True, True)                      | PC_5         | Flip (S6 == True)            | (…, True, False)                          |
| 6          | (…, True, False)                     | PC_6         | Flip (S5 == True)            | (…, False, True)                          |
| 7          | (…, False, True)                     | PC_7         | Flip (S6 == True)            | (…, False, False)                         |
| 8          | (…, False, False)                    | PC_8         | None (All branches explored) | N/A                                       |