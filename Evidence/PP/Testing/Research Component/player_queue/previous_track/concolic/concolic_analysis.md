# Concolic Analysis Report for Player Queue - Previous Track Function

## Path Exploration Table
| Iteration   | Concrete Seed (S1, S2, S3…)            | Path Taken                | Constraint to Flip  | New Derived Input    |
|-------------|----------------------------------------|---------------------------|---------------------|----------------------|
| 1           | S1=None                                | PC_1 (Invalid State)      | Flip (S1 is None)   | S1=State(), S2=[]    |
| 2           | S1=State(), S2=[]                      | PC_2 (No Tracks)          | Flip (Not Tracks)   | S1=State(), S2=[T1]  |
| 3           | S1=State(), S2=[T1], S5="one"          | PC_7 (via Loop One logic) | Flip (S5 == "one")  | S1=State(), S5="off" |
| 4           | S1=State(), S5="off", S6=True, S7=[T1] | PC_7 (via Shuffle)        | Flip (S6 AND S7)    | S1=State(), S6=False |
| 5           | S1=State(), S5="all", S4=0             | PC_7 (Wrap Logic)         | Flip (S5 == "all")  | S1=State(), S5="off" |
| 6           | S1=State(), S5="off", S4=0             | PC_7 (Start Boundary)     | Flip (old < 0)      | S1=State(), S4=1     |
| 7           | S1=State(), S5="off", S4=1             | PC_7 (Normal Decr)        | None (Max Coverage) | N/A                  |