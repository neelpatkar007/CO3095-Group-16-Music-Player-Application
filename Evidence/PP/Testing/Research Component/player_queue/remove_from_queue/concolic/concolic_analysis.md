# Concolic Analysis of `remove_from_queue` Function

## Path Exploration Table
| Iteration | Concrete Seed (S1, S2)                   | Path Taken              | Constraint to Flip            | New Derived Input                             |
|-----------|------------------------------------------|-------------------------|-------------------------------|-----------------------------------------------|
| 1         | (None, "test")                           | PC_1 (Invalid State)    | Flip (S1 is Valid)            | (MockState{}, "test")                         |
| 2         | (MockState{}, "test")                    | PC_2 (No Tracks)        | Flip (S1 has Tracks)          | (MockState{tracks=[]}, "test")                |
| 3         | (MockState{tracks=[]}, "test")           | PC_3 (Empty Tracks)     | Flip (Tracks Not Empty)       | (MockState{tracks=[T1]}, "test")              |
| 4         | (MockState{tracks=[T1]}, None)           | PC_4 (Invalid Query)    | Flip (Query is Valid Str)     | (MockState{tracks=[T1]}, "1")                 |
| 5         | (MockState{tracks=[T1]}, "1")            | PC_5 (Digit, In Range)  | Flip (Index In Range)         | (MockState{tracks=[T1]}, "99")                |
| 6         | (MockState{tracks=[T1]}, "99")           | PC_6 (Digit, Out Range) | Flip (Query is Digit)         | (MockState{tracks=[T1(name="Jazz")]}, "Jazz") |
| 7         | (MockState{tracks=[T1("Jazz")]}, "Jazz") | PC_7 (String Match)     | Flip (String Match Found)     | (MockState{tracks=[T1("Jazz")]}, "Rock")      |
| 8         | (MockState{tracks=[T1("Jazz")]}, "Rock") | PC_8 (No Match)         | None (All branches covered)   | N/A                                           |

