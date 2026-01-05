# Concolic Analysis table for toggle_shuffle Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3, S4, S5, S6, S7, S8, S9)              | Path Taken            | Constraint to Flip                 | New Derived Input             |
|-------------|-----------------------------------------------------------------|-----------------------|------------------------------------|-------------------------------|
| 1           | S1=None                                                         | PC_1 (Invalid State)  | Flip (S1 is None)                  | S1=PlayerState(), S2=[], S3=0 |
| 2           | S1=PlayerState(), S2=[]                                         | PC_2 (No Tracks)      | Flip (len(S2) == 0)                | S1=PlayerState(), S2=[T1, T2] |
| 3           | S1=PlayerState(), S2=[T1, T2], S4=0, S5='one'                   | PC_3 (Loop One)       | Flip (S5 == 'one')                 | S5='off'                      |
| 4           | S1=PlayerState(), S2=[T1, T2], S4=0, S5='off', S6=True, S7=[T1] | PC_4 (Shuffle)        | Flip (S6 AND S7)                   | S6=False, S7=[]               |
| 5           | S1=PlayerState(), S2=[T1, T2], S4=0, S5='all'                   | PC_6 (Wrap Logic)     | Flip (S5 == 'all')                 | S5='off'                      |
| 6           | S1=PlayerState(), S2=[T1, T2], S4=0                             | PC_7 (Start Boundary) | Flip (old < 0)                     | S4=1                          |
| 7           | S1=PlayerState(), S2=[T1, T2], S4=1                             | PC_7 (Normal Decr)    | None (All major branches explored) | N/A                           |

